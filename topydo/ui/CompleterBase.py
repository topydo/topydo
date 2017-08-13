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

import datetime
from functools import lru_cache

from topydo.Commands import SUBCOMMAND_MAP
from topydo.lib.Config import config


@lru_cache(maxsize=1)
def _get_subcmds():
    subcmd_map = config().aliases().copy()
    subcmd_map.update(SUBCOMMAND_MAP)

    return sorted(subcmd_map.keys())


def date_suggestions():
    """
    Returns a list of relative date that is presented to the user as auto
    complete suggestions.
    """
    # don't use strftime, prevent locales to kick in
    days_of_week = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }

    dates = [
        'today',
        'tomorrow',
    ]

    # show days of week up to next week
    dow = datetime.date.today().weekday()
    for i in range(dow + 2 % 7, dow + 7):
        dates.append(days_of_week[i % 7])

    # and some more relative days starting from next week
    dates += ["1w", "2w", "1m", "2m", "3m", "1y"]

    return dates


class CompleterBase(object):
    def __init__(self, p_todolist):
        self.todolist = p_todolist
        self._all_subcmds = _get_subcmds()

    def _contexts(self, p_word):
        completions = ['@' + context for context in self.todolist.contexts() if
                       context.startswith(p_word[1:])]
        return sorted(completions)

    def _projects(self, p_word):
        completions = ['+' + project for project in self.todolist.projects() if
                       project.startswith(p_word[1:])]
        return sorted(completions)

    def _subcmds(self, p_word):
        completions = [cmd for cmd in self._all_subcmds if
                       cmd.startswith(p_word)]
        return completions

    def get_completions(self, p_word, p_is_first_word=False):
        completions = []

        if p_word.startswith('+'):
            completions = self._projects(p_word)
        elif p_word.startswith('@'):
            completions = self._contexts(p_word)
        elif p_is_first_word:
            completions = self._subcmds(p_word)

        return completions
