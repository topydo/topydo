from datetime import date, timedelta
import unittest

import Config
from Recurrence import advance_recurring_todo, NoRecurrenceException
import Todo

class RelativeDateTester(unittest.TestCase):
    def setUp(self):
        self.todo = Todo.Todo("Test rec:1w")

    def test_duedate1(self):
        """ Where due date is in the future. """
        future = date.today() + timedelta(1)
        new_due = date.today() + timedelta(8)

        self.todo.set_tag(Config.TAG_DUE, future.isoformat())
        new_todo = advance_recurring_todo(self.todo)

        self.assertEquals(new_todo.due_date(), new_due)

    def test_duedate2(self):
        """ Where due date is today. """
        todo = date.today()
        new_due = date.today() + timedelta(7)

        self.todo.set_tag(Config.TAG_DUE, todo.isoformat())
        new_todo = advance_recurring_todo(self.todo)

        self.assertEquals(new_todo.due_date(), new_due)

    def test_duedate3(self):
        """ Where due date is in the past. """
        past = date.today() - timedelta(8)
        new_due = date.today() + timedelta(7)

        self.todo.set_tag(Config.TAG_DUE, past.isoformat())
        new_todo = advance_recurring_todo(self.todo)

        self.assertEquals(new_todo.due_date(), new_due)

    def test_noduedate(self):
        new_due = date.today() + timedelta(7)
        new_todo = advance_recurring_todo(self.todo)

        self.assertTrue(new_todo.has_tag(Config.TAG_DUE))
        self.assertEquals(new_todo.due_date(), new_due)

    def test_startdate(self):
        """ Start date is before due date. """
        self.todo.set_tag(Config.TAG_DUE, date.today().isoformat())
        yesterday = date.today() - timedelta(1)
        self.todo.set_tag(Config.TAG_START, yesterday.isoformat())

        new_start = date.today() + timedelta(6)
        new_todo = advance_recurring_todo(self.todo)

        self.assertEquals(new_todo.start_date(), new_start)

    def test_startdate2(self):
        """ Start date equals due date. """
        self.todo.set_tag(Config.TAG_DUE, date.today().isoformat())
        self.todo.set_tag(Config.TAG_START, date.today().isoformat())

        new_start = date.today() + timedelta(7)
        new_todo = advance_recurring_todo(self.todo)

        self.assertEquals(new_todo.start_date(), new_start)

    def test_no_recurrence(self):
        self.todo.remove_tag('rec')
        self.assertRaises(NoRecurrenceException,advance_recurring_todo,self.todo)
