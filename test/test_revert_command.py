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

import os
import tempfile
import unittest
from datetime import date
from glob import glob
from uuid import uuid4

from freezegun import freeze_time

from topydo.commands.AddCommand import AddCommand
from topydo.commands.ArchiveCommand import ArchiveCommand
from topydo.commands.DeleteCommand import DeleteCommand
from topydo.commands.DoCommand import DoCommand
from topydo.commands.RevertCommand import RevertCommand
from topydo.lib.ChangeSet import ChangeSet
from topydo.lib.Config import config
from topydo.lib.TodoFile import TodoFile
from topydo.lib.TodoList import TodoList

from .command_testcase import CommandTest

# We're searching for 'mock'
# 'mock' was added as 'unittest.mock' in Python 3.3, but PyPy 3 is based on Python 3.2
# pylint: disable=no-name-in-module
try:
    from unittest import mock
except ImportError:
    import mock


class BackupSimulator(object):
    def __init__(self, p_todolist, p_archive, p_timestamp, p_label):
        self.backup = ChangeSet(p_todolist, p_archive, p_label)
        self.backup.timestamp = p_timestamp

    def save(self, p_todolist):
        self.backup.save(p_todolist)


def command_executer(p_cmd, p_args, p_todolist, p_archive=None, *params):
    command = p_cmd(p_args, p_todolist, *params)
    command.execute()
    if p_archive:
        archive_command = ArchiveCommand(p_todolist, p_archive)
        archive_command.execute()


@freeze_time('2015, 11, 06')
class RevertCommandTest(CommandTest):
    def setUp(self):
        super().setUp()
        todos = [
            "Foo",
            "Bar",
            "Baz",
        ]

        self.todolist = TodoList(todos)
        self.today = date.today()

        self.tmp_name = str(uuid4().hex.upper()[0:6])

        archive_filename = tempfile.gettempdir() + os.sep + self.tmp_name + '_archive'
        todo_filename = tempfile.gettempdir() + os.sep + self.tmp_name + '_todo'

        config(p_overrides={('topydo', 'archive_filename'): archive_filename,
            ('topydo', 'filename'): todo_filename, ('topydo', 'backup_count'): '5'})

        self.archive_file = TodoFile(archive_filename)
        self.archive = TodoList([])

    def test_revert01(self):
        backup = BackupSimulator(self.todolist, self.archive, '1', ['do 1'])
        command_executer(DoCommand, ["1"], self.todolist, self.archive, self.out, self.error, None)
        self.archive_file.write(self.archive.print_todos())
        backup.save(self.todolist)

        self.assertEqual(self.archive.print_todos(), "x {} Foo".format(self.today))
        self.assertEqual(self.todolist.print_todos(), "Bar\nBaz")

        revert_command = RevertCommand([], self.todolist, self.out, self.error, None)
        revert_command.execute()

        result = TodoList(self.archive_file.read()).print_todos()

        self.assertEqual(self.errors, "")
        self.assertTrue(self.output.endswith("Reverted to state before: do 1\n"))
        self.assertEqual(result, "")
        self.assertEqual(self.todolist.print_todos(), "Foo\nBar\nBaz")

    def test_revert02(self):
        backup = BackupSimulator(self.todolist, self.archive, '1', ['do 1'])
        command_executer(DoCommand, ["1"], self.todolist, self.archive, self.out, self.error, None)
        self.archive_file.write(self.archive.print_todos())
        backup.save(self.todolist)

        # Use add_todolist and add_archive to also cover them
        backup = ChangeSet(p_label=['do Bar'])
        backup.add_todolist(self.todolist)
        backup.add_archive(self.archive)
        backup.timestamp = '2'
        command_executer(DoCommand, ["Bar"], self.todolist, self.archive, self.out, self.error, None)
        self.archive_file.write(self.archive.print_todos())
        backup.save(self.todolist)

        self.assertEqual(self.archive.print_todos(), "x {t} Foo\nx {t} Bar".format(t=self.today))
        self.assertEqual(self.todolist.print_todos(), "Baz")

        revert_command = RevertCommand([], self.todolist, self.out, self.error, None)
        revert_command.execute()

        result = TodoList(self.archive_file.read()).print_todos()

        self.assertEqual(self.errors, "")
        self.assertTrue(self.output.endswith("Reverted to state before: do Bar\n"))
        self.assertEqual(result, "x {} Foo".format(self.today))
        self.assertEqual(self.todolist.print_todos(), "Bar\nBaz")

    def test_revert03(self):
        """ Test behavior when no backup is found """
        command = RevertCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.errors, "No backup was found for the current state of {}\n".format(config().todotxt()))

    @mock.patch('topydo.lib.Config._Config.archive')
    def test_revert04(self, mock_archive):
        """ Test trimming of the backup_file """
        mock_archive.return_value = ''  # test for empty archive setting
        backup = BackupSimulator(self.todolist, self.archive, '1', ['add One'])
        command_executer(AddCommand, ["One"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '2', ['add Two'])
        command_executer(AddCommand, ["Two"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '3', ['add Three'])
        command_executer(AddCommand, ["Three"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '4', ['add Four'])
        command_executer(AddCommand, ["Four"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '5', ['add Five'])
        command_executer(AddCommand, ["Five"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        result = len(ChangeSet().backup_dict.keys())
        self.assertEqual(result, 6)

        backup = BackupSimulator(self.todolist, self.archive, '6', ['add Six'])
        command_executer(AddCommand, ["Six"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '7', ['add Seven'])
        command_executer(AddCommand, ["Seven"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        result = len(ChangeSet().backup_dict.keys())
        self.assertEqual(result, 6)

        revert_command = RevertCommand([], self.todolist, self.out, self.error, None)
        revert_command.execute()

        backup = ChangeSet()
        changesets = list(backup.backup_dict.keys())
        changesets.remove('index')
        index_timestamps = [change[0] for change in backup._get_index()]
        result = list(set(index_timestamps) - set(changesets))

        self.assertEqual(len(changesets), 4)
        self.assertEqual(result, [])
        self.assertEqual(self.errors, "")
        self.assertTrue(self.output.endswith("Reverted to state before: add Seven\n"))

    def test_revert05(self):
        """ Test for possible backup collisions """
        backup = BackupSimulator(self.todolist, self.archive, '1', ['add One'])
        command_executer(AddCommand, ["One"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '2', ['add Two'])
        command_executer(AddCommand, ["Two"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '3', ['add Three'])
        command_executer(AddCommand, ["Three"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '4', ['delete Three'])
        command_executer(DeleteCommand, ["Three"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '5', ['add Four'])
        command_executer(AddCommand, ["Four"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        revert_command = RevertCommand([], self.todolist, self.out, self.error, None)
        revert_command.execute()
        self.assertEqual(self.errors, "")
        self.assertTrue(self.output.endswith("Reverted to state before: add Four\n"))
        self.assertEqual(self.todolist.print_todos(), "Foo\nBar\nBaz\n{t} One\n{t} Two".format(t=self.today))

        revert_command = RevertCommand([], self.todolist, self.out, self.error, None)
        revert_command.execute()
        self.assertEqual(self.errors, "")
        self.assertTrue(self.output.endswith("Reverted to state before: delete Three\n"))
        self.assertEqual(self.todolist.print_todos(), "Foo\nBar\nBaz\n{t} One\n{t} Two\n{t} Three".format(t=self.today))

        revert_command = RevertCommand([], self.todolist, self.out, self.error, None)
        revert_command.execute()
        self.assertEqual(self.errors, "")
        self.assertTrue(self.output.endswith("Reverted to state before: add Three\n"))
        self.assertEqual(self.todolist.print_todos(), "Foo\nBar\nBaz\n{t} One\n{t} Two".format(t=self.today))

        revert_command = RevertCommand([], self.todolist, self.out, self.error, None)
        revert_command.execute()
        self.assertEqual(self.errors, "")
        self.assertTrue(self.output.endswith("Reverted to state before: add Two\n"))
        self.assertEqual(self.todolist.print_todos(), "Foo\nBar\nBaz\n{t} One".format(t=self.today))

        revert_command = RevertCommand([], self.todolist, self.out, self.error, None)
        revert_command.execute()
        self.assertEqual(self.errors, "")
        self.assertTrue(self.output.endswith("Reverted to state before: add One\n"))
        self.assertEqual(self.todolist.print_todos(), "Foo\nBar\nBaz")

    def test_revert06(self):
        """ Test attempt of deletion with non-existing backup key"""
        backup = BackupSimulator(self.todolist, self.archive, '1', ['add One'])
        command_executer(AddCommand, ["One"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '2', ['add Two'])
        command_executer(AddCommand, ["Two"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '3', ['add Three'])
        command_executer(AddCommand, ["Three"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '4', ['delete Three'])
        command_executer(DeleteCommand, ["Three"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = ChangeSet()
        backup.delete('Foo')

        changesets = list(backup.backup_dict.keys())
        changesets.remove('index')
        index_timestamps = [change[0] for change in backup._get_index()]
        result = list(set(index_timestamps) - set(changesets))

        self.assertEqual(len(changesets), 4)
        self.assertEqual(result, [])
        self.assertEqual(self.errors, "")

    def test_revert07(self):
        """ Test backup when no archive file is set """
        backup = ChangeSet(self.todolist, None, ['add One'])
        backup.timestamp = '1'
        command_executer(AddCommand, ["One"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        changesets = list(backup.backup_dict.keys())
        changesets.remove('index')

        self.assertEqual(len(changesets), 1)
        self.assertEqual(self.errors, "")

    def test_revert_ls(self):
        backup = BackupSimulator(self.todolist, self.archive, '1', ['add One'])
        command_executer(AddCommand, ["One"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '2', ['add Two'])
        command_executer(AddCommand, ["Two"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '3', ['add Three'])
        command_executer(AddCommand, ["Three"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '4', ['delete Three'])
        command_executer(DeleteCommand, ["Three"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '5', ['add Four'])
        command_executer(AddCommand, ["Four"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        command_executer(RevertCommand, ['ls'], self.todolist, None, self.out, self.error, None)

        self.assertEqual(self.errors, "")
        self.assertTrue(self.output.endswith("""  1| 1970-01-01 00:00:05 | add Four
  2| 1970-01-01 00:00:04 | delete Three
  3| 1970-01-01 00:00:03 | add Three
  4| 1970-01-01 00:00:02 | add Two
  5| 1970-01-01 00:00:01 | add One\n"""))

    def test_revert_08(self):
        backup = BackupSimulator(self.todolist, self.archive, '1', ['add One'])
        command_executer(AddCommand, ["One"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '2', ['add Two'])
        command_executer(AddCommand, ["Two"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '3', ['add Three'])
        command_executer(AddCommand, ["Three"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '4', ['delete Three'])
        command_executer(DeleteCommand, ["Three"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '5', ['add Four'])
        command_executer(AddCommand, ["Four"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        command_executer(RevertCommand, ['3'], self.todolist, None, self.out, self.error, None)

        self.assertEqual(self.errors, "")
        self.assertTrue(self.output.endswith("Reverted to state before: add Three\n"))
        self.assertEqual(self.todolist.print_todos(), "Foo\nBar\nBaz\n2015-11-06 One\n2015-11-06 Two")

    def test_revert_invalid(self):
        """ Test invalid input for revert. """
        command_executer(RevertCommand, ["foo"], self.todolist, None, self.out, self.error, None)
        command_executer(RevertCommand, ["ls", "foo"], self.todolist, None, self.out, self.error, None)
        command_executer(RevertCommand, ["1", "foo"], self.todolist, None, self.out, self.error, None)
        usage_text = RevertCommand([], self.todolist).usage() + '\n'
        self.assertEqual(self.errors,  usage_text*3)

    def test_revert_out_of_range(self):
        command_executer(RevertCommand, ["158"], self.todolist, None, self.out, self.error, None)
        self.assertEqual(self.errors, "Specified index is out range\n")

    def test_revert_no_todolist(self):
        """ Test attempt of revert with todolist missing """
        backup = BackupSimulator(self.todolist, self.archive, '1', ['add One'])
        command_executer(AddCommand, ["One"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '2', ['add Two'])
        command_executer(AddCommand, ["Two"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '3', ['add Three'])
        command_executer(AddCommand, ["Three"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        backup = BackupSimulator(self.todolist, self.archive, '4', ['delete Three'])
        command_executer(DeleteCommand, ["Three"], self.todolist, None, self.out, self.error, None)
        backup.save(self.todolist)

        command_executer(RevertCommand, ['1'], None, None, self.out, self.error, None)

        result = len(ChangeSet().backup_dict.keys())
        self.assertEqual(result, 4)


    def test_backup_config01(self):
        config(p_overrides={('topydo', 'backup_count'): '1'})

        self.assertEqual(config().backup_count(), 1)

    def test_backup_config02(self):
        config(p_overrides={('topydo', 'backup_count'): '0'})

        self.assertEqual(config().backup_count(), 0)

    def test_backup_config03(self):
        config(p_overrides={('topydo', 'backup_count'): '-88'})

        self.assertEqual(config().backup_count(), 0)

    def test_backup_config04(self):
        config(p_overrides={('topydo', 'backup_count'): 'foo'})

        self.assertEqual(config().backup_count(), 5)

    def test_revert_name(self):
        name = RevertCommand.name()

        self.assertEqual(name, 'revert')

    def test_help(self):
        command = RevertCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n\n" + command.help() + "\n")

    def tearDown(self):
        for filename in glob('/tmp/' + self.tmp_name + '*'):
            os.remove(filename)

if __name__ == '__main__':
    unittest.main()
