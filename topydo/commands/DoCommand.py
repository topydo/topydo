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

from datetime import date

from topydo.lib.DCommand import DCommand
from topydo.lib.PrettyPrinter import PrettyPrinter
from topydo.lib.PrettyPrinterFilter import PrettyPrinterNumbers
from topydo.lib.Recurrence import advance_recurring_todo, strict_advance_recurring_todo, NoRecurrenceException
from topydo.lib.Utils import date_string_to_date

class DoCommand(DCommand):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):

        self.strict_recurrence = False
        self.completion_date = date.today()

        super(DoCommand, self).__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

    def get_flags(self):
        """ Additional flags. """
        opts, long_opts = super(DoCommand, self).get_flags()

        return ("d:s" + opts, ["date=", "strict"] + long_opts)

    def process_flag(self, p_opt, p_value):
        super(DoCommand, self).process_flag(p_opt, p_value)

        if p_opt == "-s" or p_opt == "--strict":
            self.strict_recurrence = True
        elif p_opt == "-d" or p_opt == "--date":
            try:
                self.completion_date = date_string_to_date(p_value)
            except ValueError:
                self.completion_date = date.today()

    def _handle_recurrence(self, p_todo):
        if p_todo.has_tag('rec'):
            try:
                if self.strict_recurrence:
                    new_todo = strict_advance_recurring_todo(p_todo,
                        self.completion_date)
                else:
                    new_todo = advance_recurring_todo(p_todo,
                        self.completion_date)

                self.todolist.add_todo(new_todo)

                printer = PrettyPrinter()
                printer.add_filter(PrettyPrinterNumbers(self.todolist))
                self.out(printer.print_todo(new_todo))
            except NoRecurrenceException:
                self.error("Warning: todo item has an invalid recurrence pattern.")

    def prompt_text(self):
        return "Also mark subtasks as done? [y/N] "

    def prefix(self):
        return "Completed: "

    def condition(self, p_todo):
        """
        An additional condition whether execute_specific should be executed.
        """
        return not p_todo.is_completed()

    def condition_failed_text(self):
        return "Todo has already been completed."

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
        return """Synopsis: do [--date] [--force] [--strict] <NUMBER1> [<NUMBER2> ...]"""

    def help(self):
        return """Marks the todo(s) with given number(s) as complete.

In case a todo has subitems, a question is asked whether the subitems should be
marked as completed as well. When --force is given, no interaction is required
and the subitems are not marked completed.

In case a completed todo is recurring, a new todo will be added to the list,
while the given todo item is marked as complete. The new date is calculated
based on the todo item's due date. If the due date is in the past, today's date
is used to calculate the new recurrence date. Using --strict prevents this,
then the actual due date of the todo item is used to calculate the new
recurrence date. Note that a future due date is always used as such to
calculate the new due date.

Use --date to set a custom completion date.
"""
