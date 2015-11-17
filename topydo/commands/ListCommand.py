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

from topydo.lib.Config import config
from topydo.lib.ExpressionCommand import ExpressionCommand
from topydo.lib.Filter import InstanceFilter
from topydo.lib.PrettyPrinter import pretty_printer_factory
from topydo.lib.prettyprinters.Format import PrettyPrinterFormatFilter
from topydo.lib.TodoListBase import InvalidTodoException


class ListCommand(ExpressionCommand):
    def __init__(self, p_args, p_todolist, #pragma: no branch
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(ListCommand, self).__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

        self.printer = None
        self.sort_expression = config().sort_string()
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
        opts, args = self.getopt('f:F:i:n:s:x')

        for opt, value in opts:
            if opt == '-x':
                self.show_all = True
            elif opt == '-s':
                self.sort_expression = value
            elif opt == '-f':
                if value == 'json':
                    from topydo.lib.JsonPrinter import JsonPrinter
                    self.printer = JsonPrinter()
                elif value == 'ical':
                    if self._poke_icalendar():
                        from topydo.lib.IcalPrinter import IcalPrinter
                        self.printer = IcalPrinter(self.todolist)
                else:
                    self.printer = None
            elif opt == '-F':
                self.format = value
            elif opt == '-n':
                try:
                    self.limit = int(value)
                except ValueError:
                    pass # use default value in configuration
            elif opt == '-i':
                self.ids = value.split(',')

                # when a user requests a specific ID, it should always be shown
                self.show_all = True

        self.args = args

    def _filters(self):
        """
        Additional filters to select particular todo items given with the -i
        flag.
        """
        filters = super(ListCommand, self)._filters()

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
            hidden_tags = config().hidden_tags()

            filters = []
            filters.append(PrettyPrinterFormatFilter(self.todolist, final_format))

            self.printer = pretty_printer_factory(self.todolist, filters)

        self.out(self.printer.print_list(self._view().todos))

    def execute(self):
        if not super(ListCommand, self).execute():
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
        return """Synopsis: ls [-x] [-s <sort_expression>] [-f <output format>]
[-F <format string>] [expression]"""

    def help(self):
        return """\
Lists all relevant todos. A todo is relevant when:

* has not been completed yet;
* the start date (if present) has passed;
* there are no subitems that need to be completed.

When an expression is given, only the todos matching that expression are shown.

-f : Specify the output format, being 'text' (default), 'ical' or 'json'.

     * 'text' - Text output with colors and indentation if applicable.
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
         %s: Todo text.
         %S: Todo text, truncated such that an item fits on one line.
         %t: Absolute creation date.
         %T: Relative creation date.
         %x: 'x' followed by absolute completion date.
         %X: 'x' followed by relative completion date.
         \%: Literal percent sign.

     Conditional characters can be added with blocks surrounded by curly
     braces, they will only appear when a placeholder expanded to a value.

     E.g. %{(}p{)} will print (C) when the todo item has priority C, or ''
     (empty string) when an item has no priority set.

     A tab character serves as a marker to start right alignment.
-i : Comma separated list of todo IDs to print.
-s : Sort the list according to a sort expression. Defaults to the expression
     in the configuration.
-x : Show all todos (i.e. do not filter on dependencies or relevance).
"""
