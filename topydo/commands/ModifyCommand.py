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

from topydo.lib.Config import config
from topydo.lib.prettyprinters.Numbers import PrettyPrinterNumbers
from topydo.lib.TodoListBase import InvalidTodoException
from topydo.lib.TodoParser import parse_line
from topydo.lib.WriteCommand import WriteCommand


class ModifyCommand(WriteCommand):
    def __init__(self, p_args, p_todolist, #pragma: no branch
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super().__init__(p_args, p_todolist, p_out, p_err,
                p_prompt)

    def execute(self):
        if not super().execute():
            return False

        if len(self.args) < 2:
            self.error(self.usage())
            return False
        text = self.args[0]
        numbers = self.args[1:]

        if not isinstance(text, str):
            self.error(self.usage())
            return False
        new_text_parsed = parse_line(text)
        new_tags = new_text_parsed['tags']

        self.printer.add_filter(PrettyPrinterNumbers(self.todolist))

        # Parse numbers/ids first to ensure all valid before any writes
        todos = []
        for num in numbers:
            try:
                todos.append(self.todolist.todo(num))
            except InvalidTodoException:
                self.error(f"Invalid todo number: {num}")
                return False

        for todo in todos:
            # Remove any existing start or due tags
            for tag in new_tags:
                if tag in (config().tag_start(), config().tag_due()):
                    todo.remove_tag(tag)

            self.todolist.append(todo, text)
            self.postprocess_input_todo(todo)

            self.out(self.printer.print_todo(todo))

        return True

    def usage(self):
        return """Synopsis: modify <TEXT> <NUMBER> [<NUMBER 2> ...]"""

    def help(self):
        return """\
Adds the TEXT to the end of the todo items indicated by NUMBER(s).\
"""
