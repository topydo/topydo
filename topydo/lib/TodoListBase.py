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

from datetime import date
import re

from topydo.lib import Filter
from topydo.lib.PrettyPrinter import pretty_print_list
from topydo.lib.Todo import Todo
from topydo.lib.View import View

class InvalidTodoException(Exception):
    pass

class TodoListBase(object):
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

        self.add_list(p_todostrings)
        self.dirty = False

    def todo(self, p_identifier):
        """
        The _todos list has the same order as in the backend store (usually
        a todo.txt file. The user refers to the first task as number 1, so use
        index 0, etc.
        """
        result = None
        try:
            try:
                if not re.match('[1-9]\d*', p_identifier):
                    raise ValueError # leading zeros, pass to regexp
            except TypeError:
                # we're dealing with an integer
                pass

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

    def add(self, p_src):
        """ Given a todo string, parse it and put it to the end of the list. """
        todos = self.add_list([p_src])

        return todos[0] if len(todos) else None

    def add_list(self, p_srcs):
        todos = [Todo(src) for src in p_srcs if re.search(r'\S', src)]
        self.add_todos(todos)

        return todos

    def add_todo(self, p_todo):
        """ Add an Todo object to the list. """
        self.add_todos([p_todo])

    def add_todos(self, p_todos):
        for todo in p_todos:
            self._todos.append(todo)

        self.dirty = True

    def delete(self, p_todo):
        """ Deletes a todo item from the list. """
        number = self.number(p_todo)
        del self._todos[number - 1]
        self.dirty = True

    def erase(self):
        """ Erases all todos from the list. """
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
        return View(p_sorter, p_filters, self)

    def is_dirty(self):
        return self.dirty

    def set_dirty(self):
        self.dirty = True

    def todos(self):
        return self._todos

    def set_todo_completed(self, p_todo, p_completion_date=date.today()):
        p_todo.set_completed(p_completion_date)
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
        return lambda p_todo_str, p_todo: \
            "%3d %s" % (self.number(p_todo), p_todo_str)

    def __str__(self):
        return '\n'.join(pretty_print_list(self._todos))

