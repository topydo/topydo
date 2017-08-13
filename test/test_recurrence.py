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

from topydo.lib.Config import config
from topydo.lib.Recurrence import NoRecurrenceException, advance_recurring_todo
from topydo.lib.Todo import Todo

from .topydo_testcase import TopydoTest


class RecurrenceTest(TopydoTest):
    def setUp(self):
        super().setUp()
        self.todo = Todo("Test rec:1w")
        self.stricttodo = Todo("Test rec:+1w")

    def test_duedate1(self):
        """ Where due date is in the future. """
        future = date.today() + timedelta(1)
        new_due = date.today() + timedelta(7)

        self.todo.set_tag(config().tag_due(), future.isoformat())
        new_todo = advance_recurring_todo(self.todo)

        self.assertEqual(new_todo.due_date(), new_due)

    def test_duedate2(self):
        """ Where due date is today. """
        today = date.today()
        new_due = date.today() + timedelta(7)

        self.todo.set_tag(config().tag_due(), today.isoformat())
        new_todo = advance_recurring_todo(self.todo)

        self.assertEqual(new_todo.due_date(), new_due)

    def test_duedate3(self):
        """ Where due date is in the past. """
        past = date.today() - timedelta(8)
        new_due = date.today() + timedelta(7)

        self.todo.set_tag(config().tag_due(), past.isoformat())
        new_todo = advance_recurring_todo(self.todo)

        self.assertEqual(new_todo.due_date(), new_due)

    def test_duedate4(self):
        """ Where due date is in the past. """
        past = date.today() - timedelta(8)
        new_due = date.today() - timedelta(1)

        self.todo.set_tag(config().tag_due(), past.isoformat())
        new_todo = advance_recurring_todo(self.todo, p_strict=True)

        self.assertEqual(new_todo.due_date(), new_due)

    def test_duedate5(self):
        """ Where due date is in the future. """
        future = date.today() + timedelta(1)
        new_due = date.today() + timedelta(8)

        self.todo.set_tag(config().tag_due(), future.isoformat())
        new_todo = advance_recurring_todo(self.todo, p_strict=True)

        self.assertEqual(new_todo.due_date(), new_due)

    def test_duedate6(self):
        """ Where due date is today. """
        today = date.today()
        new_due = date.today() + timedelta(7)

        self.todo.set_tag(config().tag_due(), today.isoformat())
        new_todo = advance_recurring_todo(self.todo, p_strict=True)

        self.assertEqual(new_todo.due_date(), new_due)

    def test_noduedate1(self):
        new_due = date.today() + timedelta(7)
        new_todo = advance_recurring_todo(self.todo)

        self.assertTrue(new_todo.has_tag(config().tag_due()))
        self.assertEqual(new_todo.due_date(), new_due)

    def test_noduedate2(self):
        new_due = date.today() + timedelta(7)
        new_todo = advance_recurring_todo(self.todo, p_strict=True)

        self.assertTrue(new_todo.has_tag(config().tag_due()))
        self.assertEqual(new_todo.due_date(), new_due)

    def test_startdate1(self):
        """ Start date is before due date. """
        self.todo.set_tag(config().tag_due(), date.today().isoformat())
        yesterday = date.today() - timedelta(1)
        self.todo.set_tag(config().tag_start(), yesterday.isoformat())

        new_start = date.today() + timedelta(6)
        new_todo = advance_recurring_todo(self.todo)

        self.assertEqual(new_todo.start_date(), new_start)

    def test_startdate2(self):
        """ Strict recurrence. Start date is before due date. """
        due = date.today() - timedelta(1)
        self.todo.set_tag(config().tag_due(), date.today().isoformat())
        yesterday = due - timedelta(1)
        # pylint: disable=E1103
        self.todo.set_tag(config().tag_start(), yesterday.isoformat())

        new_start = date.today() + timedelta(5)
        new_todo = advance_recurring_todo(self.todo, p_strict=True)

        self.assertEqual(new_todo.start_date(), new_start)

    def test_startdate3(self):
        """ Start date equals due date. """
        self.todo.set_tag(config().tag_due(), date.today().isoformat())
        self.todo.set_tag(config().tag_start(), date.today().isoformat())

        new_start = date.today() + timedelta(7)
        new_todo = advance_recurring_todo(self.todo)

        self.assertEqual(new_todo.start_date(), new_start)

    def test_strict_recurrence1(self):
        """
        Strict recurrence where due date is in the past, using + notation in
        expression.
        """
        past = date.today() - timedelta(8)
        new_due = date.today() - timedelta(1)

        self.stricttodo.set_tag(config().tag_due(), past.isoformat())
        new_todo = advance_recurring_todo(self.stricttodo, p_strict=True)

        self.assertEqual(new_todo.due_date(), new_due)

    def test_strict_recurrence2(self):
        """
        Strict recurrence where due date is in the future, using + notation in
        expression.
        """
        future = date.today() + timedelta(1)
        new_due = date.today() + timedelta(8)

        self.stricttodo.set_tag(config().tag_due(), future.isoformat())
        new_todo = advance_recurring_todo(self.stricttodo, p_strict=True)

        self.assertEqual(new_todo.due_date(), new_due)

    def test_no_recurrence(self):
        self.todo.remove_tag('rec')
        self.assertRaises(NoRecurrenceException, advance_recurring_todo,
                          self.todo)

    def test_invalid_recurrence(self):
        """ Throw exception when 'rec' tag has an invalid value. """
        self.todo.set_tag('rec', '1')
        self.assertRaises(NoRecurrenceException, advance_recurring_todo,
                          self.todo)

if __name__ == '__main__':
    unittest.main()
