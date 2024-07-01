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

from topydo.commands.PriorityCommand import PriorityCommand
from topydo.lib.TodoList import TodoList

from .command_testcase import CommandTest


class PriorityCommandTest(CommandTest):
    def setUp(self):
        super().setUp()
        todos = [
            "(A) Foo",
            "Bar",
            "(B) a @test with due:2015-06-03",
            "a @test with +project p:1",
            "Baz id:1",
        ]

        self.todolist = TodoList(todos)

    def test_set_prio1(self):
        command = PriorityCommand(["1", "B"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output,
                         "Priority changed from A to B\n|  1| (B) Foo\n")
        self.assertEqual(self.errors, "")

    def test_set_prio2(self):
        command = PriorityCommand(["2", "Z"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, "Priority set to Z.\n|  2| (Z) Bar\n")
        self.assertEqual(self.errors, "")

    def test_set_prio3(self):
        command = PriorityCommand(["Foo", "B"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output,
                         "Priority changed from A to B\n|  1| (B) Foo\n")
        self.assertEqual(self.errors, "")

    def test_set_prio4(self):
        command = PriorityCommand(["1", "A"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|  1| (A) Foo\n")
        self.assertEqual(self.errors, "")

    def test_set_prio5(self):
        command = PriorityCommand(["Foo", "2", "C"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, "Priority changed from A to C\n|  1| (C) Foo\nPriority set to C.\n|  2| (C) Bar\n")
        self.assertEqual(self.errors, "")

    def test_set_prio6(self):
        """ Allow priority to be set including parentheses. """
        command = PriorityCommand(["Foo", "2", "(C)"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, "Priority changed from A to C\n|  1| (C) Foo\nPriority set to C.\n|  2| (C) Bar\n")
        self.assertEqual(self.errors, "")

    def test_set_prio7(self):
        """ Allow lowercase priority to be set. """
        command = PriorityCommand(["Foo", "2", "c"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, "Priority changed from A to C\n|  1| (C) Foo\nPriority set to C.\n|  2| (C) Bar\n")
        self.assertEqual(self.errors, "")

    def test_set_prio8(self):
        """ Allow to unset a priority. """
        command = PriorityCommand(["-d", "1"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, "Priority removed.\n|  1| Foo\n")
        self.assertEqual(self.errors, "")

    def test_expr_prio1(self):
        command = PriorityCommand(["-e", "@test", "C"], self.todolist,
                                  self.out, self.error, None)
        command.execute()

        result = "Priority changed from B to C\n|  3| (C) a @test with due:2015-06-03\nPriority set to C.\n|  4| (C) a @test with +project p:1\n"

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, result)
        self.assertEqual(self.errors, "")

    def test_expr_prio2(self):
        command = PriorityCommand(["-e", "@test", "due:2015-06-03", "C"],
                                  self.todolist, self.out, self.error, None)
        command.execute()

        result = "Priority changed from B to C\n|  3| (C) a @test with due:2015-06-03\n"

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, result)
        self.assertEqual(self.errors, "")

    def test_expr_prio3(self):
        command = PriorityCommand(["-e", "@test", "due:2015-06-03", "+project",
                                   "C"], self.todolist, self.out, self.error,
                                  None)
        command.execute()

        self.assertFalse(self.todolist.dirty)

    def test_expr_prio4(self):
        """ Don't prioritize unrelevant todo items. """
        command = PriorityCommand(["-e", "Baz", "C"], self.todolist, self.out,
                                  self.error, None)
        command.execute()

        self.assertFalse(self.todolist.dirty)

    def test_expr_prio5(self):
        """ Force prioritizing unrelevant items with additional -x flag. """
        command = PriorityCommand(["-xe", "Baz", "D"], self.todolist, self.out,
                                  self.error, None)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output,
                         "Priority set to D.\n|  5| (D) Baz id:1\n")
        self.assertEqual(self.errors, "")

    def test_expr_prio6(self):
        """ Remove multiple priorities. """
        command = PriorityCommand(["-de", "@test"], self.todolist, self.out,
                                  self.error)
        command.execute()

        result = "Priority removed.\n|  3| a @test with due:2015-06-03\n|  4| a @test with +project p:1\n"

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, result)
        self.assertEqual(self.errors, "")

    def test_invalid1(self):
        command = PriorityCommand(["99", "A"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertFalse(self.output)
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_invalid2(self):
        command = PriorityCommand(["1", "99", "A"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertFalse(self.output)
        self.assertEqual(self.errors, "Invalid todo number given: 99.\n")

    def test_invalid3(self):
        command = PriorityCommand(["98", "99", "A"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertFalse(self.output)
        self.assertEqual(self.errors, "Invalid todo number given: 98.\nInvalid todo number given: 99.\n")

    def test_invalid4(self):
        command = PriorityCommand(["1", "ZZ"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertFalse(self.output)
        self.assertEqual(self.errors, "Invalid priority given.\n")

    def test_invalid5(self):
        command = PriorityCommand(["A"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertFalse(self.output)
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_invalid6(self):
        command = PriorityCommand(["1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertFalse(self.output)
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_invalid7(self):
        """
        Throw an error with invalid argument containing special characters.
        """
        command = PriorityCommand([u"Fo\u00d3B\u0105r", "Bar", "C"],
                                  self.todolist, self.out, self.error, None)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors,
                         u"Invalid todo number given: Fo\u00d3B\u0105r.\n")

    def test_invalid8(self):
        """
        Test that there's only one capital surrounded by non-word
        characters that makes up a priority.
        """
        command = PriorityCommand(["2", "(Aa)"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid priority given.\n")

    def test_invalid9(self):
        """
        Test that there's only one capital surrounded by non-word
        characters that makes up a priority.
        """
        command = PriorityCommand(["2", "Aa"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid priority given.\n")

    def test_empty(self):
        command = PriorityCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertFalse(self.output)
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_priority_name(self):
        name = PriorityCommand.name()

        self.assertEqual(name, 'priority')

    def test_help(self):
        command = PriorityCommand(["help"], self.todolist, self.out,
                                  self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors,
                         command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
