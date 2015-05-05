# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 Bram Schoenmakers <me@bramschoenmakers.nl>
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

import CommandTest
from topydo.lib.TagCommand import TagCommand
from topydo.lib.TodoList import TodoList

class TagCommandTest(CommandTest.CommandTest):
    def setUp(self):
        super(TagCommandTest, self).setUp()
        todos = [
            "Foo",
            "Bar due:2014-10-22",
            "Baz due:2014-10-20",
            "Fnord due:2014-10-20 due:2014-10-22",
        ]

        self.todolist = TodoList(todos)

    def test_add_tag1(self):
        command = TagCommand(["1", "due", "2014-10-22"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.todolist.todo(1).source(), "Foo due:2014-10-22")
        self.assertEquals(self.output, "|  1| Foo due:2014-10-22\n")
        self.assertEquals(self.errors, "")
        self.assertTrue(self.todolist.is_dirty())

    def test_add_tag2(self):
        command = TagCommand(["Foo", "due", "2014-10-22"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.todolist.todo(1).source(), "Foo due:2014-10-22")
        self.assertEquals(self.output, "|  1| Foo due:2014-10-22\n")
        self.assertEquals(self.errors, "")
        self.assertTrue(self.todolist.is_dirty())

    def test_add_tag3(self):
        command = TagCommand(["-a", "2", "due", "2014-10-19"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.todolist.todo(2).source(), "Bar due:2014-10-22 due:2014-10-19")
        self.assertEquals(self.output, "|  2| Bar due:2014-10-22 due:2014-10-19\n")
        self.assertEquals(self.errors, "")
        self.assertTrue(self.todolist.is_dirty())

    def test_add_tag4(self):
        command = TagCommand(["Foox", "due", "2014-10-22"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEquals(self.errors, "Invalid todo number.\n")

    def test_set_tag4(self):
        command = TagCommand(["3", "due", "2014-10-20"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  3| Baz due:2014-10-20\n")
        self.assertEquals(self.errors, "")

    def test_set_tag5(self):
        command = TagCommand(["4", "due", "2014-10-20"], self.todolist, self.out, self.error, lambda t: "all")
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, " 1. 2014-10-20\n 2. 2014-10-22\n|  4| Fnord due:2014-10-20 due:2014-10-20\n")
        self.assertEquals(self.errors, "")

    def test_set_tag6(self):
        command = TagCommand(["4", "due", "2014-10-20"], self.todolist, self.out, self.error, lambda t: "1")
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, " 1. 2014-10-20\n 2. 2014-10-22\n|  4| Fnord due:2014-10-20 due:2014-10-22\n")
        self.assertEquals(self.errors, "")

    def test_set_tag7(self):
        command = TagCommand(["4", "due", "2014-10-20"], self.todolist, self.out, self.error, lambda t: "2")
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, " 1. 2014-10-20\n 2. 2014-10-22\n|  4| Fnord due:2014-10-20 due:2014-10-20\n")
        self.assertEquals(self.errors, "")

    def test_set_tag8(self):
        command = TagCommand(["4", "due", "2014-10-20"], self.todolist, self.out, self.error, lambda t: "")
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, " 1. 2014-10-20\n 2. 2014-10-22\n|  4| Fnord due:2014-10-20 due:2014-10-22\n")
        self.assertEquals(self.errors, "")

    def test_set_tag9(self):
        command = TagCommand(["4", "due", "2014-10-20"], self.todolist, self.out, self.error, lambda t: "99")
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, " 1. 2014-10-20\n 2. 2014-10-22\n|  4| Fnord due:2014-10-20 due:2014-10-22\n")
        self.assertEquals(self.errors, "")

    def test_set_tag10(self):
        command = TagCommand(["-f", "4", "due", "2014-10-20"], self.todolist, self.out, self.error, lambda t: "99")
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  4| Fnord due:2014-10-20 due:2014-10-20\n")
        self.assertEquals(self.errors, "")

    def test_rm_tag1(self):
        command = TagCommand(["1", "due"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  1| Foo\n")
        self.assertEquals(self.errors, "")

    def test_rm_tag2(self):
        command = TagCommand(["2", "due"], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  2| Bar\n")
        self.assertEquals(self.errors, "")

    def test_rm_tag3(self):
        command = TagCommand(["4", "due"], self.todolist, self.out, self.error, lambda t: "all")
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, " 1. 2014-10-20\n 2. 2014-10-22\n|  4| Fnord\n")
        self.assertEquals(self.errors, "")

    def test_rm_tag4(self):
        command = TagCommand(["4", "due"], self.todolist, self.out, self.error, lambda t: "1")
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, " 1. 2014-10-20\n 2. 2014-10-22\n|  4| Fnord due:2014-10-22\n")
        self.assertEquals(self.errors, "")

    def test_rm_tag6(self):
        command = TagCommand(["4", "due"], self.todolist, self.out, self.error, lambda t: "99")
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, " 1. 2014-10-20\n 2. 2014-10-22\n|  4| Fnord due:2014-10-20 due:2014-10-22\n")
        self.assertEquals(self.errors, "")

    def test_rm_tag7(self):
        command = TagCommand(["4", "due"], self.todolist, self.out, self.error, lambda t: "A")
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, " 1. 2014-10-20\n 2. 2014-10-22\n|  4| Fnord due:2014-10-20 due:2014-10-22\n")
        self.assertEquals(self.errors, "")

    def test_rm_tag8(self):
        command = TagCommand(["5", "due"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "Invalid todo number.\n")

    def test_rm_tag9(self):
        command = TagCommand(["A", "due"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, "Invalid todo number.\n")

    def test_rm_tag10(self):
        command = TagCommand(["-f", "4", "due"], self.todolist, self.out, self.error, lambda t: "A")
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertEquals(self.output, "|  4| Fnord\n")
        self.assertEquals(self.errors, "")

    def test_no_tag(self):
        command = TagCommand(["4"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n")

    def test_help(self):
        command = TagCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output, "")
        self.assertEquals(self.errors, command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
