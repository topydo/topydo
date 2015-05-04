# Topydo - A todo.txt client written in Python.
# Copyright (C) 2015 Bram Schoenmakers <me@bramschoenmakers.nl>
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

import re
from prompt_toolkit.completion import Completer, Completion

from topydo.Commands import _SUBCOMMAND_MAP

class TopydoCompleter(Completer):
    def __init__(self, p_todolist):
        self.todolist = p_todolist

    def get_completions(self, p_document, p_complete_event):
        # include all characters except whitespaces (for + and @)
        word_before_cursor = p_document.get_word_before_cursor(True)
        is_first_word = not re.match(r'\s*\S+\s', p_document.current_line_before_cursor)

        if is_first_word:
            subcommands = [sc for sc in sorted(_SUBCOMMAND_MAP.keys()) if sc.startswith(word_before_cursor)]
            for command in subcommands:
                yield Completion(command, -len(word_before_cursor))
        elif word_before_cursor.startswith('+'):
            projects = [p for p in self.todolist.projects() if p.startswith(word_before_cursor[1:])]

            for project in projects:
                yield Completion("+" + project, -len(word_before_cursor))
        elif word_before_cursor.startswith('@'):
            contexts = [c for c in self.todolist.contexts() if c.startswith(word_before_cursor[1:])]

            for context in contexts:
                yield Completion("@" + context, -len(word_before_cursor))
