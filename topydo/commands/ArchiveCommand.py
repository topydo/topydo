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

from topydo.lib.Command import Command


class ArchiveCommand(Command):
    def __init__(self, p_todolist, p_archive_list):
        """
        Constructor.

        p_todolist where all completed items will be moved from.
        p_archive_list is the list where the items go to. This can be a
        TodoListBase class which does no dependency checking, so a better
        choice for huge done.txt files.
        """
        super().__init__([], p_todolist)
        self.archive = p_archive_list

    def execute(self):
        for todo in [t for t in self.todolist.todos() if t.is_completed()]:
            self.archive.add_todo(todo)
            self.todolist.delete(todo)
