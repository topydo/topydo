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

from topydo.lib.Command import Command, InvalidCommandArgument
from topydo.lib.PrettyPrinter import pretty_print, pretty_print_list
from topydo.lib.TodoListBase import InvalidTodoException

class DCommand(Command):
    """
    A common class for the 'do' and 'del' operations, because they're quite
    alike.
    """

    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(DCommand, self).__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

        self.force = False

        self.process_flags()
        self.length = len(self.todolist.todos()) # to determine newly activated todos

        try:
            self.todo = self.todolist.todo(self.argument(0))
        except (InvalidCommandArgument, InvalidTodoException):
            self.todo = None

    def get_flags(self):
        """ Default implementation of getting specific flags. """
        return ("", [])

    def process_flag(self, p_option, p_value):
        """ Default implementation of processing specific flags. """
        pass

    def process_flags(self):
        opts, args = self.get_flags()
        opts, args = self.getopt("f" + opts, ["force"] + args)

        for opt, value in opts:
            if opt == "-f" or opt == "--force":
                self.force = True
            else:
                self.process_flag(opt, value)

        self.args = args

    def _uncompleted_children(self, p_todo):
        return sorted(
            [t for t in self.todolist.children(p_todo) if not t.is_completed()]
        )

    def _print_list(self, p_todos, p_print_numbers=True):
        filters = []

        if p_print_numbers:
            filters = [self.todolist.pp_number()]

        self.out("\n".join(pretty_print_list(p_todos, filters)))

    def prompt_text(self):
        return "Yes or no? [y/N] "

    def prefix(self):
        """ Prefix to use when printing a todo. """
        return ""

    def _process_subtasks(self):
        children = self._uncompleted_children(self.todo)
        if children:
            self._print_list(children)

            if not self.force:
                confirmation = self.prompt(self.prompt_text())

            if not self.force and re.match('^y(es)?$', confirmation, re.I):
                for child in children:
                    self.execute_specific_core(child)
                    self.out(self.prefix() + pretty_print(child))

    def _print_unlocked_todos(self, p_old, p_new):
        delta = [todo for todo in p_new if todo not in p_old]
        if delta:
            self.out("The following todo item(s) became active:")
            self._print_list(delta, False)

    def _active_todos(self):
        """
        Returns a list of active todos, taking uncompleted subtodos into
        account.

        The stored length of the todolist is taken into account, to prevent new
        todos created by recurrence to pop up as newly activated tasks.
        Since these todos pop up at the end of the list, we cut off the list
        just before that point.
        """
        return [todo for todo in self.todolist.todos()[:self.length]
            if not self._uncompleted_children(todo) and todo.is_active()]

    def condition(self):
        """
        An additional condition whether execute_specific should be executed.
        """
        return True

    def condition_failed_text(self):
        return ""

    def execute_specific(self):
        pass

    def execute_specific_core(self, p_todo):
        """
        The core operation on the todo itself. Also used to operate on
        child/parent tasks.
        """
        pass

    def execute(self):
        if not super(DCommand, self).execute():
            return False

        if len(self.args) == 0:
            self.error(self.usage())
        elif not self.todo:
            self.error("Invalid todo number given.")
        elif self.todo and self.condition():
            old_active = self._active_todos()
            self._process_subtasks()
            self.execute_specific()
            current_active = self._active_todos()
            self._print_unlocked_todos(old_active, current_active)
        else:
            self.error(self.condition_failed_text())

