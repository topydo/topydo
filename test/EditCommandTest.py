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
import mock
from six import u

from topydo.commands.EditCommand import EditCommand
from test.CommandTest import CommandTest, utf8
from topydo.lib.TodoList import TodoList
from topydo.lib.Todo import Todo

class EditCommandTest(CommandTest):
    def setUp(self):
        super(EditCommandTest, self).setUp()
        todos = [
            "Foo id:1",
            "Bar p:1 @test",
            "Baz @test",
            u("Fo\u00f3B\u0105\u017a"),
        ]

        self.todolist = TodoList(todos)


    @mock.patch('topydo.commands.EditCommand.EditCommand._open_in_editor')
    def test_edit1(self, mock_open_in_editor):
        """ Preserve dependencies after editing. """
        mock_open_in_editor.return_value = 0

        command = EditCommand(["1"], self.todolist, self.out, self.error, None)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEqual(self.errors, "")
        self.assertEqual(str(self.todolist), utf8(u("Bar p:1 @test\nBaz @test\nFo\u00f3B\u0105\u017a\nFoo id:1")))

    @mock.patch('topydo.commands.EditCommand.EditCommand._todos_from_temp')
    @mock.patch('topydo.commands.EditCommand.EditCommand._open_in_editor')
    def test_edit2(self, mock_open_in_editor, mock_todos_from_temp):
        """ Edit some todo. """
        mock_open_in_editor.return_value = 0
        mock_todos_from_temp.return_value = [Todo('Lazy Cat')]

        command = EditCommand(["Bar"], self.todolist, self.out, self.error, None)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEqual(self.errors, "")
        self.assertEqual(str(self.todolist), utf8(u("Foo id:1\nBaz @test\nFo\u00f3B\u0105\u017a\nLazy Cat")))

    def test_edit3(self):
        """ Throw an error after invalid todo number given as argument. """
        command = EditCommand(["FooBar"], self.todolist, self.out, self.error, None)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_edit4(self):
        """ Throw an error with pointing invalid argument. """
        command = EditCommand(["Bar", "5"], self.todolist, self.out, self.error, None)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.errors, "Invalid todo number given: 5.\n")

    @mock.patch('topydo.commands.EditCommand.EditCommand._todos_from_temp')
    @mock.patch('topydo.commands.EditCommand.EditCommand._open_in_editor')
    def test_edit5(self, mock_open_in_editor, mock_todos_from_temp):
        """ Don't let to delete todos acidentally while editing. """
        mock_open_in_editor.return_value = 0
        mock_todos_from_temp.return_value = [Todo('Only one line')]

        command = EditCommand(["1", "Bar"], self.todolist, self.out, self.error, None)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.errors, "Number of edited todos is not equal to number of supplied todo IDs.\n")
        self.assertEqual(str(self.todolist), utf8(u("Foo id:1\nBar p:1 @test\nBaz @test\nFo\u00f3B\u0105\u017a")))

    def test_edit6(self):
        """ Throw an error with invalid argument containing special characters. """
        command = EditCommand([u("Fo\u00d3B\u0105r"), "Bar"], self.todolist, self.out, self.error, None)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.errors, u("Invalid todo number given: Fo\u00d3B\u0105r.\n"))

    @mock.patch('topydo.commands.EditCommand.EditCommand._todos_from_temp')
    @mock.patch('topydo.commands.EditCommand.EditCommand._open_in_editor')
    def test_edit7(self, mock_open_in_editor, mock_todos_from_temp):
        """ Edit todo with special characters. """
        mock_open_in_editor.return_value = 0
        mock_todos_from_temp.return_value = [Todo('Lazy Cat')]

        command = EditCommand([u("Fo\u00f3B\u0105\u017a")], self.todolist, self.out, self.error, None)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEqual(self.errors, "")
        self.assertEqual(str(self.todolist), utf8(u("Foo id:1\nBar p:1 @test\nBaz @test\nLazy Cat")))


    @mock.patch('topydo.commands.EditCommand.EditCommand._todos_from_temp')
    @mock.patch('topydo.commands.EditCommand.EditCommand._open_in_editor')
    def test_edit_expr(self, mock_open_in_editor, mock_todos_from_temp):
        """ Edit todos matching expression. """
        mock_open_in_editor.return_value = 0
        mock_todos_from_temp.return_value = [Todo('Lazy Cat'), Todo('Lazy Dog')]

        command = EditCommand(["-e", "@test"], self.todolist, self.out, self.error, None)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEqual(self.errors, "")
        self.assertEqual(str(self.todolist), utf8(u("Foo id:1\nFo\u00f3B\u0105\u017a\nLazy Cat\nLazy Dog")))

if __name__ == '__main__':
    unittest.main()
