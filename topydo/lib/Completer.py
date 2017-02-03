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

from topydo.Commands import _SUBCOMMAND_MAP
from topydo.lib.Config import config


def _get_subcmds():
    subcmd_map = config().aliases()
    subcmd_map.update(_SUBCOMMAND_MAP)

    return sorted(subcmd_map.keys())


class CompleterBase(object):
    def __init__(self, p_todolist):
        self.todolist = p_todolist
        self._subcmds = _get_subcmds()

    def _complete_context(self, p_word):
        completions = ['@' + context for context in self.todolist.contexts() if
                       context.startswith(p_word[1:])]
        return completions

    def _complete_project(self, p_word):
        completions = ['+' + project for project in self.todolist.projects() if
                       project.startswith(p_word[1:])]
        return completions

    def _complete_subcmd(self, p_word):
        completions = [cmd for cmd in self._subcmds if
                       cmd.startswith(p_word)]
        return completions

    def get_completions(self, p_word, p_is_first_word=False):
        completions = []

        if p_word.startswith('+'):
            completions = self._complete_project(p_word)
        elif p_word.startswith('@'):
            completions = self._complete_context(p_word)
        elif p_is_first_word:
            completions = self._complete_subcmd(p_word)

        return completions
