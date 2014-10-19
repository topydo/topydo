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

import CommandTest
import TestFacilities
import ListContextCommand

class ListContextCommandTest(CommandTest.CommandTest):
    def test_contexts1(self):
        todolist = TestFacilities.load_file_to_todolist("data/TodoListTest.txt")
        command = ListContextCommand.ListContextCommand([""], todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output,"Context1\nContext2\n")
        self.assertFalse(self.errors)

    def test_contexts2(self):
        todolist = TestFacilities.load_file_to_todolist("data/TodoListTest.txt")
        command = ListContextCommand.ListContextCommand(["aaa"], todolist, self.out, self.error)
        command.execute()

        self.assertEquals(self.output,"Context1\nContext2\n")
        self.assertFalse(self.errors)
