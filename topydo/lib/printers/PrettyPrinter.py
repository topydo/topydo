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

from topydo.lib.prettyprinters.Colors import PrettyPrinterColorFilter
from topydo.lib.prettyprinters.Numbers import PrettyPrinterNumbers
from topydo.lib.TopydoString import TopydoString


class Printer(object):
    """
    An abstract class that turns todo items into strings.

    Subclasses must at least implement the print_todo method.
    """

    def print_todo(self, p_todo):
        raise NotImplementedError

    def print_list(self, p_todos):
        for todo in p_todos:
            self.print_todo(todo)


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
        super().__init__()
        self.filters = []

    def add_filter(self, p_filter):
        """
        Adds a filter to be applied when calling print_todo.

        p_filter is an instance of a PrettyPrinterFilter.
        """
        self.filters.append(p_filter)

    def print_todo(self, p_todo):
        """ Given a todo item, pretty print it. """
        todo_str = p_todo.source()

        for ppf in self.filters:
            todo_str = ppf.filter(todo_str, p_todo)

        return TopydoString(todo_str)

    def print_list(self, p_todos):
        """
        Given a list of todo items, pretty print it and return a list of
        formatted TopydoStrings. The output function in the UI should convert
        the colors inside properly.
        """
        return [self.print_todo(todo) for todo in p_todos]


def pretty_printer_factory(p_todolist, p_additional_filters=None):
    """ Returns a pretty printer suitable for the ls and dep subcommands. """
    p_additional_filters = p_additional_filters or []

    printer = PrettyPrinter()
    printer.add_filter(PrettyPrinterNumbers(p_todolist))

    for ppf in p_additional_filters:
        printer.add_filter(ppf)

    # apply colors at the last step, the ANSI codes may confuse the
    # preceding filters.
    printer.add_filter(PrettyPrinterColorFilter())

    return printer
