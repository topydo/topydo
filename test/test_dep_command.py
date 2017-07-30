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

from topydo.commands.DepCommand import DepCommand
from topydo.lib.TodoList import TodoList

from .command_testcase import CommandTest


class DepCommandTest(CommandTest):
    def setUp(self):
        super().setUp()
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

        self.assertTrue(self.todolist.dirty)
        self.assertTrue(self.todolist.todo(4).has_tag('p', '1'))
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_add2(self):
        command = DepCommand(["add", "1", "4"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertTrue(self.todolist.todo(4).has_tag('p', '1'))
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_add3(self):
        command = DepCommand(["add", "99", "3"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_add4(self):
        command = DepCommand(["add", "A", "3"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_add5(self):
        command = DepCommand(["add", "1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_add6(self):
        command = DepCommand(["add", "1", "after", "4"], self.todolist,
                             self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertTrue(self.todolist.todo(4).has_tag('p', '1'))
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_add7(self):
        command = DepCommand(["add", "1", "before", "4"], self.todolist,
                             self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertTrue(self.todolist.todo(1).has_tag('p', '2'))
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_add8(self):
        command = DepCommand(["add", "1", "partof", "4"], self.todolist,
                             self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertTrue(self.todolist.todo(1).has_tag('p', '2'))
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_add9(self):
        command = DepCommand(["add", "Foo", "to", "4"], self.todolist,
                             self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertTrue(self.todolist.todo(4).has_tag('p', '1'))
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def add_parentsof_helper(self, p_args):
        command = DepCommand(p_args, self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertTrue(self.todolist.todo(4).has_tag('p', '1'))
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_add10(self):
        self.add_parentsof_helper(["add", "4", "parents-of", "2"])

    def test_add11(self):
        self.add_parentsof_helper(["add", "4", "parent-of", "2"])

    def test_add12(self):
        self.add_parentsof_helper(["add", "4", "parentsof", "2"])

    def test_add13(self):
        self.add_parentsof_helper(["add", "4", "parentof", "2"])

    def test_add14(self):
        command = DepCommand(["add", "4", "parents-of", "5"], self.todolist,
                             self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def add_childrenof_helper(self, p_args):
        command = DepCommand(p_args, self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
        self.assertTrue(self.todolist.todo(2).has_tag('p', '2'))
        self.assertTrue(self.todolist.todo(3).has_tag('p', '2'))
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def test_add15(self):
        self.add_childrenof_helper(["add", "4", "children-of", "1"])

    def test_add16(self):
        self.add_childrenof_helper(["add", "4", "child-of", "1"])

    def test_add17(self):
        self.add_childrenof_helper(["add", "4", "childrenof", "1"])

    def test_add18(self):
        self.add_childrenof_helper(["add", "4", "childof", "1"])

    def test_add19(self):
        command = DepCommand(["add", "4", "children-of", "5"], self.todolist,
                             self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "")

    def rm_helper(self, p_args):
        """
        Helper function that checks the removal of the dependency from todo 1
        to todo 3.
        """
        command = DepCommand(p_args, self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
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

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_rm4(self):
        command = DepCommand(["rm", "A", "3"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_rm5(self):
        command = DepCommand(["rm", "1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_ls1(self):
        command = DepCommand(["ls", "1", "to"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|  2| Bar p:1\n|  3| Baz p:1\n")
        self.assertEqual(self.errors, "")

    def test_ls2(self):
        command = DepCommand(["ls", "99", "to"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_ls3(self):
        command = DepCommand(["ls", "to", "3"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|  1| Foo id:1\n")
        self.assertEqual(self.errors, "")

    def test_ls4(self):
        command = DepCommand(["ls", "to", "99"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_ls5(self):
        command = DepCommand(["ls", "before", "1"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|  2| Bar p:1\n|  3| Baz p:1\n")
        self.assertEqual(self.errors, "")

    def test_ls6(self):
        command = DepCommand(["ls", "before", "99"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_ls7(self):
        command = DepCommand(["ls", "after", "3"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "|  1| Foo id:1\n")
        self.assertEqual(self.errors, "")

    def test_ls8(self):
        command = DepCommand(["ls", "after", "99"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given.\n")

    def test_ls9(self):
        command = DepCommand(["ls", "1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_ls10(self):
        command = DepCommand(["ls"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertFalse(self.output)
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_ls11(self):
        command = DepCommand(["ls", "top", "99"], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_dot1(self):
        command = DepCommand(["dot"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n")

    def test_dot2(self):
        self.maxDiff = None
        command = DepCommand(["dot", "1"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, """digraph topydo {
node [ shape="none" margin="0" fontsize="9" fontname="Helvetica" ]
  _2 [label=<<TABLE CELLBORDER="0" CELLSPACING="1" VALIGN="top"><TR><TD><B>2</B></TD><TD BALIGN="LEFT"><B>Bar</B></TD></TR></TABLE>> style=filled fillcolor="#008000" fontcolor="#ffffff"]
  _3 [label=<<TABLE CELLBORDER="0" CELLSPACING="1" VALIGN="top"><TR><TD><B>3</B></TD><TD BALIGN="LEFT"><B>Baz</B></TD></TR></TABLE>> style=filled fillcolor="#008000" fontcolor="#ffffff"]
  _1 [label=<<TABLE CELLBORDER="0" CELLSPACING="1" VALIGN="top"><TR><TD><B>1</B></TD><TD BALIGN="LEFT"><B>Foo</B></TD></TR></TABLE>> style=filled fillcolor="#008000" fontcolor="#ffffff"]
  _1 -> _2
  _1 -> _3
}\n
""")
        self.assertEqual(self.errors, "")

    def test_dot3(self):
        command = DepCommand(["dot", "99"], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.dirty)
        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, "Invalid todo number given." + "\n")

    def gc_helper(self, p_subcommand):
        command = DepCommand([p_subcommand], self.todolist, self.out,
                             self.error)
        command.execute()

        self.assertTrue(self.todolist.dirty)
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
        self.assertFalse(self.todolist.dirty)

    def test_no_subsubcommand(self):
        command = DepCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.output)
        self.assertEqual(self.errors, command.usage() + "\n")
        self.assertFalse(self.todolist.dirty)

    def test_dep_name(self):
        name = DepCommand.name()

        self.assertEqual(name, 'dep')

    def test_help(self):
        command = DepCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors,
                         command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
