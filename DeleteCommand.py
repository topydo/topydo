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
from TodoList import InvalidTodoException
from Utils import convert_todo_number, InvalidTodoNumberException

class DeleteCommand(Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(DeleteCommand, self).__init__(p_args, p_todolist, p_out, p_err, p_prompt)

        self.number = None

        try:
            self.number = convert_todo_number(self.argument(0))
            self.todo = self.todolist.todo(self.number)
        except (InvalidCommandArgument, InvalidTodoNumberException, InvalidTodoException):
            self.todo = None

    def execute(self):
        if not super(DeleteCommand, self).execute():
            return False

        if not self.number:
            self.error(self.usage())
        elif self.todo:
            self.todolist.delete(self.todo)
            self.out("Todo %d removed." % self.number)
        else:
            self.error("Invalid todo number given.")

    def usage(self):
        return """Synopsis: del <NUMBER>"""

    def help(self):
        return """Deletes the todo item with the given number from the list."""
