# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2015 Bram Schoenmakers <me@bramschoenmakers.nl>
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

from topydo.lib.Config import config
from topydo.lib.Graph import DirectedGraph
from topydo.lib.TodoListBase import TodoListBase

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
        # initialize these first because the constructor calls add_list
        self._tododict = {} # hash(todo) to todo lookup
        self._depgraph = DirectedGraph()

        super(TodoList, self).__init__(p_todostrings)

    def todo_by_dep_id(self, p_dep_id):
        """
        Returns the todo that has the id tag set to the value p_dep_id.
        There is only one such task, the behavior is undefined when a tag has
        more than one id tag.
        """
        hits = [t for t in self._todos if t.tag_value('id') == p_dep_id]

        return hits[0] if len(hits) else None

    def _maintain_dep_graph(self, p_todo):
        """
        Makes sure that the dependency graph is consistent according to the
        given todo.
        """

        dep_id = p_todo.tag_value('id')
        # maintain dependency graph
        if dep_id:
            self._depgraph.add_node(hash(p_todo))

            # connect all tasks we have in memory so far that refer to this
            # task
            for dep in \
                [dep for dep in self._todos if dep.has_tag('p', dep_id)]:

                self._depgraph.add_edge(hash(p_todo), hash(dep), dep_id)

        for child in p_todo.tag_values('p'):
            parent = self.todo_by_dep_id(child)
            if parent:
                self._depgraph.add_edge(hash(parent), hash(p_todo), child)

    def add_todos(self, p_todos):
        for todo in p_todos:
            self._todos.append(todo)
            self._tododict[hash(todo)] = todo
            self._maintain_dep_graph(todo)

        self._update_todo_ids()
        self._update_parent_cache()
        self.dirty = True

    def delete(self, p_todo):
        """ Deletes a todo item from the list. """
        try:
            number = self._todos.index(p_todo)

            for child in self.children(p_todo):
                self.remove_dependency(p_todo, child)

            for parent in self.parents(p_todo):
                self.remove_dependency(parent, p_todo)

            del self._todos[number]
            self._update_todo_ids()

            self.dirty = True
        except ValueError:
            # todo item couldn't be found, ignore
            pass

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
                Returns True if there exists a todo with the given parent
                ID.
                """
                for todo in self._todos:
                    if todo.has_tag('id', str(p_id)):
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
            self._depgraph.add_edge(hash(p_from_todo), hash(p_to_todo), dep_id)
            self._update_parent_cache()
            append_projects_to_subtodo()
            append_contexts_to_subtodo()
            self.dirty = True

    def remove_dependency(self, p_from_todo, p_to_todo):
        """ Removes a dependency between two todos. """
        dep_id = p_from_todo.tag_value('id')

        if dep_id:
            p_to_todo.remove_tag('p', dep_id)
            self._depgraph.remove_edge(hash(p_from_todo), hash(p_to_todo))
            self._update_parent_cache()

            if not self.children(p_from_todo, True):
                p_from_todo.remove_tag('id')

            self.dirty = True

    def parents(self, p_todo, p_only_direct=False):
        """
        Returns a list of parent todos that (in)directly depend on the
        given todo.
        """
        parents = self._depgraph.incoming_neighbors(
            hash(p_todo), not p_only_direct)
        return [self._tododict[parent] for parent in parents]

    def children(self, p_todo, p_only_direct=False):
        """
        Returns a list of child todos that the given todo (in)directly depends
        on.
        """
        children = \
            self._depgraph.outgoing_neighbors(hash(p_todo), not p_only_direct)
        return [self._tododict[child] for child in children]

    def clean_dependencies(self):
        """
        Cleans the dependency graph.

        This is achieved by performing a transitive reduction on the dependency
        graph and removing unused dependency ids from the graph (in that
        order).
        """
        def clean_by_tag(tag_name):
            """ Generic function to handle 'p' and 'id' tags. """
            for todo in [todo for todo in self._todos
                if todo.has_tag(tag_name)]:

                value = todo.tag_value(tag_name)
                if not self._depgraph.has_edge_id(value):
                    todo.remove_tag(tag_name, value)
                    self.dirty = True

        self._depgraph.transitively_reduce()
        clean_by_tag('p')
        clean_by_tag('id')

    def _update_parent_cache(self):
        """
        Sets the attribute to the list of parents, such that others may access
        it outside this todo list.
        This is used for calculating the average importance, that requires
        access to a todo's parents.
        """

        for todo in self._todos:
            todo.attributes['parents'] = self.parents(todo)
