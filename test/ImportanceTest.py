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

from datetime import date
import unittest

from topydo.lib.Config import config
from topydo.lib.Importance import importance
from topydo.lib.Todo import Todo
from test.TopydoTest import TopydoTest

class ImportanceTest(TopydoTest):
    def test_importance1(self):
        todo = Todo("Foo")
        self.assertEqual(importance(todo), 2)

    def test_importance2(self):
        todo = Todo("(A) Foo")
        self.assertEqual(importance(todo), 5)

    def test_importance3(self):
        todo = Todo("(A) Foo " + config().tag_star() + ":1")
        self.assertEqual(importance(todo), 6)

    def test_importance4(self):
        today_str = date.today().isoformat()
        todo = Todo("(C) Foo " + config().tag_due() + ":" + today_str)
        self.assertEqual(importance(todo), 8)

if __name__ == '__main__':
    unittest.main()
