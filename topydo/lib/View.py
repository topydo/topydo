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

""" A view is a list of todos, sorted and filtered. """

from topydo.lib.PrettyPrinterFilter import (
    PrettyPrinterColorFilter,
    PrettyPrinterNumbers
)
from topydo.lib.PrettyPrinter import PrettyPrinter

class View(object):
    """
    A view is instantiated by a todo list, usually obtained from a todo.txt
    file. Also a sorter and a list of filters should be given that is applied
    to the list.

    A printer can be passed, but it won't be used when pretty_print() is
    called, since it will instantiate its own pretty printer instance.
    """
    def __init__(self, p_sorter, p_filters, p_todolist,
            p_printer=PrettyPrinter()):

        self._todolist = p_todolist
        self._viewdata = []
        self._sorter = p_sorter
        self._filters = p_filters
        self._printer = p_printer

        self.update()

    def update(self):
        """
        Updates the view data. Should be called when the backing todo list
        has changed.
        """
        self._viewdata = self._sorter.sort(self._todolist.todos())

        for _filter in self._filters:
            self._viewdata = _filter.filter(self._viewdata)

    def pretty_print(self, p_pp_filters=None):
        """ Pretty prints the view. """
        p_pp_filters = p_pp_filters or []

        # since we're using filters, always use PrettyPrinter
        printer = PrettyPrinter()

        printer.add_filter(PrettyPrinterNumbers(self._todolist))

        for ppf in p_pp_filters:
            printer.add_filter(ppf)

        # apply colors at the last step, the ANSI codes may confuse the
        # preceding filters.
        printer.add_filter(PrettyPrinterColorFilter())

        return printer.print_list(self._viewdata)

    def __str__(self):
        return self._printer.print_list(self._viewdata)
