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

class Printer(object):
    """
    An abstract class that turns todo items into strings.

    Subclasses must at least implement the print_todo method.
    """
    def print_todo(self, p_todo):
        """ Base implementation. Simply returns the string conversion. """
        return str(p_todo)

    def print_list(self, p_todos):
        """
        Given a list of todo items, pretty print it and return a list of
        formatted strings.
        """
        return "\n".join([self.print_todo(todo) for todo in p_todos])

class PrettyPrinter(Printer):
    """
    Prints todo items on a single line, decorated by the filters passed by
    the caller.

    The caller can adjust the output by passing on a set of filters, that may
    add colors, indentation, etc. These filters are found in the
    PrettyPrinterFilter module.
    """
    def __init__(self):
        """
        Constructor.
        """
        super(PrettyPrinter, self).__init__()
        self.filters = []

    def add_filter(self, p_filter):
        """
        Adds a filter to be applied when calling print_todo.

        p_filter is an instance of a PrettyPrinterFilter.
        """
        self.filters.append(p_filter)

    def print_todo(self, p_todo):
        """ Given a todo item, pretty print it. """
        todo_str = str(p_todo)

        for ppf in self.filters:
            todo_str = ppf.filter(todo_str, p_todo)

        return todo_str
