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

from topydo.Commands import get_subcommand
from topydo.commands.AddCommand import AddCommand
from topydo.commands.DeleteCommand import DeleteCommand
from topydo.commands.ListCommand import ListCommand
from topydo.commands.TagCommand import TagCommand
from topydo.lib.Config import ConfigError, config

from .topydo_testcase import TopydoTest


class GetSubcommandTest(TopydoTest):
    def test_normal_cmd(self):
        args = ["add"]
        real_cmd, _ = get_subcommand(args)
        self.assertTrue(issubclass(real_cmd, AddCommand))

    def test_cmd_help(self):
        args = ["help", "add"]
        real_cmd, final_args = get_subcommand(args)
        self.assertTrue(issubclass(real_cmd, AddCommand))
        self.assertEqual(final_args, ["help"])

    def test_alias01(self):
        config("test/data/aliases.conf")

        args = ["foo"]
        real_cmd, final_args = get_subcommand(args)
        self.assertTrue(issubclass(real_cmd, DeleteCommand))
        self.assertEqual(final_args, ["-f", "test"])

    def test_alias02(self):
        config("test/data/aliases.conf")

        args = ["format"]
        real_cmd, final_args = get_subcommand(args)
        self.assertTrue(issubclass(real_cmd, ListCommand))
        self.assertEqual(final_args, ["-F", "|I| x c d {(}p{)} s k", "-n", "25"])

    def test_alias03(self):
        config("test/data/aliases.conf")

        args = ["smile"]
        real_cmd, final_args = get_subcommand(args)
        self.assertTrue(issubclass(real_cmd, ListCommand))
        self.assertEqual(final_args, [u"\u263b"])

    def test_alias04(self):
        config("test/data/aliases.conf")

        args = ["star", "foo"]
        real_cmd, final_args = get_subcommand(args)
        self.assertTrue(issubclass(real_cmd, TagCommand))
        self.assertEqual(final_args, ["foo", "star", "1"])

    def test_default_cmd01(self):
        args = ["bar"]
        real_cmd, final_args = get_subcommand(args)
        self.assertTrue(issubclass(real_cmd, ListCommand))
        self.assertEqual(final_args, ["bar"])

    def test_default_cmd02(self):
        args = []
        real_cmd, final_args = get_subcommand(args)
        self.assertTrue(issubclass(real_cmd, ListCommand))
        self.assertEqual(final_args, [])

    def test_alias_default_cmd01(self):
        config("test/data/aliases.conf", {('topydo', 'default_command'): 'foo'})

        args = ["bar"]
        real_cmd, final_args = get_subcommand(args)
        self.assertTrue(issubclass(real_cmd, DeleteCommand))
        self.assertEqual(final_args, ["-f", "test", "bar"])

    def test_alias_default_cmd02(self):
        config("test/data/aliases.conf", {('topydo', 'default_command'): 'foo'})

        args = []
        real_cmd, final_args = get_subcommand(args)
        self.assertTrue(issubclass(real_cmd, DeleteCommand))
        self.assertEqual(final_args, ["-f", "test"])

    def test_alias_default_cmd03(self):
        config("test/data/aliases.conf", {('topydo', 'default_command'): 'nonexisting_default'})

        args = ['nonexisting']
        real_cmd, final_args = get_subcommand(args)
        self.assertFalse(real_cmd)
        self.assertEqual(final_args, ['nonexisting'])

    def test_alias_default_cmd04(self):
        config("test/data/aliases.conf", {('topydo', 'default_command'): 'nonexisting_default'})

        args = []
        real_cmd, final_args = get_subcommand(args)
        self.assertFalse(real_cmd)
        self.assertEqual(final_args, [])

    def test_wrong_alias(self):
        config("test/data/aliases.conf")

        args = ["baz"]
        real_cmd, _ = get_subcommand(args)
        self.assertEqual(real_cmd, None)

    def test_alias_quotation(self):
        config("test/data/aliases.conf")

        args = ["quot"]
        with self.assertRaises(ConfigError) as ce:
            get_subcommand(args)

        self.assertEqual(str(ce.exception), 'No closing quotation')

    def test_help(self):
        real_cmd, final_args = get_subcommand(['help', 'nonexisting'])
        self.assertFalse(real_cmd)
        self.assertEqual(final_args, ['help', 'nonexisting'])

if __name__ == '__main__':
    unittest.main()
