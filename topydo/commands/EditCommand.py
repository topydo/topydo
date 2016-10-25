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

import os
import codecs
import tempfile
from subprocess import CalledProcessError, check_call

from topydo.lib.Config import config
from topydo.lib.MultiCommand import MultiCommand
from topydo.lib.prettyprinters.Numbers import PrettyPrinterNumbers
from topydo.lib.Todo import Todo
from topydo.lib.TodoList import TodoList

# the true and only editor
DEFAULT_EDITOR = 'vi'

def _get_file_mtime(p_file):
    return os.stat(p_file.name).st_mtime

def _is_edited(p_orig_mtime, p_file):
    return p_orig_mtime < _get_file_mtime(p_file)

class EditCommand(MultiCommand):
    def __init__(self, p_args, p_todolist, p_output, p_error, p_input):
        super().__init__(p_args, p_todolist, p_output,
                                          p_error, p_input)

        if len(self.args) == 0:
            self.multi_mode = False

        self.is_expression = False
        self.edit_archive = False
        self.last_argument = False

    def get_flags(self):
        return ("d", [])

    def process_flag(self, p_opt, p_value):
        if p_opt == '-d':
            self.edit_archive = True
            self.multi_mode = False

    def _todos_to_temp(self):
        f = tempfile.NamedTemporaryFile(delete=False, suffix='.todo.txt')
        for todo in self.todos:
            f.write((todo.source() + "\n").encode('utf-8'))
        f.close()

        return f

    def _todos_from_temp(self, p_temp_file):
        f = codecs.open(p_temp_file.name, encoding='utf-8')
        todos = f.read().splitlines()

        todo_objs = []
        for todo in todos:
            todo_objs.append(Todo(todo))

        return todo_objs

    def _open_in_editor(self, p_file):
        try:
            editor = os.environ['EDITOR'] or DEFAULT_EDITOR
        except(KeyError):
            editor = DEFAULT_EDITOR

        try:
            return check_call([editor, p_file])
        except CalledProcessError:
            self.error('Something went wrong in the editor...')
            return 1
        except(OSError):
            self.error('There is no such editor as: ' + editor + '. '
                       'Check your $EDITOR and/or $PATH')

    def _catch_todo_errors(self):
        errors = []

        if len(self.invalid_numbers) > 1 or len(self.invalid_numbers) > 0 and len(self.todos) > 0:
            for number in self.invalid_numbers:
                errors.append(u"Invalid todo number given: {}.".format(number))
        elif len(self.invalid_numbers) == 1 and len(self.todos) == 0:
            errors.append("Invalid todo number given.")

        if len(errors) > 0:
            return errors
        else:
            return None

    def _execute_multi_specific(self):
        self.printer.add_filter(PrettyPrinterNumbers(self.todolist))

        temp_todos = self._todos_to_temp()
        orig_mtime = _get_file_mtime(temp_todos)

        if not self._open_in_editor(temp_todos.name):
            new_todos = self._todos_from_temp(temp_todos)

            if _is_edited(orig_mtime, temp_todos):
                for todo in self.todos:
                    self.todolist.delete(todo, p_leave_tags=True)

                for todo in new_todos:
                    self.todolist.add_todo(todo)
                    self.out(self.printer.print_todo(todo))
            else:
                self.error('Editing aborted. Nothing to do.')
        else:
            self.error(self.usage())

        os.unlink(temp_todos.name)

    def _execute_not_multi(self):
        if self.edit_archive:
            archive = config().archive()

            return self._open_in_editor(archive) == 0
        else:
            todo = config().todotxt()

            return self._open_in_editor(todo) == 0

    def usage(self):
        return """Synopsis:
  edit
  edit <NUMBER 1> [<NUMBER 2> ...]
  edit -e [-x] [EXPRESSION]
  edit -d"""

    def help(self):
        return """\
Launches a text editor to edit todos.

Without any arguments it will just open the todo.txt file. Alternatively it can
edit todo item(s) with the given NUMBER(s) or edit relevant todos matching
the given EXPRESSION. See `topydo help ls` for more information on relevant
todo items. It is also possible to open the archive file.

By default it will look to your environment variable $EDITOR, otherwise it will
fall back to 'vi'.

-e : Treat the subsequent arguments as an EXPRESSION.
-x : Edit *all* todos matching the EXPRESSION (i.e. do not filter on
     dependencies or relevance).
-d : Open the archive file.\
"""
