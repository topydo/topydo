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

from test.command_testcase import CommandTest
from topydo.commands.DepCommand import DepCommand
from topydo.lib.TodoList import TodoList


class DepCommandTest(CommandTest):
    def setUp(self):
        super(DepCommandTest, self).setUp()
        todos = [
            "Foo id:1",
            "Bar p:1",
            "Baz p:1",
            "Fnord id:2",
            "Garbage dependency p:99",
            "Fart p:2",
        ]

        self.todolist = TodoList(todos)

    def test_add1(self):
        command = DepCommand(["add", "1", "to", "4"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertTrue(self.todolist.todo(4).has_tag('p', '1'))
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_add2(self):
        command = DepCommand(["add", "1", "4"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertTrue(self.todolist.todo(4).has_tag('p', '1'))
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_add3(self):
        command = DepCommand(["add", "99", "3"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_add4(self):
        command = DepCommand(["add", "A", "3"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_add5(self):
        command = DepCommand(["add", "1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_add6(self):
        command = DepCommand(["add", "1", "after", "4"], self.todolist,
                             self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertTrue(self.todolist.todo(4).has_tag('p', '1'))
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_add7(self):
        command = DepCommand(["add", "1", "before", "4"], self.todolist,
                             self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertTrue(self.todolist.todo(1).has_tag('p', '2'))
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_add8(self):
        command = DepCommand(["add", "1", "partof", "4"], self.todolist,
                             self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertTrue(self.todolist.todo(1).has_tag('p', '2'))
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_add9(self):
        command = DepCommand(["add", "Foo", "to", "4"], self.todolist,
                             self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertTrue(self.todolist.todo(4).has_tag('p', '1'))
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def rm_helper(self, p_args):
        """
        Helper function that checks the removal of the dependency from todo 1
        to todo 3.
        """
        command = DepCommand(p_args, self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertTrue(self.todolist.todo(1).has_tag('id', '1'))
        self.assertFalse(self.todolist.todo(3).has_tag('p', '1'))
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_rm1(self):
        self.rm_helper(["rm", "1", "to", "3"])

    def test_rm2(self):
        self.rm_helper(["rm", "1", "3"])

    def test_del1(self):
        self.rm_helper(["del", "1", "to", "3"])

    def test_del2(self):
        self.rm_helper(["del", "1", "3"])

    def test_rm3(self):
        command = DepCommand(["rm", "99", "3"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_rm4(self):
        command = DepCommand(["rm", "A", "3"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_rm5(self):
        command = DepCommand(["rm", "1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_ls1(self):
        command = DepCommand(["ls", "1", "to"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  2| Bar p:1\n|  3| Baz p:1\n")
        self.assertEqual(self.errors, "")

    def test_ls2(self):
        command = DepCommand(["ls", "99", "to"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_ls3(self):
        command = DepCommand(["ls", "to", "3"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "|  1| Foo id:1\n")
        self.assertEqual(self.errors, "")

    def test_ls4(self):
        command = DepCommand(["ls", "to", "99"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_ls5(self):
        command = DepCommand(["ls", "1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_ls6(self):
        command = DepCommand(["ls"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_ls7(self):
        command = DepCommand(["ls", "top", "99"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def gc_helper(self, p_subcommand):
        command = DepCommand([p_subcommand], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())
        self.assertFalse(self.output)
        self.assertFalse(self.errors)
        self.assertFalse(self.todolist.todo(5).has_tag('p', '99'))

    def test_clean(self):
        self.gc_helper("clean")

    def test_gc(self):
        self.gc_helper("gc")

    def test_invalid_subsubcommand(self):
        command = DepCommand(["foo"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.output)
        self.assertEqual(self.errors, command.usage() + "\n")
        self.assertFalse(self.todolist.is_dirty())

    def test_no_subsubcommand(self):
        command = DepCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.output)
        self.assertEqual(self.errors, command.usage() + "\n")
        self.assertFalse(self.todolist.is_dirty())

    def test_help(self):
        command = DepCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors,
                         command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
