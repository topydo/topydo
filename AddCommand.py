""" Provides the AddCommand class that implements the 'add' subcommand. """

from datetime import date
import re

import Config
import Command
from PrettyPrinter import pretty_print
from RelativeDate import relative_date_to_date

class AddCommand(Command.Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(AddCommand, self).__init__(p_args, p_todolist, p_out, p_err, p_prompt)
        self.text = ' '.join(p_args)

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
                except ValueError:
                    continue

                if p_tag == 'after':
                    self.todolist.add_dependency(self.todo.attributes['number'], value)
                elif p_tag == 'before' or p_tag == 'partof':
                    self.todolist.add_dependency(value, self.todo.attributes['number'])

                self.todo.remove_tag(p_tag, raw_value)

        convert_date(Config.TAG_START)
        convert_date(Config.TAG_DUE)

        add_dependencies('partof')
        add_dependencies('before')
        add_dependencies('after')

        self.todo.set_creation_date(date.today())

    def execute(self):
        """ Adds a todo item to the list. """
        self._preprocess_input_todo()
        self.todo = self.todolist.add(self.text)
        self._postprocess_input_todo()

        self.out(pretty_print(self.todo, [self.todolist.pp_number()]))
