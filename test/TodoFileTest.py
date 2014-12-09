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

from test.TestFacilities import load_file
from test.TopydoTest import TopydoTest

class TodoFileTest(TopydoTest):
    def test_empty_file(self):
        todofile = load_file('test/data/TodoFileTest1.txt')

        self.assertEquals(len(todofile), 0)

if __name__ == '__main__':
    unittest.main()
