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

import sys

from topydo.lib.Command import Command


class ExitCommand(Command):
    """
    A command that exits topydo. Used for the 'exit' and 'quit' subcommands on
    the prompt CLI.
    """

    def __init__(self, p_args, p_todolist, p_output, p_error, p_input):
        super().__init__(p_args, p_todolist, p_output, p_error,
                                          p_input)

    def execute(self):
        if not super().execute():
            return False

        sys.exit(0)
