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

""" Provides the AddCommand class that implements the 'add' subcommand. """

from datetime import date
import re

from topydo.lib.Config import config
from topydo.lib.Command import Command
from topydo.lib.PrettyPrinter import pretty_print
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
        self.todo = None

    def _preprocess_input_todo(self):
        """
        Preprocesses user input when adding a task.

        It detects a priority mid-sentence and puts it at the start.
        """
        self.text = re.sub(r'^(.+) (\([A-Z]\))(.*)$', r'\2 \1\3', self.text)

    def _postprocess_input_todo(self):
        """
        Post-processes a parsed todo when adding it to the list.

        * It converts relative dates to absolute ones.
        * Automatically inserts a creation date if not present.
        * Handles more user-friendly dependencies with before:, partof: and
          after: tags
        """
        def convert_date(p_tag):
            value = self.todo.tag_value(p_tag)

            if value:
                dateobj = relative_date_to_date(value)
                if dateobj:
                    self.todo.set_tag(p_tag, dateobj.isoformat())

        def add_dependencies(p_tag):
            for raw_value in self.todo.tag_values(p_tag):
                try:
                    value = int(raw_value)
                    dep = self.todolist.todo(value)

                    if p_tag == 'after':
                        self.todolist.add_dependency(self.todo, dep)
                    elif p_tag == 'before' or p_tag == 'partof':
                        self.todolist.add_dependency(dep, self.todo)
                except ValueError:
                    continue
                except InvalidTodoException:
                    pass

                self.todo.remove_tag(p_tag, raw_value)

        convert_date(config().tag_start())
        convert_date(config().tag_due())

        add_dependencies('partof')
        add_dependencies('before')
        add_dependencies('after')

        self.todo.set_creation_date(date.today())

    def execute(self):
        """ Adds a todo item to the list. """
        if not super(AddCommand, self).execute():
            return False

        if self.text:
            self._preprocess_input_todo()
            self.todo = self.todolist.add(self.text)
            self._postprocess_input_todo()

            self.out(pretty_print(self.todo, [self.todolist.pp_number()]))
        else:
            self.error(self.usage())

    def usage(self):
        return """Synopsis: add <text>"""

    def help(self):
        return """\
This subcommand automatically adds the creation date to the added item.

<text> may contain:

* Priorities mid-sentence. Example: add "Water flowers (C)"

* Dependencies using before, after and partof tags. They are translated to the
  corresponding 'id' and 'p' tags. The values of these tags correspond to the
  todo number (not the dependency number).

  Example: add "Subtask partof:1"
"""
