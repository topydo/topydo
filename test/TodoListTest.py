""" Tests for the TodoList class. """

import datetime
import re
import unittest

import TodoFile
import TodoList

class TodoListTester(unittest.TestCase):
    def setUp(self):
        self.todofile = TodoFile.TodoFile('data/TodoListTest.txt')
        lines = [line for line in self.todofile.read() \
                       if re.search(r'\S', line)]
        self.text = ''.join(lines)
        self.todolist = TodoList.TodoList(lines)

    def test_contexts(self):
        self.assertEquals(set(['Context1', 'Context2']), \
            self.todolist.contexts())

    def test_projects(self):
        self.assertEquals(set(['Project1', 'Project2']), \
            self.todolist.projects())

    def test_add1(self):
        text = "(C) Adding a new task @Context3 +Project3"
        count = self.todolist.count()
        self.todolist.add(text)

        self.assertEquals(self.todolist.todo(count+1).source(), text)
        self.assertEquals(set(['Project1', 'Project2', 'Project3']), \
            self.todolist.projects())
        self.assertEquals(set(['Context1', 'Context2', 'Context3']), \
            self.todolist.contexts())

    def test_add2(self):
        text = str(self.todolist)
        self.todolist.add('')
        self.assertEquals(str(self.todolist), text)

    def test_add3a(self):
        count = self.todolist.count()
        self.todolist.add('\n(C) New task')

        self.assertEqual(self.todolist.count(), count + 1)
        self.assertEqual(self.todolist.todo(count + 1).source(), '(C) New task')
        self.assertEqual(self.todolist.todo(count + 1).priority(), 'C')

    def test_add3b(self):
        count = self.todolist.count()
        self.todolist.add('(C) New task\n')

        self.assertEqual(self.todolist.count(), count + 1)
        self.assertEqual(self.todolist.todo(count + 1).source(), '(C) New task')
        self.assertEqual(self.todolist.todo(count + 1).priority(), 'C')

    def test_add4(self):
        text = str(self.todolist)
        self.todolist.add(' ')
        self.assertEquals(str(self.todolist), text)

    def test_add5(self):
        text = str(self.todolist)
        self.todolist.add("\n")
        self.assertEquals(str(self.todolist), text)

    def test_delete1(self):
        count = self.todolist.count()
        self.todolist.delete(2)

        self.assertEquals(self.todolist.todo(2).source(), \
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

    def test_string(self):
        # readlines() always ends a string with \n, but join() in str(todolist)
        # doesn't necessarily.
        self.assertEquals(str(self.todolist) + '\n', self.text)

    def test_count(self):
        """ Test that empty lines are not counted. """
        self.assertEquals(self.todolist.count(), 5)

    def test_todo_by_dep_id(self):
        """ Tests that todos can be retrieved by their id tag. """
        self.todolist.add("(C) Foo id:1")

        self.assertTrue(self.todolist.todo_by_dep_id('1'))
        self.assertFalse(self.todolist.todo_by_dep_id('2'))

class TodoListDependencyTester(unittest.TestCase):
    def setUp(self):
        self.todolist = TodoList.TodoList([])
        self.todolist.add("Foo id:1")
        self.todolist.add("Bar p:1")
        self.todolist.add("Baz p:1 id:2")
        self.todolist.add("Buzz p:2")

    def test_check_dep(self):
        children = self.todolist.children(1)
        self.assertEqual([todo.source() for todo in children], \
            ['Bar p:1', 'Baz p:1 id:2', 'Buzz p:2'])

        children = self.todolist.children(1, True)
        self.assertEqual([todo.source() for todo in children], \
            ['Bar p:1', 'Baz p:1 id:2'])

        children = self.todolist.children(3)
        self.assertEqual([todo.source() for todo in children], \
            ['Buzz p:2'])

        parents = self.todolist.parents(4)
        self.assertEqual([todo.source() for todo in parents], \
            ['Foo id:1', 'Baz p:1 id:2'])

        parents = self.todolist.parents(4, True)
        self.assertEqual([todo.source() for todo in parents], \
            ['Baz p:1 id:2'])

        self.assertEqual(self.todolist.children(2), [])
        self.assertEqual(self.todolist.parents(1), [])

    def test_remove_dep1(self):
        self.todolist.remove_dependency(3, 4)

        self.assertFalse(self.todolist.todo(3).has_tag('id'))
        self.assertFalse(self.todolist.todo(4).has_tag('p'))

    def test_remove_dep2(self):
        old = str(self.todolist)
        self.todolist.remove_dependency(1, 4)

        self.assertEquals(str(self.todolist),old)

    def test_remove_task(self):
        self.todolist.delete(3)
        self.assertFalse(self.todolist.todo(3).has_tag('p', '2'))

        children = self.todolist.children(1)
        self.assertEqual([todo.source() for todo in children], \
            ['Bar p:1'])
