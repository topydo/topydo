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

import os
import unittest

from six import u

from test.command_testcase import CommandTest
from topydo.commands.EditCommand import EditCommand
from topydo.lib.Config import config
from topydo.lib.Todo import Todo
from topydo.lib.TodoList import TodoList

# We're searching for 'mock'
# pylint: disable=no-name-in-module
try:
    from unittest import mock
except ImportError:
    import mock


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

    @mock.patch('topydo.commands.EditCommand._is_edited')
    @mock.patch('topydo.commands.EditCommand.EditCommand._todos_from_temp')
    @mock.patch('topydo.commands.EditCommand.EditCommand._open_in_editor')
    def test_edit01(self, mock_open_in_editor, mock_todos_from_temp, mock_is_edited):
        """ Preserve dependencies after editing. """
        mock_open_in_editor.return_value = 0
        mock_todos_from_temp.return_value = [Todo('Foo id:1')]
        mock_is_edited.return_value = True

        command = EditCommand(["1"], self.todolist, self.out, self.error, None)
        command.execute()

        self.assertEqual(self.errors, "")
        self.assertTrue(self.todolist.is_dirty())
        self.assertEqual(self.todolist.print_todos(), u("Bar p:1 @test\nBaz @test\nFo\u00f3B\u0105\u017a\nFoo id:1"))

    @mock.patch('topydo.commands.EditCommand._is_edited')
    @mock.patch('topydo.commands.EditCommand.EditCommand._todos_from_temp')
    @mock.patch('topydo.commands.EditCommand.EditCommand._open_in_editor')
    def test_edit02(self, mock_open_in_editor, mock_todos_from_temp, mock_is_edited):
        """ Edit some todo. """
        mock_open_in_editor.return_value = 0
        mock_todos_from_temp.return_value = [Todo('Lazy Cat')]
        mock_is_edited.return_value = True

        command = EditCommand(["Bar"], self.todolist, self.out, self.error,
                              None)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEqual(self.errors, "")
        self.assertEqual(self.todolist.print_todos(), u("Foo id:1\nBaz @test\nFo\u00f3B\u0105\u017a\nLazy Cat"))

    def test_edit03(self):
        """ Throw an error after invalid todo number given as argument. """
        command = EditCommand(["FooBar"], self.todolist, self.out, self.error,
                              None)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_edit04(self):
        """ Throw an error with pointing invalid argument. """
        command = EditCommand(["Bar", "5"], self.todolist, self.out,
                              self.error, None)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.errors, "Invalid todo number given: 5.\n")

    def test_edit05(self):
        """
        Throw an error with invalid argument containing special characters.
        """
        command = EditCommand([u("Fo\u00d3B\u0105r"), "Bar"], self.todolist,
                              self.out, self.error, None)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.errors,
                         u("Invalid todo number given: Fo\u00d3B\u0105r.\n"))

    @mock.patch('topydo.commands.EditCommand._is_edited')
    @mock.patch('topydo.commands.EditCommand.EditCommand._todos_from_temp')
    @mock.patch('topydo.commands.EditCommand.EditCommand._open_in_editor')
    def test_edit06(self, mock_open_in_editor, mock_todos_from_temp, mock_is_edited):
        """ Edit todo with special characters. """
        mock_open_in_editor.return_value = 0
        mock_todos_from_temp.return_value = [Todo('Lazy Cat')]
        mock_is_edited.return_value = True

        command = EditCommand([u("Fo\u00f3B\u0105\u017a")], self.todolist,
                              self.out, self.error, None)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEqual(self.errors, "")
        self.assertEqual(self.todolist.print_todos(),
                         u("Foo id:1\nBar p:1 @test\nBaz @test\nLazy Cat"))

    @mock.patch('topydo.commands.EditCommand._is_edited')
    @mock.patch('topydo.commands.EditCommand.EditCommand._todos_from_temp')
    @mock.patch('topydo.commands.EditCommand.EditCommand._open_in_editor')
    def test_edit07(self, mock_open_in_editor, mock_todos_from_temp, mock_is_edited):
        """ Don't perform write if tempfile is unchanged """
        mock_open_in_editor.return_value = 0
        mock_todos_from_temp.return_value = [Todo('Only one line')]
        mock_is_edited.return_value = False

        command = EditCommand(["1", "Bar"], self.todolist, self.out,
                              self.error, None)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.errors, "Editing aborted. Nothing to do.\n")
        self.assertEqual(self.todolist.print_todos(), u("Foo id:1\nBar p:1 @test\nBaz @test\nFo\u00f3B\u0105\u017a"))

    @mock.patch('topydo.commands.EditCommand._is_edited')
    @mock.patch('topydo.commands.EditCommand.EditCommand._todos_from_temp')
    @mock.patch('topydo.commands.EditCommand.EditCommand._open_in_editor')
    def test_edit_expr(self, mock_open_in_editor, mock_todos_from_temp, mock_is_edited):
        """ Edit todos matching expression. """
        mock_open_in_editor.return_value = 0
        mock_todos_from_temp.return_value = [Todo('Lazy Cat'),
                                             Todo('Lazy Dog')]
        mock_is_edited.return_value = True

        command = EditCommand(["-e", "@test"], self.todolist, self.out,
                              self.error, None)
        command.execute()

        expected = u("|  3| Lazy Cat\n|  4| Lazy Dog\n")

        self.assertEqual(self.errors, "")
        self.assertTrue(self.todolist.is_dirty())
        self.assertEqual(self.output, expected)
        self.assertEqual(self.todolist.print_todos(), u("Foo id:1\nFo\u00f3B\u0105\u017a\nLazy Cat\nLazy Dog"))

    @mock.patch('topydo.commands.EditCommand.check_call')
    def test_edit_archive(self, mock_call):
        """ Edit archive file. """
        mock_call.return_value = 0

        editor = 'vi'
        os.environ['EDITOR'] = editor
        archive = config().archive()

        command = EditCommand(["-d"], self.todolist, self.out, self.error,
                              None)
        command.execute()

        self.assertEqual(self.errors, "")
        mock_call.assert_called_once_with([editor, archive])

    @mock.patch('topydo.commands.EditCommand.check_call')
    def test_edit_todotxt(self, mock_call):
        """ Edit todo file. """
        mock_call.return_value = 0

        editor = 'vi'
        os.environ['EDITOR'] = editor
        todotxt = config().todotxt()

        result = self.todolist.print_todos()  # copy TodoList content *before* executing command

        command = EditCommand([], self.todolist, self.out, self.error, None)
        command.execute()

        self.assertEqual(self.errors, "")
        self.assertEqual(self.todolist.print_todos(), result)
        mock_call.assert_called_once_with([editor, todotxt])

    def test_help(self):
        command = EditCommand(["help"], self.todolist, self.out, self.error,
                              None)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors,
                         command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
