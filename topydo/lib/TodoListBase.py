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

import re
from datetime import date

from topydo.lib import Filter
from topydo.lib.Config import config
from topydo.lib.HashListValues import hash_list_values
from topydo.lib.PrettyPrinter import PrettyPrinter
from topydo.lib.RelativeDate import relative_date_to_date
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
        self._todo_id_map = {}
        self._id_todo_map = {}

        self.add_list(p_todostrings)
        self.dirty = False

    def __iter__(self):
        """
        Allows use of `for my_todo in todolist` constructs.
        """
        return iter(self._todos)

    def todo(self, p_identifier):
        """
        The _todos list has the same order as in the backend store (usually
        a todo.txt file. The user refers to the first task as number 1, so use
        index 0, etc.

        Alternative ways to identify a todo is using a hashed version based on
        the todo's text, or a regexp that matches the todo's source. The regexp
        match is a fallback.

        Returns None when the todo couldn't be found.
        """
        result = None

        def todo_by_uid(p_identifier):
            """ Returns the todo that corresponds to the unique ID. """
            result = None

            if config().identifiers() == 'text':
                try:
                    result = self._id_todo_map[p_identifier]
                except KeyError:
                    pass  # we'll try something else

            return result

        def todo_by_linenumber(p_identifier):
            """
            Attempts to find the todo on the given line number.

            When the identifier is a number but has leading zeros, the result
            will be None.
            """
            result = None

            if config().identifiers() != 'text':
                try:
                    if re.match('[1-9]\d*', p_identifier):
                        # the expression is a string and no leading zeroes,
                        # treat it as an integer
                        raise TypeError
                except TypeError as te:
                    try:
                        result = self._todos[int(p_identifier) - 1]
                    except (ValueError, IndexError):
                        raise InvalidTodoException from te

            return result

        def todo_by_regexp(p_identifier):
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

        result = todo_by_uid(p_identifier)

        if not result:
            result = todo_by_linenumber(p_identifier)

        if not result:
            # convert integer to text so we pass on a valid regex
            result = todo_by_regexp(str(p_identifier))

        return result

    def add(self, p_src):
        """
        Given a todo string, parse it and put it to the end of the list.
        """
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

        self._update_todo_ids()
        self.dirty = True

    def delete(self, p_todo):
        """ Deletes a todo item from the list. """
        try:
            number = self._todos.index(p_todo)
            del self._todos[number]
            self._update_todo_ids()
            self.dirty = True
        except ValueError:
            # todo item couldn't be found, ignore
            pass

    def erase(self):
        """ Erases all todos from the list. """
        self._todos = []
        self.dirty = True

    def replace(self, p_todos):
        """ Replaces whole todolist with todo objects supplied as p_todos. """
        self.erase()
        self.add_todos(p_todos)
        self.dirty = True

    def count(self):
        """ Returns the number of todos on this list. """
        return len(self._todos)

    def _convert_date(self, p_todo, p_tag):
        """
        For the given tag, attemps to convert a relative date to an absolute
        date.
        """
        value = p_todo.tag_value(p_tag)

        if value:
            dateobj = relative_date_to_date(value)
            if dateobj:
                p_todo.set_tag(p_tag, dateobj.isoformat())

    def append(self, p_todo, p_string):
        """
        Appends a text to the todo, specified by its number.
        The todo will be parsed again, such that tags and projects in the
        appended string are processed.
        """
        if len(p_string) > 0:
            new_text = p_todo.source() + ' ' + p_string
            p_todo.set_source_text(new_text)

            self._convert_date(p_todo, config().tag_start())
            self._convert_date(p_todo, config().tag_due())

            self._update_todo_ids()
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
        """
        Returns the line number or text ID of a todo (depends on the
        configuration.
        """
        try:
            if config().identifiers() == 'text':
                return self._todo_id_map[p_todo]
            else:
                return self._todos.index(p_todo) + 1
        except (ValueError, KeyError) as ex:
            raise InvalidTodoException from ex

    def _update_todo_ids(self):
        # the idea is to have a hash that is independent of the position of the
        # todo. Use the text (without tags) of the todo to keep the id as
        # stable as possible (not influenced by priorities or due dates, etc.)
        self._todo_id_map = {}
        self._id_todo_map = {}

        uids = hash_list_values(self._todos, lambda t: t.text())

        for (todo, uid) in uids:
            self._todo_id_map[todo] = uid
            self._id_todo_map[uid] = todo

    def print_todos(self):
        """
        Returns a pretty-printed string (without colors) of the todo items in
        this list.
        """
        printer = PrettyPrinter()
        return printer.print_list(self._todos)
