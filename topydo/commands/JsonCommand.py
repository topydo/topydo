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

"""
Implements a subcommand that outputs an JSON file.
"""

from topydo.lib.JsonPrinter import JsonPrinter
from topydo.commands.ListCommand import ListCommand

class JsonCommand(ListCommand):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(JsonCommand, self).__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

        self.printer = JsonPrinter()

    def _print(self):
        self.out(str(self._view()))

    def execute(self):
        return super(JsonCommand, self).execute()

    def usage(self):
        return """Synopsis: json [-x] [expression]"""

    def help(self):
        return """\
Similar to the 'ls' subcommand, except that the todos are printed in JSON
format such that other applications can process it.

By default prints the active todo items, possibly filtered by the given
expression.

For the supported options, please refer to the help text of 'ls'
(topydo help ls).

Note: topydo does not support reading JSON files, this is merely a dump.
"""
