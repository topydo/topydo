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
from datetime import date, timedelta

from topydo.lib.Todo import Todo

from .topydo_testcase import TopydoTest


def today_date():
    today = date.today()
    return today.isoformat()


def tomorrow_date():
    tomorrow = date.today() + timedelta(days=1)
    return tomorrow.isoformat()


class TodoTest(TopydoTest):
    def test_due_date1(self):
        todo = Todo("(C) Foo due:2014-06-09")
        due = date(2014, 6, 9)

        self.assertEqual(todo.due_date(), due)

    def test_false_date(self):
        todo = Todo("(C) Foo due:2014-04-31")
        self.assertEqual(todo.due_date(), None)

    def test_active1(self):
        todo = Todo("(C) Foo due:2014-01-01")
        self.assertTrue(todo.is_active())

    def test_active2(self):
        todo = Todo("(C) Foo t:" + tomorrow_date())
        self.assertFalse(todo.is_active())

    def test_active3(self):
        todo = Todo("x 2014-06-09 Foo t:2014-01-01")
        self.assertFalse(todo.is_active())

    def test_active4(self):
        todo = Todo("(C) Foo t:" + today_date())
        self.assertTrue(todo.is_active())

    def test_active5(self):
        todo = Todo("(C) Foo t:2014-02-29")
        self.assertTrue(todo.is_active())

    def test_overdue1(self):
        todo = Todo("(C) Foo due:2014-01-01")
        self.assertTrue(todo.is_overdue())

    def test_overdue2(self):
        todo = Todo("(C) Foo due:" + tomorrow_date())
        self.assertFalse(todo.is_overdue())

    def test_overdue3(self):
        todo = Todo("(C) Foo due:" + today_date())
        self.assertFalse(todo.is_overdue())

    def days_till_due(self):
        todo = Todo("(C) due:" + tomorrow_date())
        self.assertEqual(todo.days_till_due(), 1)

    def test_length1(self):
        todo = Todo("(C) Foo t:2014-01-01 due:2013-12-31")
        self.assertEqual(todo.length(), 0)

    def test_length2(self):
        todo = Todo("(C) Foo t:2014-01-01 due:2014-01-01")
        self.assertEqual(todo.length(), 0)

    def test_length3(self):
        todo = Todo("(C) Foo t:2014-01-01 due:2014-01-02")
        self.assertEqual(todo.length(), 1)

    def test_length4(self):
        todo = Todo("(C) Foo)")
        self.assertEqual(todo.length(), 0)

    def test_length5(self):
        todo = Todo("(C) 2015-11-18 Foo)")
        self.assertEqual(todo.length(), 0)

    def test_length6(self):
        todo = Todo("(C) 2015-11-18 Foo due:2015-11-19)")
        self.assertEqual(todo.length(), 1)

    def test_length7(self):
        todo = Todo("(C) 2015-11-18 Foo due:2015-11-18)")
        self.assertEqual(todo.length(), 0)

    def test_length8(self):
        todo = Todo("(C) 2015-11-18 Foo t:2015-11-19 due:2015-11-20)")
        self.assertEqual(todo.length(), 1)

    def test_length9(self):
        todo = Todo("(C) 2015-11-18 Foo due:2015-11-16)")
        self.assertEqual(todo.length(), 0)

    def test_length10(self):
        todo = Todo("(C) Foo t:2017-06-30")
        self.assertEqual(todo.length(), 0)

    def test_length11(self):
        todo = Todo("(C) Foo t:2017-06-31 due:2017-07-01")
        self.assertEqual(todo.length(), 0)

if __name__ == '__main__':
    unittest.main()
