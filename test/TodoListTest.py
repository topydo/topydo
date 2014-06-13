""" Tests for the TodoList class. """

import datetime
import unittest

import TodoFile
import TodoList

class TodoListTester(unittest.TestCase):
    def setUp(self):
        self.todofile = TodoFile.TodoFile('TodoListTest.txt')
        lines = self.todofile.read()
        self.text = ''.join(lines)
        self.todolist = TodoList.TodoList(lines)

    def test_contexts(self):
        self.assertEquals(set(['Context1', 'Context2']), \
            self.todolist.contexts())

    def test_projects(self):
        self.assertEquals(set(['Project1', 'Project2']), \
            self.todolist.projects())

    def test_add(self):
        text = "(C) Adding a new task @Context3 +Project3"
        self.todolist.add(text)

        self.assertEquals(self.todolist.todo(6).src, text)
        self.assertEquals(set(['Project1', 'Project2', 'Project3']), \
            self.todolist.projects())
        self.assertEquals(set(['Context1', 'Context2', 'Context3']), \
            self.todolist.contexts())

    def test_delete1(self):
        count = self.todolist.count()
        self.todolist.delete(2)

        self.assertEquals(self.todolist.todo(2).src, \
            "(C) Baz @Context1 +Project1 key:value")
        self.assertEquals(self.todolist.count(), count - 1)

    def test_delete2(self):
        count = self.todolist.count()
        self.todolist.delete(count + 1)

        self.assertEquals(self.todolist.count(), count)

    def test_append1(self):
        self.todolist.append(3, "@Context3")

        self.assertEquals(self.todolist.todo(3).source(), \
            "(C) Baz @Context1 +Project1 key:value @Context3")
        self.assertEquals(set(['Context1', 'Context2', 'Context3']), \
            self.todolist.contexts())

    def test_append2(self):
        text = self.todolist.todo(3).text()
        self.todolist.append(3, "foo:bar")

        self.assertEquals(self.todolist.todo(3).text(), text)
        self.assertEquals(self.todolist.todo(3).source(), \
            "(C) Baz @Context1 +Project1 key:value foo:bar")

    def test_append3(self):
        text = self.todolist.todo(3).text()
        self.todolist.append(3, '')

        self.assertEquals(self.todolist.todo(3).text(), text)

    def test_todo(self):
        count = self.todolist.count()
        todo = self.todolist.todo(count+100)

        self.assertEquals(todo, None)

    def test_completed(self):
        self.todolist.todo(1).set_completed()
        today = datetime.date.today().isoformat()

        self.assertTrue(self.todolist.todo(1).is_completed())
        self.assertEquals(self.todolist.todo(1).source(), \
            "x " + today + " Foo @Context1 Not@Context +Project1 Not+Project")

    def test_string(self):
        # readlines() always ends a string with \n, but join() in str(todolist)
        # doesn't necessarily.
        self.assertEquals(str(self.todolist) + '\n', self.text)

