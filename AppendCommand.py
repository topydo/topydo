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
from PrettyPrinter import pretty_print
import TodoList
from Utils import convert_todo_number, InvalidTodoNumberException

class AppendCommand(Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(AppendCommand, self).__init__(p_args, p_todolist, p_out, p_err, p_prompt=lambda a: None)

    def execute(self):
        try:
            number = convert_todo_number(self.argument(0))
            text = " ".join(self.args[1:])

            if text:
                todo = self.todolist.todo(number)
                self.todolist.append(todo, text)
                self.out(pretty_print(todo, [self.todolist.pp_number()]))
            else:
                self.error(self.usage())
        except (InvalidCommandArgument, InvalidTodoNumberException):
            self.error(self.usage())
        except TodoList.InvalidTodoException:
            self.error("Invalid todo number given.")

