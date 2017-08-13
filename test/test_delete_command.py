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

from topydo.commands.DeleteCommand import DeleteCommand
from topydo.lib.Config import config
from topydo.lib.TodoList import TodoList
from topydo.lib.TodoListBase import InvalidTodoException

from .command_testcase import CommandTest


def _yes_prompt(self):
    return "y"


def _no_prompt(self):
    return "n"


class DeleteCommandTest(CommandTest):
    def setUp(self):
        super().setUp()
        todos = [
            "Foo id:1",
            "Bar p:1",
            "a @test with due:2015-06-03",
            "a @test with +project",
        ]

        self.todolist = TodoList(todos)

    def test_del1(self):
        command = DeleteCommand(["1"], self.todolist, self.out, self.error,
                                _no_prompt)
        command.execute()
        command.execute_post_archive_actions()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.todolist.todo(1).source(), "Bar")
        self.assertEqual(self.output, "|  2| Bar p:1\nRemoved: Foo id:1\n")
        self.assertEqual(self.errors, "")

    def test_del1_regex(self):
        command = DeleteCommand(["Foo"], self.todolist, self.out, self.error,
                                _no_prompt)
        command.execute()
        command.execute_post_archive_actions()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.todolist.todo(1).source(), "Bar")
        self.assertEqual(self.output, "|  2| Bar p:1\nRemoved: Foo id:1\n")
        self.assertEqual(self.errors, "")

    def test_del2(self):
        command = DeleteCommand(["1"], self.todolist, self.out, self.error,
                                _yes_prompt)
        command.execute()
        command.execute_post_archive_actions()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.todolist.count(), 2)
        self.assertEqual(self.output,
                         "|  2| Bar p:1\nRemoved: Bar\nRemoved: Foo\n")
        self.assertEqual(self.errors, "")

    def test_del3(self):
        command = DeleteCommand(["-f", "1"], self.todolist, self.out,
                                self.error, _yes_prompt)
        command.execute()
        command.execute_post_archive_actions()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.todolist.count(), 3)  # force won't delete subtasks
        self.assertEqual(self.output, "|  2| Bar p:1\nRemoved: Foo id:1\n")
        self.assertEqual(self.errors, "")

    def test_del4(self):
        command = DeleteCommand(["--force", "1"], self.todolist, self.out,
                                self.error, _yes_prompt)
        command.execute()
        command.execute_post_archive_actions()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.todolist.count(), 3)  # force won't delete subtasks
        self.assertEqual(self.output, "|  2| Bar p:1\nRemoved: Foo id:1\n")
        self.assertEqual(self.errors, "")

    def test_del5(self):
        command = DeleteCommand(["2"], self.todolist, self.out, self.error)
        command.execute()
        command.execute_post_archive_actions()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.todolist.todo(1).source(), "Foo")
        self.assertEqual(self.output, "Removed: Bar p:1\nThe following todo item(s) became active:\n|  1| Foo\n")
        self.assertEqual(self.errors, "")

    def test_del7(self):
        command = DeleteCommand(["99"], self.todolist, self.out, self.error)
        command.execute()
        command.execute_post_archive_actions()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_del8(self):
        command = DeleteCommand(["A"], self.todolist, self.out, self.error)
        command.execute()
        command.execute_post_archive_actions()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_del9(self):
        """ Test deletion with textual IDs. """
        config("test/data/todolist-uid.conf")

        command = DeleteCommand(["8to"], self.todolist, self.out, self.error)
        command.execute()
        command.execute_post_archive_actions()

        result = "Foo\na @test with due:2015-06-03\na @test with +project"

        self.assertEqual(self.todolist.print_todos(), result)
        self.assertRaises(InvalidTodoException, self.todolist.todo, 'b0n')

    def test_multi_del1(self):
        """ Test deletion of multiple items. """
        command = DeleteCommand(["1", "2"], self.todolist, self.out,
                                self.error, _no_prompt)
        command.execute()
        command.execute_post_archive_actions()

        result = "a @test with due:2015-06-03\na @test with +project"

        self.assertEqual(self.todolist.count(), 2)
        self.assertEqual(self.todolist.print_todos(), result)

    def test_multi_del2(self):
        """ Test deletion of multiple items. """
        command = DeleteCommand(["1", "2"], self.todolist, self.out,
                                self.error, _yes_prompt)
        command.execute()
        command.execute_post_archive_actions()

        result = "a @test with due:2015-06-03\na @test with +project"

        self.assertEqual(self.todolist.count(), 2)
        self.assertEqual(self.todolist.print_todos(), result)

    def test_multi_del3(self):
        """  Fail if any of supplied todo numbers is invalid. """
        command = DeleteCommand(["99", "2"], self.todolist, self.out,
                                self.error, _yes_prompt)
        command.execute()
        command.execute_post_archive_actions()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given: 99.\n")

    def test_multi_del4(self):
        """  Check output when all supplied todo numbers are invalid. """
        command = DeleteCommand(["99", "A"], self.todolist, self.out,
                                self.error, _yes_prompt)
        command.execute()
        command.execute_post_archive_actions()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given: 99.\nInvalid todo number given: A.\n")

    def test_multi_del5(self):
        """
        Throw an error with invalid argument containing special characters.
        """
        command = DeleteCommand([u"Fo\u00d3B\u0105r", "Bar"], self.todolist,
                                self.out, self.error, None)
        command.execute()
        command.execute_post_archive_actions()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors,
                         u"Invalid todo number given: Fo\u00d3B\u0105r.\n")

    def test_expr_del1(self):
        command = DeleteCommand(["-e", "@test"], self.todolist, self.out,
                                self.error, None)
        command.execute()
        command.execute_post_archive_actions()

        result = "Removed: a @test with due:2015-06-03\nRemoved: a @test with +project\n"

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.todolist.count(), 2)
        self.assertEqual(self.output, result)
        self.assertEqual(self.errors, "")

    def test_expr_del2(self):
        command = DeleteCommand(["-e", "@test", "due:2015-06-03"],
                                self.todolist, self.out, self.error, None)
        command.execute()
        command.execute_post_archive_actions()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, "Removed: a @test with due:2015-06-03\n")
        self.assertEqual(self.errors, "")

    def test_expr_del3(self):
        command = DeleteCommand(["-e", "@test", "due:2015-06-03", "+project"],
                                self.todolist, self.out, self.error, None)
        command.execute()
        command.execute_post_archive_actions()

        self.assertFalse(self.todolist.dirty)

    def test_expr_del4(self):
        """ Remove only relevant todo items. """
        command = DeleteCommand(["-e", ""], self.todolist, self.out,
                                self.error, None)
        command.execute()
        command.execute_post_archive_actions()

        result = "Foo"

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.todolist.count(), 1)
        self.assertEqual(self.todolist.print_todos(), result)

    def test_expr_del5(self):
        """ Force deleting unrelevant items with additional -x flag. """
        command = DeleteCommand(["-xe", ""], self.todolist, self.out,
                                self.error, _yes_prompt)
        command.execute()
        command.execute_post_archive_actions()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.todolist.count(), 0)

    def test_empty(self):
        command = DeleteCommand([], self.todolist, self.out, self.error)
        command.execute()
        command.execute_post_archive_actions()

        self.assertFalse(self.todolist.dirty)
        self.assertFalse(self.output)
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_delete_name(self):
        name = DeleteCommand.name()

        self.assertEqual(name, 'delete')

    def test_help(self):
        command = DeleteCommand(["help"], self.todolist, self.out, self.error)
        command.execute()
        command.execute_post_archive_actions()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors,
                         command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
