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

from topydo.lib.Command import Command
from topydo.lib.TodoListBase import InvalidTodoException

class MultiCommand(Command):
    """
    A common class for operations that can work with multiple todo IDs.
    """

    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(MultiCommand, self).__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

        self.todos = []
        self.invalid_numbers = []

    def get_todos(self, p_numbers):
        """ Gets todo objects from supplied todo IDs """
        for number in p_numbers:
            try:
                self.todos.append(self.todolist.todo(number))
            except InvalidTodoException:
                self.invalid_numbers.append(number)

    def _catch_todo_errors(self):
        """
        Returns None or list of error messages depending on number of valid todo
        objects and number of invalid todo IDs.

        In case of multiple invalid todo IDs we generate separate error message for each
        one of them with information about supplied ID.
        """
        errors = []

        if len(self.invalid_numbers) > 1 or len(self.invalid_numbers) > 0 and len(self.todos) > 0:
            for number in self.invalid_numbers:
                errors.append("Invalid todo number given: {}.".format(number))
        elif len(self.invalid_numbers) == 1 and len(self.todos) == 0:
            errors.append("Invalid todo number given.")
        elif len(self.todos) == 0 and len(self.invalid_numbers) == 0:
            errors.append(self.usage())

        if len(errors) > 0:
            return errors
        else:
            return None

    def execute_multi_specific(self):
        """
        Operations specific for particular command dealing with multiple todo
        IDs.
        """
        pass

    def execute(self):
        if not super(MultiCommand, self).execute():
            return False

        todo_errors = self._catch_todo_errors()

        if not todo_errors:
            self.execute_multi_specific()
        else:
            for error in todo_errors:
                self.error(error)

        return True
