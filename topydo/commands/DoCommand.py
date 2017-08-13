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

from datetime import date

from topydo.lib.DCommand import DCommand
from topydo.lib.printers.PrettyPrinter import PrettyPrinter
from topydo.lib.Recurrence import NoRecurrenceException, advance_recurring_todo
from topydo.lib.RelativeDate import relative_date_to_date
from topydo.lib.Utils import date_string_to_date


class DoCommand(DCommand):
    def __init__(self, p_args, p_todolist, #pragma: no branch
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):

        self.strict_recurrence = False
        self.completion_date = date.today()

        super().__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

        self.condition = lambda todo: not todo.is_completed()
        self.condition_failed_text = "Todo has already been completed."

    def get_flags(self):
        """ Additional flags. """
        opts, long_opts = super().get_flags()

        return ("d:s" + opts, ["date=", "strict"] + long_opts)

    def process_flag(self, p_opt, p_value):
        super().process_flag(p_opt, p_value)

        if p_opt == "-s" or p_opt == "--strict":
            self.strict_recurrence = True
        elif p_opt == "-d" or p_opt == "--date":
            try:
                self.completion_date = relative_date_to_date(p_value)

                if not self.completion_date:
                    self.completion_date = date_string_to_date(p_value)
            except ValueError:
                self.completion_date = date.today()

    def _handle_recurrence(self, p_todo):
        if p_todo.has_tag('rec'):
            try:
                new_todo = advance_recurring_todo(
                    p_todo,
                    p_offset=self.completion_date,
                    p_strict=self.strict_recurrence
                )

                self.todolist.add_todo(new_todo)

            except NoRecurrenceException:
                self.error("Warning: todo item has an invalid recurrence pattern.")

    def prompt_text(self):
        return "Also mark subtasks as done? [y/N] "

    def prefix(self):
        return "Completed: "

    def execute_specific(self, p_todo):
        """ Actions specific to this command. """
        self._handle_recurrence(p_todo)
        self.execute_specific_core(p_todo)

        printer = PrettyPrinter()
        self.out(self.prefix() + printer.print_todo(p_todo))

    def execute_specific_core(self, p_todo):
        """
        The core operation on the todo itself. Also used to operate on
        child/parent tasks.
        """
        self.todolist.set_todo_completed(p_todo, self.completion_date)

    def usage(self):
        return """\
Synopsis: do [--date <DATE>] [--force] [--strict] <NUMBER 1> [<NUMBER 2> ...]
          do [-x] -e <EXPRESSION>\
"""

    def help(self):
        return """Marks the todo(s) with given NUMBER(s) as complete.

It is also possible to mark todo items as complete with an EXPRESSION using the
-e flag. Use -x to also process todo items that are normally invisible (as with
the 'ls' subcommand).

In case a todo has subitems (dependencies), a question is asked whether the
subitems should be marked as completed as well. When --force is given, no
interaction is required and the subitems are not marked completed.

In case a completed todo is recurring, a new todo will be added to the list,
while the given todo item is marked as complete. The new date is calculated
based on the todo item's due date. If the due date is in the past, today's date
is used to calculate the new recurrence date. Using --strict prevents this, and
then the actual due date of the todo item is used to calculate the new
recurrence date. Note that a future due date is always used as such to
calculate the new due date.

Use --date to set a custom completion date.\
"""
