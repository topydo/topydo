# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 Bram Schoenmakers <me@bramschoenmakers.nl>
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

import re

import Filter
import Graph
from PrettyPrinter import pretty_print_list
import Todo
import View

class InvalidTodoException(Exception):
    pass

class TodoList(object):
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
        self._todos = []
        self._depgraph = Graph.DirectedGraph()

        for string in p_todostrings:
            self.add(string)

        self.dirty = False

    def todo(self, p_identifier):
        """
        The _todos list has the same order as in the backend store (usually
        a todo.txt file. The user refers to the first task as number 1, so use
        index 0, etc.
        """
        result = None
        try:
            result = self._todos[int(p_identifier) - 1]
        except IndexError:
            raise InvalidTodoException
        except (TypeError, ValueError):
            result = self.todo_by_regexp(p_identifier)

        return result

    def todo_by_regexp(self, p_identifier):
        """
        Returns the todo that is (uniquely) identified by the given regexp.
        If the regexp matches more than one item, no result is returned.
        """
        result = None

        candidates = Filter.GrepFilter(p_identifier).filter(self._todos)

        if len(candidates) == 1:
            result = candidates[0]
        else:
            raise InvalidTodoException

        return result

    def todo_by_hash(self, p_hash):
        """
        Given the hash value of a todo, return the corresponding instance.
        """

        result = None
        for todo in self._todos:
            if hash(todo) == p_hash:
                result = todo
                break
        return result

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

    def add(self, p_src):
        """ Given a todo string, parse it and put it to the end of the list. """
        todo = None
        if re.search(r'\S', p_src):
            todo = Todo.Todo(p_src)
            self.add_todo(todo)

        return todo

    def add_todo(self, p_todo):
        """
        Add an Todo object to the list.

        Also maintains the dependency graph to track the dependencies between
        tasks.

        The node ids are the todo numbers.
        The edge ids are the numbers denoted by id: and p: tags.

        For example:

        (C) Parent task id:4
        (B) Child task p:4

        Then there will be an edge 1 --> 2 with ID 4.
        """
        self._todos.append(p_todo)

        self._maintain_dep_graph(p_todo)
        self._update_parent_cache()
        self.dirty = True

    def delete(self, p_todo):
        """ Deletes a todo item from the list. """
        number = self.number(p_todo)

        for child in self.children(p_todo):
            self.remove_dependency(p_todo, child)

        for parent in self.parents(p_todo):
            self.remove_dependency(parent, p_todo)

        del self._todos[number - 1]

        self.dirty = True

    def erase(self):
        """
        Erases all todos from the list.
        Not done with self.delete to prevent dependencies disappearing from the
        todo items.
        """

        self._todos = []
        self.dirty = True

    def count(self):
        """ Returns the number of todos on this list. """
        return len(self._todos)

    def append(self, p_todo, p_string):
        """
        Appends a text to the todo, specified by its number.
        The todo will be parsed again, such that tags and projects in de
        appended string are processed.
        """
        if len(p_string) > 0:
            new_text = p_todo.source() + ' ' + p_string
            p_todo.set_source_text(new_text)
            self.dirty = True

    def projects(self):
        """ Returns a set of all projects in this list. """
        result = set()
        for todo in self._todos:
            projects = todo.projects()
            result = result.union(projects)

        return result

    def contexts(self):
        """ Returns a set of all contexts in this list. """
        result = set()
        for todo in self._todos:
            contexts = todo.contexts()
            result = result.union(contexts)

        return result

    def view(self, p_sorter, p_filters):
        """
        Constructs a view of the todo list.

        A view is a sorted and filtered todo list, where the properties are
        defined by the end user. Todos is this list should not be modified,
        modifications should occur through this class.
        """
        return View.View(p_sorter, p_filters, self)

    def add_dependency(self, p_from_todo, p_to_todo):
        """ Adds a dependency from task 1 to task 2. """
        def find_next_id():
            """
            Find a new unused ID.
            Unused means that no task has it as an 'id' value or as a 'p'
            value.
            """

            new_id = 1
            while self._depgraph.has_edge_id('%d' % new_id):
                new_id += 1

            return '%d' % new_id

        if p_from_todo != p_to_todo and not self._depgraph.has_edge(hash(p_from_todo), hash(p_to_todo)):
            dep_id = None
            if p_from_todo.has_tag('id'):
                dep_id = p_from_todo.tag_value('id')
            else:
                dep_id = find_next_id()
                p_from_todo.set_tag('id', dep_id)

            p_to_todo.add_tag('p', dep_id)
            self._depgraph.add_edge(hash(p_from_todo), hash(p_to_todo), dep_id)
            self._update_parent_cache()
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
        parents = self._depgraph.incoming_neighbors(hash(p_todo), not p_only_direct)
        return [self.todo_by_hash(parent) for parent in parents]

    def children(self, p_todo, p_only_direct=False):
        """
        Returns a list of child todos that the given todo (in)directly depends
        on.
        """
        children = \
            self._depgraph.outgoing_neighbors(hash(p_todo), not p_only_direct)
        return [self.todo_by_hash(child) for child in children]

    def clean_dependencies(self):
        """
        Cleans the dependency graph.

        This is achieved by performing a transitive reduction on the dependency
        graph and removing unused dependency ids from the graph (in that
        order).
        """
        def clean_by_tag(tag_name):
            """ Generic function to handle 'p' and 'id' tags. """
            for todo in [todo for todo in self._todos if todo.has_tag(tag_name)]:
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

    def is_dirty(self):
        return self.dirty

    def set_dirty(self):
        self.dirty = True

    def todos(self):
        return self._todos

    def set_todo_completed(self, p_todo):
        p_todo.set_completed()
        self.dirty = True

    def set_priority(self, p_todo, p_priority):
        if p_todo.priority() != p_priority:
            p_todo.set_priority(p_priority)
            self.dirty = True

    def number(self, p_todo):
        try:
            return self._todos.index(p_todo) + 1
        except ValueError:
            raise InvalidTodoException

    def pp_number(self):
        """
        A filter for the pretty printer to append the todo number to the
        printed todo.
        """
        return lambda p_todo_str, p_todo: "%3d %s" % (self.number(p_todo), p_todo_str)

    def __str__(self):
        return '\n'.join(pretty_print_list(self._todos))

