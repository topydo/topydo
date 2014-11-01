# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 Bram Schoenmakers <me@bramschoenmakers.nl>
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

from DCommand import DCommand
from PrettyPrinter import pretty_print
from Recurrence import advance_recurring_todo

class DoCommand(DCommand):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(DoCommand, self).__init__(p_args, p_todolist, p_out, p_err, p_prompt)

    def _handle_recurrence(self):
        if self.todo.has_tag('rec'):
            new_todo = advance_recurring_todo(self.todo)
            self.todolist.add_todo(new_todo)
            self.out(pretty_print(new_todo, [self.todolist.pp_number()]))

    def prompt_text(self):
        return "Also mark subtasks as done? [n] "

    def prefix(self):
        return "Completed: "

    def condition(self):
        """ An additional condition whether execute_specific should be executed. """
        return not self.todo.is_completed()

    def conditionFailedText(self):
        return "Todo has already been completed."

    def execute_specific(self):
        """ Actions specific to this command. """
        self._handle_recurrence()
        self.execute_specific_core(self.todo)
        self.out(self.prefix() + pretty_print(self.todo))

    def execute_specific_core(self, p_todo):
        """
        The core operation on the todo itself. Also used to operate on
        child/parent tasks.
        """
        self.todolist.set_todo_completed(p_todo)

    def usage(self):
        return """Synopsis: do [--force] <NUMBER>"""

    def help(self):
        return """Marks the todo with given number as complete.

In case the todo has subitems, a question is asked whether the subitems should
be marked as completed as well. When --force is given, no interaction is
required and the subitems are not marked completed.

In case the completed todo is recurring, a new todo will be added to the list,
while the given todo item is marked as complete."""
