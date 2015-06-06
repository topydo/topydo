# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 Bram Schoenmakers <me@bramschoenmakers.nl>
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

import unittest

from topydo.lib.Utils import escape_ansi
from test.TopydoTest import TopydoTest

class CommandTest(TopydoTest):
    def __init__(self, *args, **kwargs):
        super(CommandTest, self).__init__(*args, **kwargs)
        self.output = ""
        self.errors = ""

    def out(self, p_output):
        if p_output:
            self.output += escape_ansi(p_output + "\n")

    def error(self, p_error):
        if p_error:
            self.errors += escape_ansi(p_error + "\n")

if __name__ == '__main__':
    unittest.main()
