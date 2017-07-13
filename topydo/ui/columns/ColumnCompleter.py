# Topydo - A todo.txt client written in Python.
# Copyright (C) 2017 Bram Schoenmakers <bram@topydo.org>
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
This module provides a completer class that can be used by the Column UI
CommmandLineWidget.
"""

from topydo.lib.Config import config
from topydo.ui.CompleterBase import CompleterBase, date_suggestions


class ColumnCompleter(CompleterBase):
    """
    Completer class that completes projects, contexts, dates and
    subcommands designed to work with CommandLineWidget for column UI.
    """
    def get_completions(self, p_word, p_is_first_word=False):
        def dates(p_word, p_tag):
            dates = []
            for date in date_suggestions():
                candidate = p_tag + ':' + date
                if candidate.startswith(p_word):
                    dates.append(candidate)

            return dates

        due_tag = config().tag_due()
        start_tag = config().tag_start()

        if p_word.startswith(due_tag + ':'):
            return dates(p_word, due_tag)
        elif p_word.startswith(start_tag + ':'):
            return dates(p_word, start_tag)
        else:
            return super().get_completions(p_word, p_is_first_word)
