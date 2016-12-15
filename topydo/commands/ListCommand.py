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

import re
import sys
import os

from topydo.lib.Config import config
from topydo.lib.ExpressionCommand import ExpressionCommand
from topydo.lib.Filter import HiddenTagFilter, InstanceFilter
from topydo.lib.printers.PrettyPrinter import pretty_printer_factory
from topydo.lib.prettyprinters.Format import PrettyPrinterFormatFilter
from topydo.lib.TodoListBase import InvalidTodoException
from topydo.lib.Sorter import Sorter
from topydo.lib.Utils import get_terminal_size
from topydo.lib.View import View


class ListCommand(ExpressionCommand):
    def __init__(self, p_args, p_todolist, #pragma: no branch
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super().__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

        self.printer = None
        self.sort_expression = config().sort_string()
        self.group_expression = config().group_string()
        self.show_all = False
        self.ids = None
        self.format = config().list_format()

    def _poke_icalendar(self):
        """
        Attempts to import the icalendar package. Returns True if it
        succeeds, otherwise False.
        """
        try:
            import icalendar as _
        except ImportError:  # pragma: no cover
            self.error("icalendar package is not installed.")
            return False

        return True

    def _process_flags(self):
        opts, args = self.getopt('f:F:g:i:n:Ns:x')

        for opt, value in opts:
            if opt == '-x':
                self.show_all = True
            elif opt == '-s':
                self.sort_expression = value
            elif opt == '-f':
                if value == 'json':
                    from topydo.lib.printers.Json import JsonPrinter
                    self.printer = JsonPrinter()
                elif value == 'ical':
                    if self._poke_icalendar():
                        from topydo.lib.printers.Ical import IcalPrinter
                        self.printer = IcalPrinter(self.todolist)
                elif value == 'dot':
                    from topydo.lib.printers.Dot import DotPrinter
                    self.printer = DotPrinter(self.todolist)

                    # a graph without dependencies is not so useful, hence
                    # show all
                    self.show_all = True
                else:
                    self.printer = None
            elif opt == '-F':
                self.format = value
            elif opt == '-g':
                self.group_expression = value
            elif opt == '-N':
                # 2 lines are assumed to be taken up by printing the next prompt
                # display at least one item
                self.limit = self._N_lines()
            elif opt == '-n':
                try:
                    self.limit = int(value)
                except ValueError:
                    pass  # use default value in configuration
            elif opt == '-i':
                self.ids = value.split(',')

                # when a user requests a specific ID, it should always be shown
                self.show_all = True

        self.args = args

    def _filters(self):
        """
        Additional filters to:
            - select particular todo items given with the -i flag,
            - hide appropriately tagged items in the absense of the -x flag.
        """
        filters = super()._filters()

        if self.ids:
            def get_todo(p_id):
                """
                Safely obtains a todo item given the user-supplied ID.
                Returns None if an invalid ID was entered.
                """
                try:
                    return self.todolist.todo(p_id)
                except InvalidTodoException:
                    return None

            todos = [get_todo(i) for i in self.ids]
            filters.append(InstanceFilter(todos))

        if not self.show_all:
            filters.append(HiddenTagFilter())

        return filters

    def _print(self):
        """
        Prints the todos in the right format.

        Defaults to normal text output (with possible colors and other pretty
        printing). If a format was specified on the commandline, this format is
        sent to the output.
        """
        if self.printer is None:
            # create a standard printer with some filters
            indent = config().list_indent()
            final_format = ' ' * indent + self.format

            filters = []
            filters.append(PrettyPrinterFormatFilter(self.todolist, final_format))

            self.printer = pretty_printer_factory(self.todolist, filters)

        if self.group_expression:
            self.out(self.printer.print_groups(self._view().groups))
        else:
            self.out(self.printer.print_list(self._view().todos))

    def _view(self):
        sorter = Sorter(self.sort_expression, self.group_expression)
        filters = self._filters()

        return View(sorter, filters, self.todolist)

    def _N_lines(self):
        ''' Determine how many lines to print, such that the number of items
            displayed will fit on the terminal (i.e one 'screen-ful' of items)

            This looks at the environmental prompt variable, and tries to determine
            how many lines it takes up.

            On Windows, it does this by looking for the '$_' sequence, which indicates
            a new line, in the environmental variable PROMPT.

            Otherwise, it looks for a newline ('\n') in the environmental variable
            PS1.
        '''  
        lines_in_prompt = 1     # prompt is assumed to take up one line, even
                                #   without any newlines in it
        if "win32" in sys.platform:
            lines_in_prompt += 1  # Windows will typically print a free line after
                                  #   the program output
            a = re.findall('\$_', os.getenv('PROMPT', ''))
            lines_in_prompt += len(a)
        else:
            a = re.findall('\\n', os.getenv('PS1', ''))
            lines_in_prompt += len(a)
        n_lines = get_terminal_size().lines - lines_in_prompt

        # print a minimum of one item
        n_lines = max(n_lines, 1)

        return n_lines

    def execute(self):
        if not super().execute():
            return False

        try:
            self._process_flags()
        except SyntaxError:  # pragma: no cover
            # importing icalendar failed, most likely due to Python 3.2
            self.error("icalendar is not supported in this Python version.")
            return False

        self._print()
        return True

    def usage(self):
        return """Synopsis: ls [-x] [-s <SORT EXPRESSION>]
[-g <GROUP EXPRESSION>] [-f <OUTPUT FORMAT>] [-F <FORMAT STRING>]
[-i <NUMBER 1>[,<NUMBER 2> ...]] [-N | -n <INTEGER>] [EXPRESSION]"""

    def help(self):
        return """\
Lists all relevant todos. A todo is relevant when:

* has not been completed yet,
* the start date (if present) has passed, and
* there are no subitems that need to be completed.

When an EXPRESSION is given, only the todos matching that EXPRESSION are shown.

-f : Specify the OUTPUT format, being 'text' (default), 'dot' or 'ical' or
     'json'.

     * 'text' - Text output with colors and indentation if applicable.
     * 'dot'  - Prints a dependency graph for the selected items in GraphViz
                Dot format.
     * 'ical' - iCalendar (RFC 2445). Is not supported in Python 3.2. Be aware
                that this is not a read-only operation, todo items may obtain
                an 'ical' tag with a unique ID. Completed todo items may be
                archived.
     * 'json' - Javascript Object Notation (JSON)

-F : Specify the format of the text ('text' format), which may contain
     placeholders that may be expanded if the todo has such attribute. If such
     attribute does not exist, then it expands to an empty string.

         %c: Absolute creation date.
         %C: Relative creation date.
         %d: Absolute due date.
         %D: Relative due date.
         %h: Relative due and start date (due in 3 days, started 3 days ago)
         %H: Like %h with creation date.
         %i: Todo number.
         %I: Todo number padded with spaces (always 3 characters wide).
         %k: List of tags separated by spaces (excluding hidden tags).
         %K: List of all tags separated by spaces.
         %p: Priority.
         %P: Priority or placeholder space if no priority.
         %s: Todo text.
         %S: Todo text, truncated such that an item fits on one line.
         %t: Absolute creation date.
         %T: Relative creation date.
         %x: 'x' followed by absolute completion date.
         %X: 'x' followed by relative completion date.
         \%: Literal percent sign.

     Conditional characters can be added with blocks surrounded by curly
     braces, they will only appear when a placeholder expanded to a value.

     E.g. %{(}p{)} will print '(C)' when the todo item has priority C, or ''
     (empty string) when an item has no priority set.

     A tab character serves as a marker to start right alignment.
-g : Group items according to a GROUP EXPRESSION. A group expression is similar
     to a sort expression. Defaults to the group expression in the
     configuration.
-i : Comma separated list of todo IDs to print.
-n : Number of items to display. Defaults to the value in the configuration.
-N : Limit number of items displayed such that they fit on the terminal.
-s : Sort the list according to a SORT EXPRESSION. Defaults to the sort
     expression in the configuration.
-x : Show all todos (i.e. do not filter on dependencies, relevance, or hidden
     status).\
"""
