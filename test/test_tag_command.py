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

from freezegun import freeze_time

from topydo.commands.TagCommand import TagCommand
from topydo.lib.TodoList import TodoList

from .command_testcase import CommandTest


class TagCommandTest(CommandTest):
    def setUp(self):
        super().setUp()
        todos = [
            "Foo",
            "Bar due:2014-10-22",
            "Baz due:2014-10-20",
            "Fnord due:2014-10-20 due:2014-10-22",
        ]

        self.todolist = TodoList(todos)

    def test_add_tag1(self):
        command = TagCommand(["1", "due", "2014-10-22"], self.todolist,
                             self.out, self.error)
        command.execute()

        self.assertEqual(self.todolist.todo(1).source(), "Foo due:2014-10-22")
        self.assertEqual(self.output, "|  1| Foo due:2014-10-22\n")
        self.assertEqual(self.errors, "")
        self.assertTrue(self.todolist.dirty)

    def test_add_tag2(self):
        command = TagCommand(["Foo", "due", "2014-10-22"], self.todolist,
                             self.out, self.error)
        command.execute()

        self.assertEqual(self.todolist.todo(1).source(), "Foo due:2014-10-22")
        self.assertEqual(self.output, "|  1| Foo due:2014-10-22\n")
        self.assertEqual(self.errors, "")
        self.assertTrue(self.todolist.dirty)

    def test_add_tag3(self):
        command = TagCommand(["-a", "2", "due", "2014-10-19"], self.todolist,
                             self.out, self.error)
        command.execute()

        self.assertEqual(self.todolist.todo(2).source(),
                         "Bar due:2014-10-22 due:2014-10-19")
        self.assertEqual(self.output,
                         "|  2| Bar due:2014-10-22 due:2014-10-19\n")
        self.assertEqual(self.errors, "")
        self.assertTrue(self.todolist.dirty)

    def test_add_tag4(self):
        command = TagCommand(["Foox", "due", "2014-10-22"], self.todolist,
                             self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertFalse(self.output)
        self.assertEqual(self.errors, "Invalid todo number.\n")

    def test_force_add_tag01(self):
        '''Tries to different values to a tag for the same name 3 times.'''
        for letter in ['a', 'b', 'c']:
            command = TagCommand(['-a', '1', 'k', letter], self.todolist,
                                 self.out, self.error)
            command.execute()

            self.assertEqual(self.errors, "")
            self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.todolist.todo(1).source(), "Foo k:a k:b k:c")

    def test_set_tag04(self):
        command = TagCommand(["3", "due", "2014-10-20"], self.todolist,
                             self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|  3| Baz due:2014-10-20\n")
        self.assertEqual(self.errors, "")

    def test_set_tag05(self):
        command = TagCommand(["4", "due", "2014-10-20"], self.todolist,
                             self.out, self.error, lambda t: "all")
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, " 1. 2014-10-20\n 2. 2014-10-22\n|  4| Fnord due:2014-10-20 due:2014-10-20\n")
        self.assertEqual(self.errors, "")

    def test_set_tag06(self):
        command = TagCommand(["4", "due", "2014-10-20"], self.todolist,
                             self.out, self.error, lambda t: "1")
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, " 1. 2014-10-20\n 2. 2014-10-22\n|  4| Fnord due:2014-10-20 due:2014-10-22\n")
        self.assertEqual(self.errors, "")

    def test_set_tag07(self):
        command = TagCommand(["4", "due", "2014-10-20"], self.todolist,
                             self.out, self.error, lambda t: "2")
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, " 1. 2014-10-20\n 2. 2014-10-22\n|  4| Fnord due:2014-10-20 due:2014-10-20\n")
        self.assertEqual(self.errors, "")

    def test_set_tag08(self):
        command = TagCommand(["4", "due", "2014-10-20"], self.todolist,
                             self.out, self.error, lambda t: "")
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, " 1. 2014-10-20\n 2. 2014-10-22\n|  4| Fnord due:2014-10-20 due:2014-10-22\n")
        self.assertEqual(self.errors, "")

    def test_set_tag09(self):
        command = TagCommand(["4", "due", "2014-10-20"], self.todolist,
                             self.out, self.error, lambda t: "99")
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, " 1. 2014-10-20\n 2. 2014-10-22\n|  4| Fnord due:2014-10-20 due:2014-10-22\n")
        self.assertEqual(self.errors, "")

    def test_set_tag10(self):
        command = TagCommand(["-f", "4", "due", "2014-10-20"], self.todolist,
                             self.out, self.error, lambda t: "99")
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output,
                         "|  4| Fnord due:2014-10-20 due:2014-10-20\n")
        self.assertEqual(self.errors, "")

    @freeze_time('2015, 11, 19')
    def test_set_tag11(self):
        command = TagCommand(["3", "due", "today"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, "|  3| Baz due:2015-11-19\n")
        self.assertEqual(self.errors, "")

    def test_set_tag12(self):
        """
        Do not convert relative dates for tags that were not configured as
        start/due date.
        """
        command = TagCommand(["3", "foo", "today"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, "|  3| Baz due:2014-10-20 foo:today\n")
        self.assertEqual(self.errors, "")

    @freeze_time('2017, 1, 12')
    def test_set_tag13(self):
        """
        Convert relative dates when forced to.
        """

        command = TagCommand(["-r", "3", "foo", "today"], self.todolist,
                             self.out, self.error)

        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, "|  3| Baz due:2014-10-20 foo:2017-01-12\n")
        self.assertEqual(self.errors, "")

    def test_set_tag14(self):
        """
        Leave the original value when an invalid relative date was given.
        """

        command = TagCommand(["-r", "3", "foo", "bar"], self.todolist,
                             self.out, self.error)

        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, "|  3| Baz due:2014-10-20 foo:bar\n")
        self.assertEqual(self.errors, "")

    def test_rm_tag01(self):
        command = TagCommand(["1", "due"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|  1| Foo\n")
        self.assertEqual(self.errors, "")

    def test_rm_tag02(self):
        command = TagCommand(["2", "due"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, "|  2| Bar\n")
        self.assertEqual(self.errors, "")

    def test_rm_tag03(self):
        command = TagCommand(["4", "due"], self.todolist, self.out,
                             self.error, lambda t: "all")
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output,
                         " 1. 2014-10-20\n 2. 2014-10-22\n|  4| Fnord\n")
        self.assertEqual(self.errors, "")

    def test_rm_tag04(self):
        command = TagCommand(["4", "due"], self.todolist, self.out, self.error,
                             lambda t: "1")
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, " 1. 2014-10-20\n 2. 2014-10-22\n|  4| Fnord due:2014-10-22\n")
        self.assertEqual(self.errors, "")

    def test_rm_tag06(self):
        command = TagCommand(["4", "due"], self.todolist, self.out, self.error,
                             lambda t: "99")
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, " 1. 2014-10-20\n 2. 2014-10-22\n|  4| Fnord due:2014-10-20 due:2014-10-22\n")
        self.assertEqual(self.errors, "")

    def test_rm_tag07(self):
        command = TagCommand(["4", "due"], self.todolist, self.out, self.error,
                             lambda t: "A")
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, " 1. 2014-10-20\n 2. 2014-10-22\n|  4| Fnord due:2014-10-20 due:2014-10-22\n")
        self.assertEqual(self.errors, "")

    def test_rm_tag08(self):
        command = TagCommand(["5", "due"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number.\n")

    def test_rm_tag09(self):
        command = TagCommand(["A", "due"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number.\n")

    def test_rm_tag10(self):
        command = TagCommand(["-f", "4", "due"], self.todolist, self.out,
                             self.error, lambda t: "A")
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertEqual(self.output, "|  4| Fnord\n")
        self.assertEqual(self.errors, "")

    def test_no_tag(self):
        command = TagCommand(["4"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_tag_name(self):
        name = TagCommand.name()

        self.assertEqual(name, 'tag')

    def test_help(self):
        command = TagCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors,
                         command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
