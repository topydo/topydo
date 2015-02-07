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

        numbers = None
        priority = None
        try:
            numbers = self.args[:-1]
            priority = self.args[-1]

            if len(numbers) > 0:
                todos = []
                for number in numbers:
                    todos.append(self.todolist.todo(number))

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
        except IndexError:
            self.error(self.usage())
        except InvalidCommandArgument:
            self.error(self.usage())
        except (InvalidTodoException):
            if len(numbers) > 0 and priority:
                self.error( "Invalid todo number given.")
            else:
                self.error(self.usage())

    def usage(self):
        return """Synopsis: pri <NUMBER> <PRIORITY>"""

    def help(self):
        return """\
Sets the priority of todo the given number to the given priority.
"""
