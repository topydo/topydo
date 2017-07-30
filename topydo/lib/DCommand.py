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

from topydo.lib.MultiCommand import MultiCommand
from topydo.lib.prettyprinters.Numbers import PrettyPrinterNumbers
from topydo.lib.printers.PrettyPrinter import PrettyPrinter


class DCommand(MultiCommand):
    """
    A common class for the 'do' and 'del' operations, because they're quite
    alike.
    """

    def __init__(self, p_args, p_todolist, #pragma: no branch
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super().__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

        self.force = False
        self._delta = []
        self.condition = lambda _: True
        self.condition_failed_text = ""

    def get_flags(self):
        return ("f", ["force"])

    def process_flag(self, p_option, p_value):
        if p_option == "-f" or p_option == "--force":
            self.force = True

    def _uncompleted_children(self, p_todo):
        return sorted(
            [t for t in self.todolist.children(p_todo) if not t.is_completed()],
            key=self.todolist.number
        )

    def _print_list(self, p_todos):
        printer = PrettyPrinter()
        printer.add_filter(PrettyPrinterNumbers(self.todolist))
        self.out(printer.print_list(p_todos))

    def prompt_text(self):
        raise NotImplementedError

    def prefix(self):
        raise NotImplementedError

    def _process_subtasks(self, p_todo):
        children = self._uncompleted_children(p_todo)
        if children:
            self._print_list(children)

            if not self.force:
                confirmation = self.prompt(self.prompt_text())

            if not self.force and re.match('^y(es)?$', confirmation, re.I):
                for child in children:
                    self.execute_specific_core(child)
                    self.out(self.prefix() + self.printer.print_todo(child))

    def _print_unlocked_todos(self):
        if self._delta:
            self.out("The following todo item(s) became active:")
            self._print_list(self._delta)

    def _active_todos(self):
        """
        Returns a list of active todos, taking uncompleted subtodos into
        account.

        The stored length of the todolist is taken into account, to prevent new
        todos created by recurrence to pop up as newly activated tasks.
        Since these todos pop up at the end of the list, we cut off the list
        just before that point.
        """
        return [todo for todo in self.todolist.todos()
                if not self._uncompleted_children(todo) and todo.is_active()]

    def execute_specific(self, _):
        raise NotImplementedError

    def execute_specific_core(self, p_todo):
        """
        The core operation on the todo itself. Also used to operate on
        child/parent tasks.
        """
        raise NotImplementedError

    def _execute_multi_specific(self):
        old_active = self._active_todos()

        for todo in self.todos:
            if todo and self.condition(todo):
                self._process_subtasks(todo)
                self.execute_specific(todo)
            else:
                self.error(self.condition_failed_text)

        current_active = self._active_todos()
        self._delta = [todo for todo in current_active
                       if todo not in old_active]

    def execute_post_archive_actions(self):
        self._print_unlocked_todos()
