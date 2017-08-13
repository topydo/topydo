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

import unittest
from datetime import date

from freezegun import freeze_time

from topydo.lib.Config import config
from topydo.lib.Importance import importance
from topydo.lib.Todo import Todo

from .topydo_testcase import TopydoTest


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


@freeze_time("2016, 10, 21")
class ImportanceWeekendFridayTest(TopydoTest):
    def test_importance_ignore_weekends_due_not_next_monday(self):
        # Today is friday
        # due on a monday, but over a month away.
        # So 2 + 0 (no priority) + 0 (no star) + 0 (due > 14 days)
        config(p_overrides={('sort', 'ignore_weekends'): '1'})
        todo = Todo("Foo " + config().tag_due() + ":" + "2016-11-28")
        self.assertEqual(importance(todo), 2)


@freeze_time("2016, 10, 22")
class ImportanceWeekendSaturdayTest(TopydoTest):
    def test_importance_ignore_weekends_due_not_next_monday(self):
        # Today is saturday
        # due on a monday, but over a month away.
        # So 2 + 0 (no priority) + 0 (no star) + 0 (due > 14 days)
        config(p_overrides={('sort', 'ignore_weekends'): '1'})
        todo = Todo("Foo " + config().tag_due() + ":" + "2016-11-28")
        self.assertEqual(importance(todo), 2)


@freeze_time("2016, 10, 23")
class ImportanceWeekendSundayTest(TopydoTest):
    def test_importance_ignore_weekends_due_not_next_monday(self):
        # Today is sunday
        # due on a monday, but over a month away.
        # So 2 + 0 (no priority) + 0 (no star) + 0 (due > 14 days)
        config(p_overrides={('sort', 'ignore_weekends'): '1'})
        todo = Todo("Foo " + config().tag_due() + ":" + "2016-11-28")
        self.assertEqual(importance(todo), 2)


if __name__ == '__main__':
    unittest.main()
