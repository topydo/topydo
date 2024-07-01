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

from topydo.commands.ArchiveCommand import ArchiveCommand
from topydo.lib.TodoList import TodoList

from .command_testcase import CommandTest
from .facilities import load_file_to_todolist


class ArchiveCommandTest(CommandTest):
    def test_archive(self):
        todolist = load_file_to_todolist("test/data/ArchiveCommandTest.txt")
        archive = TodoList([])

        command = ArchiveCommand(todolist, archive)
        command.execute()

        self.assertTrue(todolist.dirty)
        self.assertTrue(archive.dirty)
        self.assertEqual(todolist.print_todos(), "(C) Active")
        self.assertEqual(archive.print_todos(), "x 2014-10-19 Complete\nx 2014-10-20 Another one complete")

if __name__ == '__main__':
    unittest.main()
