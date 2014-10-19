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

import ArchiveCommand
import CommandTest
import TestFacilities
import TodoList

class ArchiveCommandTest(CommandTest.CommandTest):
    def test_archive(self):
        todolist = TestFacilities.load_file_to_todolist("data/ArchiveCommandTest.txt")
        archive = TodoList.TodoList([])

        command = ArchiveCommand.ArchiveCommand(todolist, archive)
        command.execute()

        self.assertTrue(todolist.is_dirty())
        self.assertTrue(archive.is_dirty())
        self.assertEquals(str(todolist), "x Not complete\n(C) Active")
        self.assertEquals(str(archive), "x 2014-10-19 Complete\nx 2014-10-20 Another one complete")

