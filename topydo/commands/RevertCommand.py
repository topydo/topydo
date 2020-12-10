# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2017 Bram Schoenmakers <bram@topydo.org>
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

from topydo.lib import TodoFile, TodoList
from topydo.lib.ChangeSet import ChangeSet
from topydo.lib.Command import Command, InvalidCommandArgument
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

        if len(self.args) > 1:
            self.error(self.usage())
        else:
            try:
                arg = self.argument(0)
                self._handle_args(arg)
            except InvalidCommandArgument:
                try:
                    self._revert_last()
                except (ValueError, KeyError):
                    self.error('No backup was found for the current state of '
                               + config().todotxt())

        self._backup.close()

    def _revert(self, p_timestamp=None):
        self._backup.read_backup(self.todolist, p_timestamp)
        self._backup.apply(self.todolist, self._archive)

        if self._archive:
            self._archive_file.write(self._archive.print_todos())

        self.out("Reverted to state before: " + self._backup.label)

    def _revert_last(self):
        self._revert()
        self._backup.delete()

    def _revert_to_specific(self, p_position):
        timestamps = [timestamp for timestamp, _ in self._backup]
        position = int(p_position) - 1  # numbering in UI starts with 1
        try:
            timestamp = timestamps[position]
            self._revert(timestamp)
            for timestamp in timestamps[:position + 1]:
                self._backup.read_backup(p_timestamp=timestamp)
                self._backup.delete()
        except IndexError:
            self.error('Specified index is out range')

    def _handle_args(self, p_arg):
        try:
            if p_arg == 'ls':
                self._handle_ls()
            elif p_arg.isdigit():
                self._revert_to_specific(p_arg)
            else:
                raise InvalidCommandArgument
        except InvalidCommandArgument:
            self.error(self.usage())

    def _handle_ls(self):
        num = 1
        for timestamp, change in self._backup:
            label = change[2]
            time = arrow.get(float(timestamp)).format('YYYY-MM-DD HH:mm:ss')

            self.out('{0: >3}| {1} | {2}'.format(str(num), time, label))
            num += 1

    def usage(self):
        return """Synopsis:
  revert [ls]
  revert [NUMBER]"""

    def help(self):
        return """\
Reverts last commands.

* ls       : Lists all backups ordered and numbered chronologically (starting
             with 1 for the latest backup).
* [NUMBER] : revert to specific point in history specified by NUMBER.

Output example for `revert ls`:
1 | 1970-01-01 00:00:02 | add Baz
2 | 1970-01-01 00:00:01 | add Bar
3 | 1970-01-01 00:00:00 | add Foo

In such example executing `revert 2` will revert the todo and archive files to
the state before execution of `add Bar`.

* `revert` without any further arguments will revert to the latest backup
  available, provided that this backup matches the current state of the todo
  file.
  Topydo will refuse to revert, if any changes to todo file were made by
  external application after the latest backup. To force a `revert` action use
  it with a NUMBER.\
"""
