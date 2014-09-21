from datetime import date, timedelta
import unittest

import Todo

def today_date():
    today = date.today()
    return today.isoformat()

def tomorrow_date():
    tomorrow = date.today() + timedelta(days=1)
    return tomorrow.isoformat()

class TodoTest(unittest.TestCase):
    def test_due_date1(self):
        todo = Todo.Todo("(C) Foo due:2014-06-09")
        due = date(2014, 6, 9)

        self.assertEqual(todo.due_date(), due)

    def test_false_date(self):
        todo = Todo.Todo("(C) Foo due:2014-04-31")
        self.assertEqual( todo.due_date(), None )

    def test_active1(self):
        todo = Todo.Todo("(C) Foo due:2014-01-01")
        self.assertTrue(todo.is_active())

    def test_active2(self):
        todo = Todo.Todo("(C) Foo t:" + tomorrow_date())
        self.assertFalse(todo.is_active())

    def test_active3(self):
        todo = Todo.Todo("x 2014-06-09 Foo t:2014-01-01")
        self.assertFalse(todo.is_active())

    def test_active4(self):
        todo = Todo.Todo("(C) Foo t:" + today_date())
        self.assertTrue(todo.is_active())

    def test_active5(self):
        todo = Todo.Todo("(C) Foo t:2014-02-29")
        self.assertTrue(todo.is_active())

    def test_overdue1(self):
        todo = Todo.Todo("(C) Foo due:2014-01-01")
        self.assertTrue(todo.is_overdue())

    def test_overdue2(self):
        todo = Todo.Todo("(C) Foo due:" + tomorrow_date())
        self.assertFalse(todo.is_overdue())

    def test_overdue3(self):
        todo = Todo.Todo("(C) Foo due:" + today_date())
        self.assertFalse(todo.is_overdue())

    def days_till_due(self):
        todo = Todo.Todo("(C) due:" + tomorrow_date())
        self.assertEqual(todo.days_till_due(), 1)

    def test_length1(self):
        todo = Todo.Todo("(C) Foo t:2014-01-01 due:2013-12-31")
        self.assertEqual(todo.length(), 0)

    def test_length2(self):
        todo = Todo.Todo("(C) Foo t:2014-01-01 due:2014-01-01")
        self.assertEqual(todo.length(), 0)

    def test_length3(self):
        todo = Todo.Todo("(C) Foo t:2014-01-01 due:2014-01-02")
        self.assertEqual(todo.length(), 1)
