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

from datetime import timedelta

from topydo.lib.Config import config
from topydo.lib.MultiCommand import MultiCommand
from topydo.lib.prettyprinters.Numbers import PrettyPrinterNumbers
from topydo.lib.RelativeDate import relative_date_to_date
from topydo.lib.Time import today
from topydo.lib.Utils import date_string_to_date


class PostponeCommand(MultiCommand):
    def __init__(self, p_args, p_todolist, #pragma: no branch
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super().__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

        self.move_start_date = False
        self.last_argument = True

    def get_flags(self):
        return("s", [])

    def process_flag(self, p_option, p_value):
        if p_option == '-s':
            self.move_start_date = True

    def _execute_multi_specific(self):
        def _get_offset(p_todo):
            offset = p_todo.tag_value(
                config().tag_due(), today().isoformat())

            offset_date = date_string_to_date(offset)

            if offset_date < today():
                offset_date = today()

            return offset_date

        pattern = self.args[-1]
        self.printer.add_filter(PrettyPrinterNumbers(self.todolist))

        for todo in self.todos:
            try:
                offset = _get_offset(todo)
            except ValueError:
                self.error("Postponing todo item failed: invalid due date.")
                break

            new_due = relative_date_to_date(pattern, offset)

            if new_due:
                if self.move_start_date and todo.start_date():
                    length = todo.length()
                    new_start = new_due - timedelta(length)
                    # pylint: disable=E1103
                    todo.set_tag(config().tag_start(), new_start.isoformat())
                elif self.move_start_date and not todo.start_date():
                    self.error("Warning: todo item has no (valid) start date, therefore it was not adjusted.")

                # pylint: disable=E1103
                todo.set_tag(config().tag_due(), new_due.isoformat())

                self.todolist.dirty = True
                self.out(self.printer.print_todo(todo))
            else:
                self.error("Invalid date pattern given.")
                break

    def usage(self):
        return """\
Synopsis: postpone [-s] <NUMBER> [<NUMBER2> ...] <PATTERN>
          postpone [-x] -e <EXPRESSION>\
"""

    def help(self):
        return """\
Postpone the todo item(s) with the given NUMBER(s) and the given PATTERN.

Postponing is done by adjusting the due date(s) of the todo(s), and if the -s
flag is given, the start date accordingly.

It is also possible to postpone items as complete with an EXPRESSION using
the -e flag. Use -x to also process todo items that are normally invisible (as
with the 'ls' subcommand).

The PATTERN is a relative date, written in the format <COUNT> <PERIOD> where
COUNT is a number and PERIOD is either 'd', 'w', 'm' or 'y', which stands for
days, weeks, months and years respectively. Example: 'postpone 1 2w' postpones
todo number 1 for 2 weeks.\
"""
