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

from topydo.lib.Config import config
from topydo.lib.RelativeDate import relative_date_to_date
from topydo.ui.CompleterBase import CompleterBase, date_suggestions


def _dates(p_word_before_cursor):
    """ Generator for date completion. """
    to_absolute = lambda s: relative_date_to_date(s).isoformat()

    start_value_pos = p_word_before_cursor.find(':') + 1
    value = p_word_before_cursor[start_value_pos:]

    for reldate in date_suggestions():
        if not reldate.startswith(value):
            continue

        yield Completion(reldate, -len(value), display_meta=to_absolute(reldate))


class PromptCompleter(CompleterBase, Completer):
    """
    Completer class that completes projects, contexts, dates and
    subcommands and is compatible with prompt toolkit.
    """

    def _completion_generator(self, p_word, is_first_word):
        candidates = super().get_completions(p_word, is_first_word)
        for candidate in candidates:
            yield Completion(candidate, -len(p_word))

    def get_completions(self, p_word, p_is_first_word=False):
        # include all characters except whitespaces (for + and @)
        word_before_cursor = p_word.get_word_before_cursor(True)
        is_first_word = not re.match(r'\s*\S+\s',
                                     p_word.current_line_before_cursor)
        if word_before_cursor.startswith(config().tag_due() + ':'):
            return _dates(word_before_cursor)
        elif word_before_cursor.startswith(config().tag_start() + ':'):
            return _dates(word_before_cursor)

        return self._completion_generator(word_before_cursor, is_first_word)
