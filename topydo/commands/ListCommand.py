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

from topydo.lib.ExpressionCommand import ExpressionCommand
from topydo.lib.Config import config
from topydo.lib.PrettyPrinter import pretty_printer_factory
from topydo.lib.PrettyPrinterFilter import (
    PrettyPrinterIndentFilter,
    PrettyPrinterHideTagFilter
)
from topydo.lib.IcalPrinter import IcalPrinter
from topydo.lib.JsonPrinter import JsonPrinter

class ListCommand(ExpressionCommand):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(ListCommand, self).__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

        self.printer = None
        self.sort_expression = config().sort_string()
        self.show_all = False

    def _poke_icalendar(self):
        """
        Attempts to import the icalendar package. Returns True if it
        succeeds, otherwise False.

        Raises a SyntaxError when icalendar couldn't be imported (most likely
        under Python 3.2.
        """
        try:
            import icalendar as _
        except ImportError: # pragma: no cover
            self.error("icalendar package is not installed.")
            return False

        # may also raise SyntaxError, but we'll deal with that in execute()

        return True

    def _process_flags(self):
        opts, args = self.getopt('f:s:x')

        for opt, value in opts:
            if opt == '-x':
                self.show_all = True
            elif opt == '-s':
                self.sort_expression = value
            elif opt == '-f':
                if value == 'json':
                    self.printer = JsonPrinter()
                elif value == 'ical':
                    if self._poke_icalendar():
                        self.printer = IcalPrinter(self.todolist)
                else:
                    self.printer = None

        self.args = args

    def _print(self):
        """
        Prints the todos in the right format.

        Defaults to normal text output (with possible colors and other pretty
        printing. If a format was specified on the commandline, this format is
        sent to the output.
        """

        if self.printer == None:
            # create a standard printer with some filters
            indent = config().list_indent()
            hidden_tags = config().hidden_tags()

            filters = []
            filters.append(PrettyPrinterIndentFilter(indent))
            filters.append(PrettyPrinterHideTagFilter(hidden_tags))

            self.printer = pretty_printer_factory(self.todolist, filters)

        self.out(self.printer.print_list(self._view().todos))

    def execute(self):
        if not super(ListCommand, self).execute():
            return False

        try:
            self._process_flags()
        except SyntaxError: # pragma: no cover
            # importing icalendar failed, most likely due to Python 3.2
            self.error("icalendar is not supported in this Python version.")
            return False

        self._print()
        return True

    def usage(self):
        return """ Synopsis: ls [-x] [-s <sort_expression>] [-f <format>] [expression]"""

    def help(self):
        return """\
Lists all relevant todos. A todo is relevant when:

* has not been completed yet;
* the start date (if present) has passed;
* there are no subitems that need to be completed.

When an expression is given, only the todos matching that expression are shown.

-f : Specify the output format, being 'text' (default), 'ical' or 'json'.

     * 'text' - Text output with colors and identation if applicable.
     * 'ical' - iCalendar (RFC 2445). Is not supported in Python 3.2. Be aware
                that this is not a read-only operation, todo items may obtain
                an 'ical' tag with a unique ID. Completed todo items may be
                archived.
     * 'json' - Javascript Object Notation (JSON)
-s : Sort the list according to a sort expression. Defaults to the expression
     in the configuration.
-x : Show all todos (i.e. do not filter on dependencies or relevance).
"""
