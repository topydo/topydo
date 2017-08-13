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

from topydo.commands.DepriCommand import DepriCommand
from topydo.lib.TodoList import TodoList

from .command_testcase import CommandTest


class DepriCommandTest(CommandTest):
    def setUp(self):
        super().setUp()
        todos = [
            "(A) Foo",
            "Bar",
            "(B) Baz",
            "(E) a @test with due:2015-06-03",
            "(Z) a @test with +project p:1",
            "(D) Bax id:1",
        ]

        self.todolist = TodoList(todos)

    def test_depri1(self):
        command = DepriCommand(["1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.todolist.todo(1).priority(), None)
        self.assertEqual(self.output, "Priority removed.\n|  1| Foo\n")
        self.assertEqual(self.errors, "")

    def test_depri2(self):
        command = DepriCommand(["2"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.todolist.todo(2).priority(), None)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_depri3(self):
        command = DepriCommand(["Foo"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.todolist.todo(1).priority(), None)
        self.assertEqual(self.output, "Priority removed.\n|  1| Foo\n")
        self.assertEqual(self.errors, "")

    def test_depri4(self):
        command = DepriCommand(["1", "Baz"], self.todolist, self.out,
                               self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.todolist.todo(1).priority(), None)
        self.assertEqual(self.todolist.todo(3).priority(), None)
        self.assertEqual(self.output, "Priority removed.\n|  1| Foo\nPriority removed.\n|  3| Baz\n")
        self.assertEqual(self.errors, "")

    def test_expr_depri1(self):
        command = DepriCommand(["-e", "@test"], self.todolist, self.out,
                               self.error, None)
        command.execute()

        result = "Priority removed.\n|  4| a @test with due:2015-06-03\nPriority removed.\n|  5| a @test with +project p:1\n"

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, result)
        self.assertEqual(self.errors, "")

    def test_expr_depri2(self):
        command = DepriCommand(["-e", "@test", "due:2015-06-03"],
                               self.todolist, self.out, self.error, None)
        command.execute()

        result = "Priority removed.\n|  4| a @test with due:2015-06-03\n"

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, result)
        self.assertEqual(self.errors, "")

    def test_expr_depri3(self):
        command = DepriCommand(["-e", "@test", "due:2015-06-03", "+project"],
                               self.todolist, self.out, self.error, None)
        command.execute()

        self.assertFalse(self.todolist.dirty)

    def test_expr_depri4(self):
        """ Don't remove priority from unrelevant todo items. """
        command = DepriCommand(["-e", "Bax"], self.todolist, self.out,
                               self.error, None)
        command.execute()

        self.assertFalse(self.todolist.dirty)

    def test_expr_depri5(self):
        """ Force unprioritizing unrelevant items with additional -x flag. """
        command = DepriCommand(["-xe", "Bax"], self.todolist, self.out,
                               self.error, None)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, "Priority removed.\n|  6| Bax id:1\n")
        self.assertEqual(self.errors, "")

    def test_invalid1(self):
        command = DepriCommand(["99"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertFalse(self.output)
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_invalid2(self):
        command = DepriCommand(["99", "1"], self.todolist, self.out,
                               self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertFalse(self.output)
        self.assertEqual(self.errors, "Invalid todo number given: 99.\n")

    def test_invalid3(self):
        command = DepriCommand(["99", "FooBar"], self.todolist, self.out,
                               self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertFalse(self.output)
        self.assertEqual(self.errors, "Invalid todo number given: 99.\nInvalid todo number given: FooBar.\n")

    def test_invalid4(self):
        """
        Throw an error with invalid argument containing special characters.
        """
        command = DepriCommand([u"Fo\u00d3B\u0105r", "Bar"], self.todolist,
                               self.out, self.error, None)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertFalse(self.output)
        self.assertEqual(self.errors,
                         u"Invalid todo number given: Fo\u00d3B\u0105r.\n")

    def test_empty(self):
        command = DepriCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertFalse(self.output)
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_depri_name(self):
        name = DepriCommand.name()

        self.assertEqual(name, 'depri')

    def test_help(self):
        command = DepriCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors,
                         command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
