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

import os
import tempfile
import unittest

from datetime import date
from glob import glob
from six import u
from uuid import uuid4

from test.command_testcase import CommandTest
from topydo.commands.AddCommand import AddCommand
from topydo.commands.ArchiveCommand import ArchiveCommand
from topydo.commands.DeleteCommand import DeleteCommand
from topydo.commands.DoCommand import DoCommand
from topydo.commands.RevertCommand import RevertCommand
from topydo.lib.ChangeSet import ChangeSet
from topydo.lib.Config import config
from topydo.lib.TodoFile import TodoFile
from topydo.lib.TodoList import TodoList

class RevertCommandTest(CommandTest):
    def setUp(self):
        super(RevertCommandTest, self).setUp()
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
        backup = ChangeSet(p_call=['do 1'])
        backup.add_todolist(self.todolist)
        backup.add_archive(self.archive)
        backup.timestamp = '1'
        command = DoCommand(["1"], self.todolist, self.out, self.error, None)
        command.execute()
        archive_command = ArchiveCommand(self.todolist, self.archive)
        archive_command.execute()
        self.archive_file.write(self.archive.print_todos())
        backup.save(self.todolist)

        self.assertEqual(self.archive.print_todos(), "x {} Foo".format(self.today))
        self.assertEqual(self.todolist.print_todos(), "Bar\nBaz")

        revert_command = RevertCommand([], self.todolist, self.out, self.error, None)
        revert_command.execute()

        result = TodoList(self.archive_file.read()).print_todos()

        self.assertEqual(self.errors, "")
        self.assertTrue(self.output.endswith("Successfully reverted: do 1\n"))
        self.assertEqual(result, "")
        self.assertEqual(self.todolist.print_todos(), "Foo\nBar\nBaz")

    def test_revert02(self):
        backup = ChangeSet(self.todolist, self.archive, ['do 1'])
        backup.timestamp = '1'
        command1 = DoCommand(["1"], self.todolist, self.out, self.error, None)
        command1.execute()
        archive_command1 = ArchiveCommand(self.todolist, self.archive)
        archive_command1.execute()
        self.archive_file.write(self.archive.print_todos())
        backup.save(self.todolist)

        backup = ChangeSet(self.todolist, self.archive, ['do Bar'])
        backup.timestamp = '2'
        command2 = DoCommand(["Bar"], self.todolist, self.out, self.error, None)
        command2.execute()
        archive_command2 = ArchiveCommand(self.todolist, self.archive)
        archive_command2.execute()
        self.archive_file.write(self.archive.print_todos())
        backup.save(self.todolist)

        self.assertEqual(self.archive.print_todos(), "x {t} Foo\nx {t} Bar".format(t=self.today))
        self.assertEqual(self.todolist.print_todos(), "Baz")

        revert_command = RevertCommand([], self.todolist, self.out, self.error, None)
        revert_command.execute()

        result = TodoList(self.archive_file.read()).print_todos()

        self.assertEqual(self.errors, "")
        self.assertTrue(self.output.endswith("Successfully reverted: do Bar\n"))
        self.assertEqual(result, "x {} Foo".format(self.today))
        self.assertEqual(self.todolist.print_todos(), "Bar\nBaz")

    def test_revert03(self):
        """ Test behavior when no backup is found """
        command = RevertCommand([], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.errors, "No backup was found for the current state of {}\n".format(config().todotxt()))

    def test_revert04(self):
        """ Test trimming of the backup_file """
        backup = ChangeSet(self.todolist, self.archive, ['add One'])
        backup.timestamp = '1'
        command1 = AddCommand(["One"], self.todolist, self.out, self.error, None)
        command1.execute()
        backup.save(self.todolist)

        backup = ChangeSet(self.todolist, self.archive, ['add Two'])
        backup.timestamp = '2'
        command2 = AddCommand(["Two"], self.todolist, self.out, self.error, None)
        command2.execute()
        backup.save(self.todolist)

        backup = ChangeSet(self.todolist, self.archive, ['add Three'])
        backup.timestamp = '3'
        command3 = AddCommand(["Three"], self.todolist, self.out, self.error, None)
        command3.execute()
        backup.save(self.todolist)

        backup = ChangeSet(self.todolist, self.archive, ['add Four'])
        backup.timestamp = '4'
        command4 = AddCommand(["Four"], self.todolist, self.out, self.error, None)
        command4.execute()
        backup.save(self.todolist)

        backup = ChangeSet(self.todolist, self.archive, ['add Five'])
        backup.timestamp = '5'
        command5 = AddCommand(["Five"], self.todolist, self.out, self.error, None)
        command5.execute()
        backup.save(self.todolist)

        result = len(ChangeSet().backup_dict.keys())
        self.assertEqual(result, 6)

        backup = ChangeSet(self.todolist, self.archive, ['add Six'])
        backup.timestamp = '6'
        command6 = AddCommand(["Six"], self.todolist, self.out, self.error, None)
        command6.execute()
        backup.save(self.todolist)

        backup = ChangeSet(self.todolist, self.archive, ['add Seven'])
        backup.timestamp = '7'
        command7 = AddCommand(["Seven"], self.todolist, self.out, self.error, None)
        command7.execute()
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
        self.assertTrue(self.output.endswith("Successfully reverted: add Seven\n"))

    def test_revert05(self):
        """ Test for possible backup collisions """
        backup = ChangeSet(self.todolist, self.archive, ['add One'])
        backup.timestamp = '1'
        command1 = AddCommand(["One"], self.todolist, self.out, self.error, None)
        command1.execute()
        backup.save(self.todolist)

        backup = ChangeSet(self.todolist, self.archive, ['add Two'])
        backup.timestamp = '2'
        command2 = AddCommand(["Two"], self.todolist, self.out, self.error, None)
        command2.execute()
        backup.save(self.todolist)

        backup = ChangeSet(self.todolist, self.archive, ['add Three'])
        backup.timestamp = '3'
        command3 = AddCommand(["Three"], self.todolist, self.out, self.error, None)
        command3.execute()
        backup.save(self.todolist)

        backup = ChangeSet(self.todolist, self.archive, ['delete Three'])
        backup.timestamp = '4'
        command4 = DeleteCommand(["Three"], self.todolist, self.out, self.error, None)
        command4.execute()
        backup.save(self.todolist)

        backup = ChangeSet(self.todolist, self.archive, ['add Four'])
        backup.timestamp = '5'
        command4 = AddCommand(["Four"], self.todolist, self.out, self.error, None)
        command4.execute()
        backup.save(self.todolist)

        revert_command = RevertCommand([], self.todolist, self.out, self.error, None)
        revert_command.execute()
        self.assertEqual(self.errors, "")
        self.assertTrue(self.output.endswith("Successfully reverted: add Four\n"))
        self.assertEqual(self.todolist.print_todos(), "Foo\nBar\nBaz\n{t} One\n{t} Two".format(t=self.today))

        revert_command = RevertCommand([], self.todolist, self.out, self.error, None)
        revert_command.execute()
        self.assertEqual(self.errors, "")
        self.assertTrue(self.output.endswith("Successfully reverted: delete Three\n"))
        self.assertEqual(self.todolist.print_todos(), "Foo\nBar\nBaz\n{t} One\n{t} Two\n{t} Three".format(t=self.today))

        revert_command = RevertCommand([], self.todolist, self.out, self.error, None)
        revert_command.execute()
        self.assertEqual(self.errors, "")
        self.assertTrue(self.output.endswith("Successfully reverted: add Three\n"))
        self.assertEqual(self.todolist.print_todos(), "Foo\nBar\nBaz\n{t} One\n{t} Two".format(t=self.today))

        revert_command = RevertCommand([], self.todolist, self.out, self.error, None)
        revert_command.execute()
        self.assertEqual(self.errors, "")
        self.assertTrue(self.output.endswith("Successfully reverted: add Two\n"))
        self.assertEqual(self.todolist.print_todos(), "Foo\nBar\nBaz\n{t} One".format(t=self.today))

        revert_command = RevertCommand([], self.todolist, self.out, self.error, None)
        revert_command.execute()
        self.assertEqual(self.errors, "")
        self.assertTrue(self.output.endswith("Successfully reverted: add One\n"))
        self.assertEqual(self.todolist.print_todos(), "Foo\nBar\nBaz")

    def test_revert06(self):
        """ Test attempt of deletion with non-existing backup key"""
        backup = ChangeSet(self.todolist, self.archive, ['add One'])
        backup.timestamp = '1'
        command1 = AddCommand(["One"], self.todolist, self.out, self.error, None)
        command1.execute()
        backup.save(self.todolist)

        backup = ChangeSet(self.todolist, self.archive, ['add Two'])
        backup.timestamp = '2'
        command2 = AddCommand(["Two"], self.todolist, self.out, self.error, None)
        command2.execute()
        backup.save(self.todolist)

        backup = ChangeSet(self.todolist, self.archive, ['add Three'])
        backup.timestamp = '3'
        command3 = AddCommand(["Three"], self.todolist, self.out, self.error, None)
        command3.execute()
        backup.save(self.todolist)

        backup = ChangeSet(self.todolist, self.archive, ['delete Three'])
        backup.timestamp = '4'
        command4 = DeleteCommand(["Three"], self.todolist, self.out, self.error, None)
        command4.execute()
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
