from datetime import date
import unittest

import Config
from Importance import importance
import Todo

class ImportanceTest(unittest.TestCase):
    def test_importance1(self):
        todo = Todo.Todo("Foo")
        self.assertEqual(importance(todo), 2)

    def test_importance2(self):
        todo = Todo.Todo("(A) Foo")
        self.assertEqual(importance(todo), 5)

    def test_importance3(self):
        todo = Todo.Todo("(A) Foo " + Config.TAG_STAR + ":1")
        self.assertEqual(importance(todo), 6)

    def test_importance4(self):
        today_str = date.today().isoformat()
        todo = Todo.Todo("(C) Foo " + Config.TAG_DUE + ":" + today_str)
        self.assertEqual(importance(todo), 8)
