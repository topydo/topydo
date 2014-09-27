from datetime import date
import re

import Config
import Command
from RelativeDate import relative_date_to_date

class AddCommand(Command.Command):
    def __init__(self, p_text, p_todolist):
        super(AddCommand, self).__init__(p_todolist)
        self.text = p_text

    def _preprocess_input_todo(self):
        """
        Preprocesses user input when adding a task.

        It detects a priority mid-sentence and puts it at the start.
        """
        self.text = re.sub(r'^(.+) (\([A-Z]\))(.*)$', r'\2 \1\3', self.text)

    def _postprocess_input_todo(self): # TODO: split function
        """
        Post-processes a parsed todo when adding it to the list.

        * It converts relative dates to absolute ones.
        * Automatically inserts a creation date if not present.
        * Handles more user-friendly dependencies with before: and after: tags
        """
        for tag in [Config.TAG_START, Config.TAG_DUE]:
            value = self.todo.tag_value(tag)

            if value:
                dateobj = relative_date_to_date(value)
                if dateobj:
                    self.todo.set_tag(tag, dateobj.isoformat())

        self.todo.set_creation_date(date.today())

        for tag in ['before', 'after']:
            for raw_value in self.todo.tag_values(tag):
                try:
                    value = int(raw_value)
                except ValueError:
                    continue

                if tag == 'after':
                    self.todolist.add_dependency(self.todo.attributes['number'], value)
                elif tag == 'before':
                    self.todolist.add_dependency(value, self.todo.attributes['number'])

                self.todo.remove_tag(tag, raw_value)

    def execute(self):
        """ Adds a todo item to the list. """
        self._preprocess_input_todo()
        self.todo = self.todolist.add(self.text)
        self._postprocess_input_todo()

