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

from topydo.lib.Command import Command, InvalidCommandArgument
from topydo.lib.PrettyPrinter import pretty_print
from topydo.lib.TodoListBase import InvalidTodoException

class DepriCommand(Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(DepriCommand, self).__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

    def execute(self):
        if not super(DepriCommand, self).execute():
            return False

        todo = None
        try:
            todo = self.todolist.todo(self.argument(0))

            if todo.priority() != None:
                self.todolist.set_priority(todo, None)
                self.out("Priority removed.")
                self.out(pretty_print(todo))
        except InvalidCommandArgument:
            self.error(self.usage())
        except (InvalidTodoException):
            if not todo:
                self.error( "Invalid todo number given.")
            else:
                self.error(self.usage())

    def usage(self):
        return """Synopsis: depri <NUMBER>"""

    def help(self):
        return """Removes the priority of the given todo item."""
