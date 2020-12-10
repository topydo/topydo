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

""" Tests for the TodoList class. """

import re
import unittest

from topydo.lib.Config import config
from topydo.lib.Todo import Todo
from topydo.lib.TodoFile import TodoFile
from topydo.lib.TodoList import TodoList
from topydo.lib.TodoListBase import InvalidTodoException, TodoListBase

from .topydo_testcase import TopydoTest


class TodoListTester(TopydoTest):
    def setUp(self):
        super().setUp()

        self.todofile = TodoFile('test/data/TodoListTest.txt')
        lines = [line for line in self.todofile.read()
                 if re.search(r'\S', line)]
        self.text = ''.join(lines)
        self.todolist = TodoListBase(lines)

    def test_contexts(self):
        self.assertEqual(set(['Context1', 'Context2']),
                         self.todolist.contexts())
        self.assertFalse(self.todolist.dirty)

    def test_projects(self):
        self.assertEqual(set(['Project1', 'Project2']),
                         self.todolist.projects())
        self.assertFalse(self.todolist.dirty)

    def test_add1(self):
        text = "(C) Adding a new task @Context3 +Project3"
        count = self.todolist.count()
        todo = self.todolist.add(text)

        self.assertEqual(self.todolist.todo(count+1).source(), text)
        self.assertEqual(set(['Project1', 'Project2', 'Project3']),
                         self.todolist.projects())
        self.assertEqual(set(['Context1', 'Context2', 'Context3']),
                         self.todolist.contexts())
        self.assertEqual(self.todolist.number(todo), 6)
        self.assertTrue(self.todolist.dirty)

    def test_add2(self):
        text = str(self.todolist)
        self.todolist.add('')
        self.assertEqual(str(self.todolist), text)

    def test_add3a(self):
        count = self.todolist.count()
        self.todolist.add('\n(C) New task')

        self.assertEqual(self.todolist.count(), count + 1)
        self.assertEqual(self.todolist.todo(count + 1).source(),
                         '(C) New task')
        self.assertEqual(self.todolist.todo(count + 1).priority(), 'C')

    def test_add3b(self):
        count = self.todolist.count()
        self.todolist.add('(C) New task\n')

        self.assertEqual(self.todolist.count(), count + 1)
        self.assertEqual(self.todolist.todo(count + 1).source(),
                         '(C) New task')
        self.assertEqual(self.todolist.todo(count + 1).priority(), 'C')

    def test_add4(self):
        text = str(self.todolist)
        self.todolist.add(' ')
        self.assertEqual(str(self.todolist), text)

    def test_add5(self):
        text = str(self.todolist)
        self.todolist.add("\n")
        self.assertEqual(str(self.todolist), text)

    def test_delete1(self):
        count = self.todolist.count()
        todo = self.todolist.todo(2)
        self.todolist.delete(todo)

        self.assertEqual(self.todolist.todo(2).source(),
                         "(C) Baz @Context1 +Project1 key:value")
        self.assertEqual(self.todolist.count(), count - 1)
        self.assertTrue(self.todolist.dirty)
        self.assertRaises(InvalidTodoException, self.todolist.number, todo)

    def test_delete2(self):
        """ Try to remove a todo item that does not exist. """
        count = self.todolist.count()

        todo = Todo('Not in the list')
        self.todolist.delete(todo)

        self.assertEqual(self.todolist.count(), count)
        self.assertFalse(self.todolist.dirty)

    def test_append1(self):
        todo = self.todolist.todo(3)
        self.todolist.append(todo, "@Context3")

        self.assertEqual(todo.source(),
                         "(C) Baz @Context1 +Project1 key:value @Context3")
        self.assertEqual(set(['Context1', 'Context2', 'Context3']),
                         self.todolist.contexts())
        self.assertTrue(self.todolist.dirty)

    def test_append2(self):
        todo = self.todolist.todo(3)
        text = todo.text()
        self.todolist.append(todo, "foo:bar")

        self.assertEqual(todo.text(), text)
        self.assertEqual(todo.source(),
                         "(C) Baz @Context1 +Project1 key:value foo:bar")

    def test_append3(self):
        todo = self.todolist.todo(3)
        text = todo.text()
        self.todolist.append(todo, '')

        self.assertEqual(todo.text(), text)

    def test_todo(self):
        count = self.todolist.count()

        self.assertRaises(InvalidTodoException, self.todolist.todo,
                          count + 100)
        self.assertFalse(self.todolist.dirty)

    def test_count(self):
        """ Test that empty lines are not counted. """
        self.assertEqual(self.todolist.count(), 5)

    def test_todo_number1(self):
        todo = Todo("No number")
        self.todolist.add_todo(todo)

        todo = self.todolist.todo(6)
        self.assertIsInstance(todo, Todo)
        self.assertEqual(todo.text(), "No number")

    def test_todo_number2(self):
        todo = Todo("Non-existent")
        self.assertRaises(InvalidTodoException, self.todolist.number, todo)

    def test_todo_complete(self):
        todo = self.todolist.todo(1)
        self.todolist.set_todo_completed(todo)
        self.assertTrue(self.todolist.todo(1).is_completed())
        self.assertTrue(self.todolist.dirty)

    def test_todo_priority1(self):
        todo = self.todolist.todo(1)
        self.todolist.set_priority(todo, 'F')

        self.assertEqual(self.todolist.todo(1).priority(), 'F')
        self.assertTrue(self.todolist.dirty)

    def test_todo_priority2(self):
        todo = self.todolist.todo(1)
        self.todolist.set_priority(todo, 'C')

        self.assertFalse(self.todolist.dirty)

    def test_erase(self):
        self.todolist.erase()

        self.assertEqual(self.todolist.count(), 0)
        self.assertTrue(self.todolist.dirty)

    def test_regex1(self):
        """ Multiple hits should result in None. """
        self.assertRaises(InvalidTodoException, self.todolist.todo, "Project1")

    def test_regex3(self):
        todo = self.todolist.todo("project2")
        self.assertTrue(todo)
        self.assertEqual(todo.source(), "(D) Bar @Context1 +Project2")

    def test_uid1(self):
        config("test/data/todolist-uid.conf")

        self.assertEqual(self.todolist.todo('t5c').source(),
                         "(C) Foo @Context2 Not@Context +Project1 Not+Project")

    def test_uid2(self):
        """ Changing the priority should not change the identifier. """
        config("test/data/todolist-uid.conf")

        todo = self.todolist.todo('t5c')
        self.todolist.set_priority(todo, 'B')
        self.assertEqual(self.todolist.todo('t5c').source(),
                         "(B) Foo @Context2 Not@Context +Project1 Not+Project")

    def test_uid3(self):
        """
        Must be able to handle integers when text identifiers are enabled.
        """
        config("test/data/todolist-uid.conf")
        self.assertRaises(InvalidTodoException, self.todolist.todo, 1)

    def test_uid4(self):
        """
        Handle UIDs properly when line numbers are configured.
        """
        config(p_overrides={('topydo', 'identifiers'): 'linenumber'})
        self.assertRaises(InvalidTodoException, self.todolist.todo, '11a')

    def test_uid5(self):
        """ Handle bogus UIDs """
        todo = Todo('invalid')
        self.assertRaises(InvalidTodoException, self.todolist.uid, todo)

    def test_new_uid(self):
        """ Make sure that item has new text ID after append. """
        config("test/data/todolist-uid.conf")
        todo = self.todolist.todo('t5c')
        self.todolist.append(todo, "A")

        self.assertNotEqual(self.todolist.number(todo), 't5c')

    def test_iteration(self):
        """ Confirms that the iternation method is working. """
        results = ["(C) Foo @Context2 Not@Context +Project1 Not+Project",
                   "(D) Bar @Context1 +Project2",
                   "(C) Baz @Context1 +Project1 key:value",
                   "(C) Drink beer @ home",
                   "(C) 13 + 29 = 42"]

        i = 0
        for todo in self.todolist:
            self.assertEqual(todo.src, results[i])
            i += 1

    def test_ids_linenumber(self):
        """ Confirms the ids method lists all todo IDs as line-numbers. """
        config(p_overrides={('topydo', 'identifiers'): 'linenumber'})
        results = {'1', '2', '3', '4', '5'}

        self.assertEqual(results, self.todolist.ids())

    def test_ids_uids(self):
        """ Confirms the ids method lists all todo IDs as text uids. """
        config("test/data/todolist-uid.conf")
        results = {'n8m', 'mfg', 'z63', 't5c', 'wa5'}

        self.assertEqual(results, self.todolist.ids())


class TodoListDependencyTester(TopydoTest):
    def setUp(self):
        super().setUp()

        self.todolist = TodoList([])
        self.todolist.add("Foo id:1")
        self.todolist.add("Bar p:1")
        self.todolist.add("Baz p:1 id:2")
        self.todolist.add("Buzz p:2")
        self.todolist.add("Fnord")
        self.todolist.add("Something with +Project")
        self.todolist.add("Another one with +Project")
        self.todolist.add("Todo with +AnotherProject")
        self.todolist.add("Todo without children id:3")
        self.todolist.add("Orphan p:4")

    def test_check_dep(self):
        children = self.todolist.children(self.todolist.todo(1))
        self.assertEqual(sorted([todo.source() for todo in children]),
                         sorted(['Bar p:1', 'Baz p:1 id:2', 'Buzz p:2']))

        children = self.todolist.children(self.todolist.todo(1), True)
        self.assertEqual(sorted([todo.source() for todo in children]),
                         sorted(['Bar p:1', 'Baz p:1 id:2']))

        children = self.todolist.children(self.todolist.todo(3))
        self.assertEqual(sorted([todo.source() for todo in children]),
                         ['Buzz p:2'])

        parents = self.todolist.parents(self.todolist.todo(4))
        self.assertEqual(sorted([todo.source() for todo in parents]),
                         sorted(['Foo id:1', 'Baz p:1 id:2']))

        parents = self.todolist.parents(self.todolist.todo(4), True)
        self.assertEqual(sorted([todo.source() for todo in parents]),
                         ['Baz p:1 id:2'])

        self.assertEqual(self.todolist.children(self.todolist.todo(2)), [])
        self.assertEqual(self.todolist.parents(self.todolist.todo(1)), [])

    def test_add_dep1(self):
        todo4 = self.todolist.todo(4)
        todo5 = self.todolist.todo(5)
        self.todolist.add_dependency(todo5, todo4)

        self.assertTrue(todo5.has_tag('id', '5'))
        self.assertTrue(todo4.has_tag('p', '5'))

    def test_add_dep2(self):
        """
        Make sure that previous add_dependency invocation stored the
        edge_id properly.
        """
        todo1 = self.todolist.todo(1)
        todo4 = self.todolist.todo(4)
        todo5 = self.todolist.todo(5)

        self.todolist.add_dependency(todo5, todo4)
        self.todolist.add_dependency(todo4, todo1)

        self.assertTrue(todo4.has_tag('id', '6'))
        self.assertTrue(todo1.has_tag('p', '6'))

    def test_add_dep3(self):
        """
        Test that projects are not added double.
        """
        todo6 = self.todolist.todo(6)
        todo7 = self.todolist.todo(7)
        projects = todo7.projects().copy()

        self.todolist.add_dependency(todo6, todo7)

        self.assertEqual(projects, todo7.projects())

    def test_add_dep4(self):
        """
        Test that a new project is added to the sub todo.
        """
        config("test/data/config3")

        todo6 = self.todolist.todo(6)
        todo8 = self.todolist.todo(8)

        self.todolist.add_dependency(todo6, todo8)

        self.assertEqual(set(["Project", "AnotherProject"]), todo8.projects())

    def test_remove_dep1(self):
        from_todo = self.todolist.todo(3)
        to_todo = self.todolist.todo(4)
        self.todolist.remove_dependency(from_todo, to_todo)

        self.assertFalse(from_todo.has_tag('id'))
        self.assertFalse(to_todo.has_tag('p'))
        self.assertFalse(self.todolist.todo_by_dep_id('2'))

    def test_remove_dep2(self):
        old = str(self.todolist)
        from_todo = self.todolist.todo(1)
        to_todo = self.todolist.todo(4)
        self.todolist.remove_dependency(from_todo, to_todo)

        self.assertEqual(str(self.todolist), old)
        self.assertTrue(self.todolist.todo_by_dep_id('1'))
        self.assertTrue(self.todolist.todo_by_dep_id('2'))
        self.assertTrue(self.todolist.todo_by_dep_id('3'))

    def test_remove_dep3(self):
        """ Try to remove non-existing dependency. """
        old = str(self.todolist)
        from_todo = self.todolist.todo(4)
        to_todo = self.todolist.todo(1)
        self.todolist.remove_dependency(from_todo, to_todo)

        self.assertEqual(str(self.todolist), old)
        self.assertTrue(self.todolist.todo_by_dep_id('1'))
        self.assertTrue(self.todolist.todo_by_dep_id('2'))
        self.assertTrue(self.todolist.todo_by_dep_id('3'))

    def test_remove_todo_check_children(self):
        todo = self.todolist.todo(2)
        self.todolist.delete(todo)

        todo = self.todolist.todo(2)
        self.assertTrue(self.todolist.children(todo))

    def test_remove_task(self):
        todo = self.todolist.todo(3)
        self.todolist.delete(todo)
        self.assertFalse(todo.has_tag('p', '2'))
        self.assertFalse(self.todolist.todo_by_dep_id('2'))

        todo = self.todolist.todo(1)
        children = self.todolist.children(todo)
        self.assertEqual([t.source() for t in children], ['Bar p:1'])

    def test_add_double_dep(self):
        todo1 = self.todolist.todo(1)
        todo2 = self.todolist.todo(2)
        self.todolist.add_dependency(todo1, todo2)

        self.assertEqual(todo1.source(), 'Foo id:1')
        self.assertEqual(todo2.source(), 'Bar p:1')

    def test_todo_by_dep_id(self):
        """ Tests that todos can be retrieved by their id tag. """
        todolist = TodoList([])
        todolist.add("(C) Foo id:1")

        self.assertTrue(todolist.todo_by_dep_id('1'))
        self.assertFalse(todolist.todo_by_dep_id('2'))

    def test_add_after_dependencies(self):
        """
        Test that information is properly stored after dependency related
        information was retrieved from the todo list.
        """
        todo = self.todolist.todo(1)
        self.todolist.parents(todo)

        self.todolist.add('New dependency id:99')
        self.todolist.add('Child p:99')

        self.assertTrue(self.todolist.dirty)
        self.assertTrue(self.todolist.todo_by_dep_id('99'))

    def test_delete01(self):
        """ Check that dependency tags are cleaned up. """
        todo = self.todolist.todo(4)
        self.todolist.delete(todo, p_leave_tags=False)

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.todolist.todo(3).source(), "Baz p:1")

    def test_delete02(self):
        """ Check that dependency tags are left when requested. """
        todo = self.todolist.todo(4)
        self.todolist.delete(todo, p_leave_tags=True)

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.todolist.todo(3).source(), "Baz p:1 id:2")

    def test_delete03(self):
        """ Check that dependency tags are left when requested. """
        todo = self.todolist.todo(3)
        self.todolist.delete(todo, p_leave_tags=True)

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.todolist.todo(3).source(), "Buzz p:2")


class TodoListCleanDependencyTester(TopydoTest):
    """
    Tests for cleaning up the graph:

    * Transitive reduction
    * Remove obsolete id: tags
    * Remove obsolete p: tags
    """

    def setUp(self):
        super().setUp()
        self.todolist = TodoList([])

    def test_clean_dependencies1(self):
        """ Clean p: tags from non-existing parent items. """
        self.todolist.add("Bar p:1")
        self.todolist.add("Baz p:1 id:2")
        self.todolist.add("Buzz p:2")

        self.todolist.clean_dependencies()

        self.assertFalse(self.todolist.todo(1).has_tag('p'))
        self.assertFalse(self.todolist.todo(2).has_tag('p'))
        self.assertTrue(self.todolist.todo(2).has_tag('id', '2'))
        self.assertTrue(self.todolist.todo(3).has_tag('p', '2'))

    def test_clean_dependencies2(self):
        """ Clean p: items when siblings are still connected to parent. """
        self.todolist.add("Foo id:1")
        self.todolist.add("Bar p:1")
        self.todolist.add("Baz p:1 id:2")
        self.todolist.add("Buzz p:1 p:2")

        self.todolist.clean_dependencies()

        self.assertFalse(self.todolist.todo(4).has_tag('p', '1'))
        self.assertTrue(self.todolist.todo(1).has_tag('id', '1'))
        self.assertTrue(self.todolist.todo(2).has_tag('p', '1'))

    def test_clean_dependencies3(self):
        """ Clean id: tags from todo items without child todos. """
        self.todolist.add("Foo id:1")

        self.todolist.clean_dependencies()

        self.assertFalse(self.todolist.todo(1).has_tag('id'))
        self.assertFalse(self.todolist.todo_by_dep_id('1'))


class TodoLoadTester(TopydoTest):
    """Test the auto_delete_whitespace configuration parameter"""
    def setUp(self):
        super().setUp()
        self.todoPath = 'test/data/TodoListTest.txt'
        self.todofile = TodoFile(self.todoPath)

    def test_load_default(self):
        todolist = TodoListBase(self.todofile.read())

        self.assertTrue(all([len(todo.source()) != 0 for todo in todolist]))

    def test_load_preserve_ws(self):
        config("test/data/listload.conf")
        todolist = TodoListBase(self.todofile.read())

        self.assertTrue(any([len(todo.source()) == 0 for todo in todolist]))

    def test_load_use_default(self):
        config("test/data/listload2.conf")
        todolist = TodoListBase(self.todofile.read())

        self.assertTrue(all([len(todo.source()) != 0 for todo in todolist]))


if __name__ == '__main__':
    unittest.main()
