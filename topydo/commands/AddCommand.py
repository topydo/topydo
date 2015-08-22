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

""" Provides the AddCommand class that implements the 'add' subcommand. """

from datetime import date
import re
from sys import stdin
import codecs
from os.path import expanduser

from topydo.lib.Config import config
from topydo.lib.Command import Command
from topydo.lib.PrettyPrinterFilter import PrettyPrinterNumbers
from topydo.lib.RelativeDate import relative_date_to_date
from topydo.lib.TodoListBase import InvalidTodoException

class AddCommand(Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(AddCommand, self).__init__(
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
            Preprocesses user input when adding a task.

            It detects a priority mid-sentence and puts it at the start.
            """
            todo_text = re.sub(r'^(.+) (\([A-Z]\))(.*)$', r'\2 \1\3', p_todo_text)

            return todo_text

        def _postprocess_input_todo(p_todo):
            """
            Post-processes a parsed todo when adding it to the list.

            * It converts relative dates to absolute ones.
            * Automatically inserts a creation date if not present.
            * Handles more user-friendly dependencies with before:, partof: and
            after: tags
            """
            def convert_date(p_tag):
                value = p_todo.tag_value(p_tag)

                if value:
                    dateobj = relative_date_to_date(value)
                    if dateobj:
                        p_todo.set_tag(p_tag, dateobj.isoformat())

            def add_dependencies(p_tag):
                for value in p_todo.tag_values(p_tag):
                    try:
                        dep = self.todolist.todo(value)

                        if p_tag == 'after':
                            self.todolist.add_dependency(p_todo, dep)
                        elif p_tag == 'before' or p_tag == 'partof':
                            self.todolist.add_dependency(dep, p_todo)
                    except InvalidTodoException:
                        pass

                    p_todo.remove_tag(p_tag, value)

            convert_date(config().tag_start())
            convert_date(config().tag_due())

            add_dependencies('partof')
            add_dependencies('before')
            add_dependencies('after')

            if config().auto_creation_date():
                p_todo.set_creation_date(date.today())

        todo_text = _preprocess_input_todo(p_todo_text)
        todo = self.todolist.add(todo_text)
        _postprocess_input_todo(todo)

        self.out(self.printer.print_todo(todo))

    def execute(self):
        """ Adds a todo item to the list. """
        if not super(AddCommand, self).execute():
            return False

        self.printer.add_filter(PrettyPrinterNumbers(self.todolist))
        self._process_flags()

        if self.from_file:
            new_todos = self.get_todos_from_file()

            for todo in new_todos:
                self._add_todo(todo)
        else:
            if self.text:
                self._add_todo(self.text)
            else:
                self.error(self.usage())

    def usage(self):
        return """Synopsis:
  add <text>
  add -f <file>
  add -f -"""

    def help(self):
        return """\
This subcommand automatically adds the creation date to the added item.

<text> may contain:

* Priorities mid-sentence. Example: add "Water flowers (C)"

* Dependencies using before, after and partof tags. They are translated to the
  corresponding 'id' and 'p' tags. The values of these tags correspond to the
  todo number (not the dependency number).

  Example: add "Subtask partof:1"

-f : Add todo items from specified <file> or from standard input.
"""
