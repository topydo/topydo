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

import os

from topydo.lib.Utils import escape_ansi

from .topydo_testcase import TopydoTest


class CommandTest(TopydoTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output = ""
        self.errors = ""

    def out(self, p_output):
        if isinstance(p_output, list) and p_output:
            self.output += escape_ansi(
                os.linesep.join([str(s) for s in p_output]) + os.linesep)
        elif p_output:
            self.output += str(p_output) + os.linesep

    def error(self, p_error):
        if isinstance(p_error, list) and p_error:
            self.errors += escape_ansi(p_error + os.linesep) + os.linesep
        elif p_error:
            self.errors += str(p_error) + os.linesep
