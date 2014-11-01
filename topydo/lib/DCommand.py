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

from Command import *
from PrettyPrinter import *
from TodoList import InvalidTodoException
from Utils import convert_todo_number, InvalidTodoNumberException

class DCommand(Command):
    """
    A common class for the 'do' and 'del' operations, because they're quite
    alike.
    """

    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(DCommand, self).__init__(p_args, p_todolist, p_out, p_err, p_prompt)

        self.number = None
        self.force = self.argument_shift("--force") or self.argument_shift("-f")

        try:
            self.number = convert_todo_number(self.argument(0))
            self.todo = self.todolist.todo(self.number)
        except (InvalidCommandArgument, InvalidTodoNumberException, InvalidTodoException):
            self.todo = None

    def _uncompleted_children(self, p_todo):
        return sorted([t for t in self.todolist.children(p_todo) if not t.is_completed()])

    def _print_list(self, p_todos, p_print_numbers=True):
        filters = []

        if p_print_numbers:
            filters = [self.todolist.pp_number()]

        self.out("\n".join(pretty_print_list(p_todos, filters)))

    def prompt_text(self):
        return "Yes or no? [n] "

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

    def _print_unlocked_todos(self):
        """
        Print the items that became unlocked by marking this subitem
        (self.todo) as complete.
        """
        parents = [parent for parent in self.todolist.parents(self.todo) if not self._uncompleted_children(parent) and parent.is_active()]

        if parents:
            self.out("The following todo item(s) became active:")
            self._print_list(parents, False)

    def condition(self):
        """ An additional condition whether execute_specific should be executed. """
        return True

    def conditionFailedText(self):
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

        if not self.number:
            self.error(self.usage())
        elif self.todo and self.condition():
            self._process_subtasks()
            self.execute_specific()
            self._print_unlocked_todos()
        elif not self.todo:
            self.error("Invalid todo number given.")
        else:
            self.error(self.conditionFailedText())

