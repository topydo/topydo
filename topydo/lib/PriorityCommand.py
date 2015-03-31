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

from topydo.lib.Command import Command, InvalidCommandArgument
from topydo.lib.PrettyPrinterFilter import PrettyPrinterNumbers
from topydo.lib.TodoListBase import InvalidTodoException
from topydo.lib.Utils import is_valid_priority

class PriorityCommand(Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(PriorityCommand, self).__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

    def execute(self):
        if not super(PriorityCommand, self).execute():
            return False

        priority = None
        todos = []
        invalid_numbers = []

        for number in self.args[:-1]:
            try:
                todos.append(self.todolist.todo(number))
            except InvalidTodoException:
                invalid_numbers.append(number)

        if len(invalid_numbers) > 1 or len(invalid_numbers) > 0 and len(todos) > 0:
            for number in invalid_numbers:
                self.error("Invalid todo number given: {}.".format(number))
        elif len(invalid_numbers) == 1 and len(todos) == 0:
            self.error("Invalid todo number given.")
        else:
            try:
                priority = self.args[-1]
                self.printer.add_filter(PrettyPrinterNumbers(self.todolist))

                if len(todos) > 0:
                    if is_valid_priority(priority):
                        for todo in todos:
                            old_priority = todo.priority()
                            self.todolist.set_priority(todo, priority)

                            if old_priority and priority and old_priority != priority:
                                self.out("Priority changed from {} to {}".format(
                                    old_priority, priority))
                            elif not old_priority:
                                self.out("Priority set to {}.".format(priority))

                            self.out(self.printer.print_todo(todo))
                    else:
                        self.error("Invalid priority given.")
                else:
                    self.error(self.usage())
            except (IndexError, InvalidCommandArgument):
                self.error(self.usage())

    def usage(self):
        return """Synopsis: pri <NUMBER1> [<NUMBER2> ...] <PRIORITY>"""

    def help(self):
        return """\
Sets the priority of todo(s) the given number(s) to the given priority.
"""
