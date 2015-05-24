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

import os
from subprocess import call, check_call, CalledProcessError
import tempfile

from topydo.lib.ExpressionCommand import ExpressionCommand
from topydo.lib.MultiCommand import MultiCommand
from topydo.lib.Config import config
from topydo.lib.Todo import Todo
from topydo.lib.TodoListBase import InvalidTodoException
from topydo.lib.TodoList import TodoList
from topydo.lib.PrettyPrinterFilter import PrettyPrinterNumbers

# Access the base class of the TodoList instance kept inside EditCommand. We
# cannot use super() inside the class itself
BASE_TODOLIST = lambda tl: super(TodoList, tl)

class EditCommand(MultiCommand, ExpressionCommand):
    def __init__(self, p_args, p_todolist, p_output, p_error, p_input):
        super(EditCommand, self).__init__(p_args, p_todolist, p_output,
            p_error, p_input)

        self.is_expression = False
        self.edit_archive = False

    def _process_flags(self):
        opts, args = self.getopt('xed')

        for opt, value in opts:
            if opt == '-d':
                self.edit_archive = True
            elif opt == '-x':
                self.show_all = True
            elif opt == '-e':
                self.is_expression = True

        self.args = args

    def _todos_to_temp(self):
        f = tempfile.NamedTemporaryFile()
        for todo in self.todos:
            f.write("%s\n" % todo.__str__())
        f.seek(0)

        return f

    def _todos_from_temp(self, temp_file):
        temp_file.seek(0)
        todos = temp_file.read().splitlines()

        todo_objs = []
        for todo in todos:
            todo_objs.append(Todo(todo))

        return todo_objs

    def _open_in_editor(self, temp_file, editor):
        try:
            return check_call([editor, temp_file.name])
        except(CalledProcessError):
            self.error('Something went wrong in the editor...')
            return 1

    def _catch_todo_errors(self):
        errors = []

        if len(self.invalid_numbers) > 1 or len(self.invalid_numbers) > 0 and len(self.todos) > 0:
            for number in self.invalid_numbers:
                errors.append("Invalid todo number given: {}.".format(number))
        elif len(self.invalid_numbers) == 1 and len(self.todos) == 0:
            errors.append("Invalid todo number given.")

        if len(errors) > 0:
            return errors
        else:
            return None

    def execute(self):
        if not super(EditCommand, self).execute():
            return False

        self.printer.add_filter(PrettyPrinterNumbers(self.todolist))
        try:
            editor = os.environ['EDITOR'] or 'vi'
        except(KeyError):
            editor =  'vi'

        try:
            if len(self.args) < 1:
                todo = config().todotxt()

                return call([editor, todo]) == 0
            else:
                self._process_flags()

                if self.edit_archive:
                    archive = config().archive()

                    return call([editor, archive]) == 0

                if self.is_expression:
                    self.todos = self._view()._viewdata
                else:
                    self.get_todos(self.args)

                todo_errors = self._catch_todo_errors()

                if not todo_errors:
                    temp_todos = self._todos_to_temp()

                    if not self._open_in_editor(temp_todos, editor):
                        new_todos = self._todos_from_temp(temp_todos)
                        if len(new_todos) == len(self.todos):
                            for todo in self.todos:
                                BASE_TODOLIST(self.todolist).delete(todo)

                            for todo in new_todos:
                                self.todolist.add_todo(todo)
                                self.out(self.printer.print_todo(todo))
                        else:
                            self.error('Number of edited todos is not equal to '
                                        'number of supplied todo IDs.')
                    else:
                        self.error(self.usage())
                else:
                    for error in todo_errors:
                        self.error(error)
        except(OSError):
            self.error('There is no such editor as: ' + editor + '. '
                        'Check your $EDITOR and/or $PATH')

    def usage(self):
        return """Synopsis:
  edit
  edit <NUMBER1> [<NUMBER2> ...]
  edit -e [-x] [expression]
  edit -d"""

    def help(self):
        return """\
Launches a text editor to edit todos.

Without any arguments it will just open the todo.txt file. Alternatively it can
edit todo item(s) with the given number(s) or edit relevant todos matching
the given expression. See `topydo help ls` for more information on relevant
todo items. It is also possible to open the archive file.

By default it will use $EDITOR in your environment, otherwise it will fall back
to 'vi'.

-e : Treat the subsequent arguments as an expression.
-x : Edit *all* todos matching the expression (i.e. do not filter on
     dependencies or relevance).
-d : Open the archive file.
"""
