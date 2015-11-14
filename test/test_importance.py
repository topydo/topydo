# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2015 Bram Schoenmakers <me@bramschoenmakers.nl>
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
from datetime import date, timedelta
from freezegun import freeze_time

from test.topydo_testcase import TopydoTest
from topydo.lib.Config import config
from topydo.lib.Importance import importance
from topydo.lib.Todo import Todo


@freeze_time("2015, 11, 06")
class ImportanceTest(TopydoTest):
    def test_importance01(self):
        todo = Todo("Foo")
        self.assertEqual(importance(todo), 2)

    def test_importance02(self):
        todo = Todo("(A) Foo")
        self.assertEqual(importance(todo), 5)

    def test_importance03(self):
        todo = Todo("(A) Foo " + config().tag_star() + ":1")
        self.assertEqual(importance(todo), 6)

    def test_importance04(self):
        today_str = date.today().isoformat()
        todo = Todo("(C) Foo " + config().tag_due() + ":" + today_str)
        self.assertEqual(importance(todo), 8)

    def test_importance05(self):
        todo = Todo("(C) Foo " + config().tag_due() + ":" + "2015-11-14")
        self.assertEqual(importance(todo), 4)

    def test_importance06(self):
        todo = Todo("(C) Foo " + config().tag_due() + ":" + "2015-11-10")
        self.assertEqual(importance(todo), 5)

    def test_importance07(self):
        config(p_overrides={('sort', 'ignore_weekends'): '1'})
        todo = Todo("(C) Foo " + config().tag_due() + ":" + "2015-11-09")
        self.assertEqual(importance(todo), 6)

if __name__ == '__main__':
    unittest.main()
