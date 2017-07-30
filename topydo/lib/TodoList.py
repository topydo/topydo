# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2015 Bram Schoenmakers <bram@topydo.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
A list of todo items.
"""

import types

from topydo.lib.Config import config
from topydo.lib.TodoListBase import TodoListBase


def _needs_dependencies(p_function):
    """
    A decorator that triggers the population of the dependency tree in a
    TodoList (and other administration). The decorator should be applied to
    methods of TodoList that require dependency information.
    """
    def build_dependency_information(p_todolist):
        for todo in p_todolist._todos:
            p_todolist._register_todo(todo)

    def inner(self, *args, **kwargs):
        if not self._initialized:
            self._initialized = True

            from topydo.lib.Graph import DirectedGraph
            self._depgraph = DirectedGraph()

            build_dependency_information(self)

        return p_function(self, *args, **kwargs)

    return inner

class TodoList(TodoListBase):
    """
    Provides operations for a todo list, such as adding items, removing them,
    etc.

    The list is usually a complete list found in the program's input (e.g. a
    todo.txt file), not an arbitrary set of todo items.
    """

    def __init__(self, p_todostrings):
        """
        Should be given a list of strings, each element a single todo string.
        The string will be parsed.
        """
        self._initialized = False  # whether dependency information was
                                   # initialized

        # initialize these first because the constructor calls add_list
        self._tododict = {}  # hash(todo) to todo lookup
        self._parentdict = {}  # dependency id => parent todo
        self._depgraph = None

        super().__init__(p_todostrings)

    @_needs_dependencies
    def todo_by_dep_id(self, p_dep_id):
        """
        Returns the todo that has the id tag set to the value p_dep_id.
        There is only one such task, the behavior is undefined when a todo item
        has more than one id tag.
        """
        try:
            return self._parentdict[p_dep_id]
        except KeyError:
            return None

    def _maintain_dep_graph(self, p_todo):
        """
        Makes sure that the dependency graph is consistent according to the
        given todo.
        """
        dep_id = p_todo.tag_value('id')
        # maintain dependency graph
        if dep_id:
            self._parentdict[dep_id] = p_todo
            self._depgraph.add_node(hash(p_todo))

            # connect all tasks we have in memory so far that refer to this
            # task
            for dep in \
                    [dep for dep in self._todos if dep.has_tag('p', dep_id)]:

                self._add_edge(p_todo, dep, dep_id)

        for dep_id in p_todo.tag_values('p'):
            try:
                parent = self._parentdict[dep_id]
                self._add_edge(parent, p_todo, dep_id)
            except KeyError:
                pass

    def _register_todo(self, p_todo):
        self._maintain_dep_graph(p_todo)
        self._tododict[hash(p_todo)] = p_todo

    def add_todos(self, p_todos):
        super().add_todos(p_todos)

        for todo in self._todos:
            todo.parents = types.MethodType(self.parents, todo)

            # only do administration when the dependency info is initialized,
            # otherwise we postpone it until it's really needed (through the
            # _needs_dependencies decorator)
            if self._initialized:
                self._register_todo(todo)

    def delete(self, p_todo, p_leave_tags=False):
        """ Deletes a todo item from the list. """
        try:
            number = self._todos.index(p_todo)

            if p_todo.has_tag('id'):
                for child in self.children(p_todo):
                    self.remove_dependency(p_todo, child, p_leave_tags)

            if p_todo.has_tag('p'):
                for parent in self.parents(p_todo):
                    self.remove_dependency(parent, p_todo, p_leave_tags)

            del self._todos[number]
            self._update_todo_ids()

            self.dirty = True
        except ValueError:
            # todo item couldn't be found, ignore
            pass

    def _add_edge(self, p_from_todo, p_to_todo, p_dep_id):
        self._parentdict[p_dep_id] = p_from_todo
        self._depgraph.add_edge(hash(p_from_todo), hash(p_to_todo), p_dep_id)

    @_needs_dependencies
    def add_dependency(self, p_from_todo, p_to_todo):
        """ Adds a dependency from task 1 to task 2. """
        def find_next_id():
            """
            Find a new unused ID.
            Unused means that no task has it as an 'id' value or as a 'p'
            value.
            """
            def id_exists(p_id):
                """
                Returns True if there exists a todo with the given parent ID.
                """
                for todo in self._todos:
                    number = str(p_id)
                    if todo.has_tag('id', number) or todo.has_tag('p', number):
                        return True

                return False

            new_id = 1
            while id_exists(new_id):
                new_id += 1

            return str(new_id)

        def append_projects_to_subtodo():
            """
            Appends projects in the parent todo item that are not present in
            the sub todo item.
            """
            if config().append_parent_projects():
                for project in p_from_todo.projects() - p_to_todo.projects():
                    self.append(p_to_todo, "+{}".format(project))

        def append_contexts_to_subtodo():
            """
            Appends contexts in the parent todo item that are not present in
            the sub todo item.
            """
            if config().append_parent_contexts():
                for context in p_from_todo.contexts() - p_to_todo.contexts():
                    self.append(p_to_todo, "@{}".format(context))

        if p_from_todo != p_to_todo and not self._depgraph.has_edge(
                hash(p_from_todo), hash(p_to_todo)):

            dep_id = None
            if p_from_todo.has_tag('id'):
                dep_id = p_from_todo.tag_value('id')
            else:
                dep_id = find_next_id()
                p_from_todo.set_tag('id', dep_id)

            p_to_todo.add_tag('p', dep_id)
            self._add_edge(p_from_todo, p_to_todo, dep_id)
            append_projects_to_subtodo()
            append_contexts_to_subtodo()
            self.dirty = True

    @_needs_dependencies
    def remove_dependency(self, p_from_todo, p_to_todo, p_leave_tags=False):
        """ Removes a dependency between two todos. """
        dep_id = p_from_todo.tag_value('id')

        if dep_id:
            self._depgraph.remove_edge(hash(p_from_todo), hash(p_to_todo))
            self.dirty = True

        # clean dangling dependency tags
        if dep_id and not p_leave_tags:
            p_to_todo.remove_tag('p', dep_id)

            if not self.children(p_from_todo, True):
                p_from_todo.remove_tag('id')
                del self._parentdict[dep_id]

    @_needs_dependencies
    def parents(self, p_todo, p_only_direct=False):
        """
        Returns a list of parent todos that (in)directly depend on the
        given todo.
        """
        parents = self._depgraph.incoming_neighbors(
            hash(p_todo), not p_only_direct)
        return [self._tododict[parent] for parent in parents]

    @_needs_dependencies
    def children(self, p_todo, p_only_direct=False):
        """
        Returns a list of child todos that the given todo (in)directly depends
        on.
        """
        children = \
            self._depgraph.outgoing_neighbors(hash(p_todo), not p_only_direct)
        return [self._tododict[child] for child in children]

    @_needs_dependencies
    def clean_dependencies(self):
        """
        Cleans the dependency graph.

        This is achieved by performing a transitive reduction on the dependency
        graph and removing unused dependency ids from the graph (in that
        order).
        """
        def remove_tag(p_todo, p_tag, p_value):
            """
            Removes a tag from a todo item.
            """
            p_todo.remove_tag(p_tag, p_value)
            self.dirty = True

        def clean_parent_relations():
            """
            Remove id: tags for todos without child todo items.
            """

            for todo in [todo for todo in self._todos if todo.has_tag('id')]:
                value = todo.tag_value('id')
                if not self._depgraph.has_edge_id(value):
                    remove_tag(todo, 'id', value)
                    del self._parentdict[value]

        def clean_orphan_relations():
            """
            Remove p: tags for todos referring to a parent that is not in the
            dependency graph anymore.
            """

            for todo in [todo for todo in self._todos if todo.has_tag('p')]:
                for value in todo.tag_values('p'):
                    parent = self.todo_by_dep_id(value)

                    if not self._depgraph.has_edge(hash(parent), hash(todo)):
                        remove_tag(todo, 'p', value)

        self._depgraph.transitively_reduce()
        clean_parent_relations()
        clean_orphan_relations()
