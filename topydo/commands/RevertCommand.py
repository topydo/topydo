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

import arrow

from topydo.lib.Command import Command, InvalidCommandArgument
from topydo.lib.ChangeSet import ChangeSet
from topydo.lib import TodoFile
from topydo.lib import TodoList
from topydo.lib.Config import config


class RevertCommand(Command):
    def __init__(self, p_args, p_todolist,  # pragma: no branch
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super().__init__(p_args, p_todolist, p_out, p_err, p_prompt)

        self._backup = None
        self._archive_file = None
        self._archive = None

    def execute(self):
        if not super().execute():
            return False

        self._backup = ChangeSet()
        archive_path = config().archive()
        if archive_path:
            self._archive_file = TodoFile.TodoFile(config().archive())
            self._archive = TodoList.TodoList(self._archive_file.read())

        if len(self.args) > 0:
            self._handle_args()
        else:
            try:
                self._revert_last()
            except (ValueError, KeyError):
                self.error('No backup was found for the current state of '
                           + config().todotxt())

        self._backup.close()

    def _revert(self, p_timestamp=None):
        if p_timestamp is None:
            self._backup.get_backup_from_todolist(self.todolist)
        else:
            self._backup.get_backup_from_timestamp(p_timestamp)

        self._backup.apply(self.todolist, self._archive)
        if self._archive:
            self._archive_file.write(self._archive.print_todos())
        self.out("Reverted to state before: " + self._backup.label)

    def _revert_last(self):
        self._revert()
        self._backup.delete()

    def _revert_to_specific(self, p_position):
        timestamps = [timestamp for timestamp, _ in self._backup]
        position = int(p_position)
        try:
            timestamp = timestamps[position]
            self._revert(timestamp)
            for timestamp in timestamps[:position + 1]:
                self._backup.get_backup_from_timestamp(timestamp)
                self._backup.delete()
        except IndexError:
            self.error('Specified index is out range')

    def _handle_args(self):
        arg = self.argument(0)
        try:
            if arg == 'ls':
                self._handle_ls()
            elif arg.isdigit():
                self._revert_to_specific(arg)
            else:
                raise InvalidCommandArgument
        except InvalidCommandArgument:
            self.error(self.usage())

    def _handle_ls(self):
        num = 0
        changes = []
        for timestamp, change in self._backup:
            label = change[2]
            time = arrow.get(timestamp).format('YYYY-MM-DD HH:mm:ss')

            changes.append(str(num) + ' | ' + time + ' | ' + label + '\n')
            num += 1

        self.out(''.join(changes).rstrip())

    def usage(self):
        return """Synopsis: revert"""

    def help(self):
        return """Reverts the last command."""
