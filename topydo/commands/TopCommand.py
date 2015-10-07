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
    PrettyPrinterHideTagFilter,
    PrettyPrinterBasicPriorityFilter,
    PrettyPrinterHumanDatesFilter
)

try:
    from shutil import get_terminal_size
except ImportError:
    from backports.shutil_get_terminal_size import get_terminal_size


class TopCommand(ExpressionCommand):

    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(TopCommand, self).__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

        self.printer = None
        self.sort_expression = config().sort_string()
        self.show_all = False

    def _process_flags(self):
        opts, args = self.getopt('s:x')

        for opt, value in opts:
            if opt == '-x':
                self.show_all = True
            elif opt == '-s':
                self.sort_expression = value

        self.args = args

    def _print(self):
        """
        Prints the todos in the right format.

        Supplies normal text output (with possible colors and other pretty
        printing), only one line per item, and only as many items as will
        fit in one console 'screen'.
        """

        if self.printer is None:
            # create a standard printer with some filters
            indent = config().list_indent()
            hidden_tags = config().hidden_tags()

            filters = []
            filters.append(PrettyPrinterHideTagFilter(hidden_tags))
            filters.append(PrettyPrinterBasicPriorityFilter())
            filters.append(PrettyPrinterHumanDatesFilter())
            # run indent after rearranging the text, but before adding colours
            filters.append(PrettyPrinterIndentFilter(indent, 1))  # only one line per item

            self.printer = pretty_printer_factory(self.todolist, filters)

        #  only print as many lines as are on the terminal
        #  leave three blank lines to accomadate the new following terminal prompt
        self.out(self.printer.print_list(self._view().todos[:get_terminal_size().lines - 3]))

    def execute(self):
        if not super(TopCommand, self).execute():
            return False

        self._process_flags()

        self._print()
        return True

    def usage(self):
        return """ Synopsis: top [-x] [-s <sort_expression>] [expression]"""

    def help(self):
        return """\
Lists one screen of the most relevant todos. A todo is relevant when:

* has not been completed yet;
* the start date (if present) has passed;
* there are no subitems that need to be completed.

When an expression is given, only the todos matching that expression are shown.

-s : Sort the list according to a sort expression. Defaults to the expression
     in the configuration.
-x : Show all todos (i.e. do not filter on dependencies or relevance).
"""
