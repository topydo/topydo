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

import codecs
import os
import shlex
import tempfile
from subprocess import CalledProcessError, check_call

from topydo.lib.Config import config
from topydo.lib.MultiCommand import MultiCommand
from topydo.lib.prettyprinters.Numbers import PrettyPrinterNumbers
from topydo.lib.Todo import Todo


def _get_file_mtime(p_file):
    return os.stat(p_file.name).st_mtime

def _is_edited(p_orig_mtime, p_file):
    return p_orig_mtime < _get_file_mtime(p_file)

class EditCommand(MultiCommand):
    def __init__(self, p_args, p_todolist, p_output, p_error, p_input):
        super().__init__(p_args, p_todolist, p_output,
                                          p_error, p_input)

        self.editor = config().editor()
        self.is_expression = False
        self.edit_archive = False
        self.last_argument = False

    def get_flags(self):
        return ("dE:", [])

    def process_flag(self, p_option, p_value):
        if p_option == '-d':
            self.edit_archive = True
            self.multi_mode = False
        elif p_option == '-E':
            self.editor = shlex.split(p_value)

    def _process_flags(self):
        """
        Override to add an additional check after processing the flags: when
        there are no flags left after argument parsing, then it means we'll be
        editing the whole todo.txt file as a whole and therefore we're not in
        multi mode.
        """
        super()._process_flags()

        if len(self.args) == 0:
            self.multi_mode = False

    def _todos_to_temp(self):
        f = tempfile.NamedTemporaryFile(delete=False, suffix='.todo.txt')
        for todo in self.todos:
            f.write((todo.source() + "\n").encode('utf-8'))
        f.close()

        return f

    @staticmethod
    def _todos_from_temp(p_temp_file):
        with codecs.open(p_temp_file.name, encoding='utf-8') as temp:
            todos = temp.read().splitlines()

        todo_objs = []
        for todo in todos:
            todo_objs.append(Todo(todo))

        return todo_objs

    def _open_in_editor(self, p_file):
        try:
            return check_call(self.editor + [p_file])
        except CalledProcessError:
            self.error('Something went wrong in the editor...')
            return 1
        except OSError:
            self.error('There is no such editor as: ' + self.editor + '. '
                       'Check your configuration file, $TOPYDO_EDITOR, $EDITOR and/or $PATH')

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
            new_todos = EditCommand._todos_from_temp(temp_todos)

            if _is_edited(orig_mtime, temp_todos):
                modified = list(zip(self.todos, new_todos))
                for (todo, new_todo) in modified:
                    self.todolist.modify_todo(todo, new_todo.src)
                    self.out(self.printer.print_todo(todo))

                for todo in self.todos[len(modified):]:
                    self.todolist.delete(todo, p_leave_tags=True)

                for todo in new_todos[len(modified):]:
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
  edit [-E <EDITOR>]
  edit [-E <EDITOR>] <NUMBER 1> [<NUMBER 2> ...]
  edit [-E <EDITOR>] -e [-x] [EXPRESSION]
  edit [-E <EDITOR>] -d"""

    def help(self):
        return """\
Launches a text editor to edit todos.

Without any arguments it will just open the todo.txt file. Alternatively it can
edit todo item(s) with the given NUMBER(s) or edit relevant todos matching
the given EXPRESSION. See `topydo help ls` for more information on relevant
todo items. It is also possible to open the archive file.

The editor is chosen as follows:
    1. Check whether the -E flag is given and use it;
    2. Use the value of $TOPYDO_EDITOR in the environment;
    3. Use the value in the configuration file;
    4. Use the value of $EDITOR in the environment;
    5. If all else fails, use 'vi'.

-e : Treat the subsequent arguments as an EXPRESSION.
-E : Editor to start.
-x : Edit *all* todos matching the EXPRESSION (i.e. do not filter on
     dependencies or relevance).
-d : Open the archive file.\
"""
