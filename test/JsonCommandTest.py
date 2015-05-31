# Topydo - A todo.txt client written in Python.
# Copyright (C) 2015 Bram Schoenmakers <me@bramschoenmakers.nl>
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

import codecs
import re
import sys
import unittest

from topydo.lib.Config import config
from topydo.commands.JsonCommand import JsonCommand
from test.CommandTest import CommandTest, utf8
from test.TestFacilities import load_file_to_todolist

class JsonCommandTest(CommandTest):
    def setUp(self):
        super(JsonCommandTest, self).setUp()
        self.todolist = load_file_to_todolist("test/data/ListCommandTest.txt")

    def test_json(self):
        command = JsonCommand([""], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())

        jsontext = ""
        with codecs.open('test/data/ListCommandTest.json', 'r', encoding='utf-8') as json:
            jsontext = json.read()

        self.assertEqual(self.output, jsontext)
        self.assertEqual(self.errors, "")

    def test_help(self):
        command = JsonCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n\n" + command.help() + "\n")

class JsonCommandUnicodeTest(CommandTest):
    def setUp(self):
        super(JsonCommandUnicodeTest, self).setUp()
        self.todolist = load_file_to_todolist("test/data/ListCommandUnicodeTest.txt")

    def test_json_unicode(self):
        command = JsonCommand([""], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())

        jsontext = ""
        with codecs.open('test/data/ListCommandUnicodeTest.json', 'r', encoding='utf-8') as json:
            jsontext = json.read()

        self.assertEqual(self.output, utf8(jsontext))
        self.assertEqual(self.errors, "")

if __name__ == '__main__':
    unittest.main()
