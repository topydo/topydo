# Topydo - A todo.txt client written in Python.
# Copyright (C) 2015 Bram Schoenmakers <bram@topydo.org>
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

"""
This module provides a completer class that can be used by the prompt provided
by the prompt toolkit.
"""

import re

from prompt_toolkit.completion import Completer, Completion
from topydo.lib.Completer import CompleterBase, date_suggestions
from topydo.lib.Config import config
from topydo.lib.RelativeDate import relative_date_to_date


def _dates(p_word_before_cursor):
    """ Generator for date completion. """
    to_absolute = lambda s: relative_date_to_date(s).isoformat()

    start_value_pos = p_word_before_cursor.find(':') + 1
    value = p_word_before_cursor[start_value_pos:]

    for reldate in date_suggestions():
        if not reldate.startswith(value):
            continue

        yield Completion(reldate, -len(value), display_meta=to_absolute(reldate))


class TopydoCompleter(Completer):
    """
    Completer class that completes projects, contexts, dates and
    subcommands.
    """

    def __init__(self, p_todolist):
        self.inner_completer = CompleterBase(p_todolist)

    def _projects(self, p_word_before_cursor):
        """ Generator for project completion. """
        projects = self.inner_completer.projects(p_word_before_cursor)
        for project in projects:
            yield Completion(project, -len(p_word_before_cursor))

    def _contexts(self, p_word_before_cursor):
        """ Generator for context completion. """
        contexts = self.inner_completer.contexts(p_word_before_cursor)
        for context in contexts:
            yield Completion(context, -len(p_word_before_cursor))

    def _subcmds(self, p_word_before_cursor):
        subcommands = self.inner_completer.subcmds(p_word_before_cursor)
        for command in subcommands:
            yield Completion(command, -len(p_word_before_cursor))

    def get_completions(self, p_document, _):
        # include all characters except whitespaces (for + and @)
        word_before_cursor = p_document.get_word_before_cursor(True)
        is_first_word = not re.match(r'\s*\S+\s',
                                     p_document.current_line_before_cursor)

        if is_first_word:
            return self._subcmds(word_before_cursor)
        elif word_before_cursor.startswith('+'):
            return self._projects(word_before_cursor)
        elif word_before_cursor.startswith('@'):
            return self._contexts(word_before_cursor)
        elif word_before_cursor.startswith(config().tag_due() + ':'):
            return _dates(word_before_cursor)
        elif word_before_cursor.startswith(config().tag_start() + ':'):
            return _dates(word_before_cursor)

        return []
