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

""" Provides the AddCommand class that implements the 'add' subcommand. """

import codecs
import re
from datetime import date
from os.path import expanduser
from sys import stdin

from topydo.lib.Config import config
from topydo.lib.prettyprinters.Numbers import PrettyPrinterNumbers
from topydo.lib.WriteCommand import WriteCommand


class AddCommand(WriteCommand):
    def __init__(self, p_args, p_todolist, # pragma: no branch
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super().__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)
        self.text = ' '.join(p_args)
        self.from_file = None

    def _process_flags(self):
        opts, args = self.getopt('f:')

        for opt, value in opts:
            if opt == '-f':
                self.from_file = expanduser(value)

        self.args = args

    def get_todos_from_file(self):
        if self.from_file == '-':
            f = stdin
        else:
            f = codecs.open(self.from_file, 'r', encoding='utf-8')

        todos = f.read().splitlines()

        return todos

    def _add_todo(self, p_todo_text):
        def _preprocess_input_todo(p_todo_text):
            """
            Pre-processes user input when adding a task.

            It detects a priority mid-sentence and puts it at the start.
            """
            todo_text = re.sub(r'^(.+) (\([A-Z]\))(.*)$', r'\2 \1\3',
                               p_todo_text)

            return todo_text

        todo_text = _preprocess_input_todo(p_todo_text)
        todo = self.todolist.add(todo_text)
        self.postprocess_input_todo(todo)

        if config().auto_creation_date():
            todo.set_creation_date(date.today())

        self.out(self.printer.print_todo(todo))

    def execute(self):
        """ Adds a todo item to the list. """
        if not super().execute():
            return False

        self.printer.add_filter(PrettyPrinterNumbers(self.todolist))
        self._process_flags()

        if self.from_file:
            try:
                new_todos = self.get_todos_from_file()

                for todo in new_todos:
                    self._add_todo(todo)
            except (IOError, OSError):
                self.error('File not found: ' + self.from_file)
        else:
            if self.text:
                self._add_todo(self.text)
            else:
                self.error(self.usage())

    def usage(self):
        return """Synopsis:
  add <TEXT>
  add -f <FILE> | -"""

    def help(self):
        return """\
This subcommand automatically adds the creation date to the added item.

TEXT may contain:

* Priorities mid-sentence. Example: add "Water flowers (C)"

* Dependencies using before, after, partof, parents-of and children-of tags.
  These are translated to the corresponding 'id' and 'p' tags. The values of
  these tags correspond to the todo number (not the dependency number).

  Example: add "Subtask partof:1"

-f : Add todo items from specified FILE or from standard input.\
"""
