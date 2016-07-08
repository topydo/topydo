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

from topydo.lib.ExpressionCommand import ExpressionCommand
from topydo.lib.TodoListBase import InvalidTodoException


class MultiCommand(ExpressionCommand):
    """
    A common class for operations that can work with multiple todo IDs.
    """

    def __init__(self, p_args, p_todolist, #pragma: no branch
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super().__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

        self.todos = []
        self.invalid_numbers = []
        self.is_expression = False
        self.multi_mode = True

    def get_flags(self):
        """ Default implementation of getting specific flags. """
        return ("", [])

    def process_flag(self, p_option, p_value):
        """ Default implementation of processing specific flags. """
        raise NotImplementedError

    def _process_flags(self):
        opts, long_opts = self.get_flags()
        opts, args = self.getopt("xe" + opts, long_opts)

        for opt, value in opts:
            if opt == '-x':
                self.show_all = True
            elif opt == '-e':
                self.is_expression = True
            else:
                self.process_flag(opt, value)

        self.args = args

    def get_todos_from_expr(self):
        self.todos = self._view().todos

    def get_todos(self):
        """ Gets todo objects from supplied todo IDs. """
        if self.is_expression:
            self.get_todos_from_expr()
        else:
            if self.last_argument:
                numbers = self.args[:-1]
            else:
                numbers = self.args

            for number in numbers:
                try:
                    self.todos.append(self.todolist.todo(number))
                except InvalidTodoException:
                    self.invalid_numbers.append(number)

    def _catch_todo_errors(self):
        """
        Returns None or list of error messages depending on number of valid
        todo objects and number of invalid todo IDs.

        In case of multiple invalid todo IDs we generate separate error message
        for each one of them with information about supplied ID.
        """
        errors = []

        if len(self.invalid_numbers) > 1 or len(self.invalid_numbers) > 0 and len(self.todos) > 0:
            for number in self.invalid_numbers:
                errors.append(u"Invalid todo number given: {}.".format(number))
        elif len(self.invalid_numbers) == 1 and len(self.todos) == 0:
            errors.append("Invalid todo number given.")
        elif len(self.todos) == 0 and len(self.invalid_numbers) == 0:
            errors.append(self.usage())

        if len(errors) > 0:
            return errors
        else:
            return None

    def _execute_multi_specific(self):
        """
        Operations specific for particular command dealing with multiple todo
        IDs.
        """
        raise NotImplementedError

    def _execute_not_multi(self):
        """
        Some commands can do something else besides operating on multiple todo
        IDs. This method is a wrapper for those other operations.
        """
        raise NotImplementedError

    def execute(self):
        if not super().execute():
            return False

        self._process_flags()

        if not self.multi_mode:
            self._execute_not_multi()
        else:
            self.get_todos()
            todo_errors = self._catch_todo_errors()

            if not todo_errors:
                self._execute_multi_specific()
            else:
                for error in todo_errors:
                    self.error(error)

        return True
