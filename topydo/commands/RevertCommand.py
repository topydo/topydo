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
from topydo.lib.ChangeSet import ChangeSet
from topydo.lib import TodoFile
from topydo.lib import TodoList
from topydo.lib.Config import config

class RevertCommand(Command):
    def __init__(self, p_args, p_todolist, #pragma: no branch
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super().__init__(p_args, p_todolist, p_out, p_err,
                p_prompt)

    def execute(self):
        if not super().execute():
            return False

        archive_file = TodoFile.TodoFile(config().archive())
        archive = TodoList.TodoList(archive_file.read())

        last_change = ChangeSet()

        try:
            last_change.get_backup(self.todolist)
            last_change.apply(self.todolist, archive)
            archive_file.write(archive.print_todos())
            last_change.delete()

            self.out("Successfully reverted: " + last_change.call)
        except (ValueError, KeyError):
            self.error('No backup was found for the current state of ' + config().todotxt())

        last_change.close()


    def usage(self):
        return """Synopsis: revert"""

    def help(self):
        return """Reverts the last command."""
