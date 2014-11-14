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

""" Entry file for the Python todo.txt CLI. """

import sys

def usage():
    """ Prints the usage of the todo.txt CLI """
    exit(1)

def arguments(p_start=2):
    """
    Retrieves all values from the argument list starting from the given
    position.

    This is a parameter, because argv has a different structure when no
    subcommand was given and it fallbacks to the default subcommand.
    """
    try:
        values = sys.argv[p_start:]
    except IndexError:
        usage()

    return values

def write(p_file, p_string):
    """
    Write p_string to file p_file, trailed by a newline character.

    ANSI codes are removed when the file is not a TTY.
    """
    if not p_file.isatty():
        p_string = escape_ansi(p_string)

    if p_string:
        p_file.write(p_string + "\n")

def error(p_string):
    """ Writes an error on the standard error. """

    write(sys.stderr, p_string)

from topydo.lib.Config import config, ConfigError

# First thing is to poke the configuration and check whether it's sane
# The modules below may already read in configuration upon import, so
# make sure to bail out if the configuration is invalid.
try:
    config()
except ConfigError as e:
    error(str(e))
    exit(1)

from topydo.lib.AddCommand import AddCommand
from topydo.lib.AppendCommand import AppendCommand
from topydo.lib.ArchiveCommand import ArchiveCommand
from topydo.lib.DeleteCommand import DeleteCommand
from topydo.lib.DepCommand import DepCommand
from topydo.lib.DepriCommand import DepriCommand
from topydo.lib.DoCommand import DoCommand
from topydo.lib.ListCommand import ListCommand
from topydo.lib.ListContextCommand import ListContextCommand
from topydo.lib.ListProjectCommand import ListProjectCommand
from topydo.lib.PostponeCommand import PostponeCommand
from topydo.lib.PrettyPrinter import *
from topydo.lib.PriorityCommand import PriorityCommand
from topydo.lib.SortCommand import SortCommand
from topydo.lib.TagCommand import TagCommand
from topydo.lib import TodoFile
from topydo.lib import TodoList
from topydo.lib import TodoListBase
from topydo.lib.Utils import escape_ansi

class CLIApplication(object):
    def __init__(self):
        self.todolist = TodoList.TodoList([])

    def archive(self):
        """
        Performs an archive action on the todolist.

        This means that all completed tasks are moved to the archive file
        (defaults to done.txt).
        """
        archive_file = TodoFile.TodoFile(config().archive())
        archive = TodoListBase.TodoListBase(archive_file.read())

        if archive:
            command = ArchiveCommand(self.todolist, archive)
            command.execute()

            if archive.is_dirty():
                archive_file.write(str(archive))

    def run(self):
        """ Main entry function. """
        todofile = TodoFile.TodoFile(config().todotxt())
        self.todolist = TodoList.TodoList(todofile.read())

        try:
            subcommand = sys.argv[1]
        except IndexError:
            subcommand = config().default_command()

        subcommand_map = {
          'add': AddCommand,
          'app': AppendCommand,
          'append': AppendCommand,
          'del': DeleteCommand,
          'dep': DepCommand,
          'depri': DepriCommand,
          'do': DoCommand,
          'ls': ListCommand,
          'lscon': ListContextCommand,
          'listcon': ListContextCommand,
          'lsprj': ListProjectCommand,
          'lsproj': ListProjectCommand,
          'listprj': ListProjectCommand,
          'listproj': ListProjectCommand,
          'listproject': ListProjectCommand,
          'listprojects': ListProjectCommand,
          'postpone': PostponeCommand,
          'pri': PriorityCommand,
          'rm': DeleteCommand,
          'sort': SortCommand,
          'tag': TagCommand,
        }

        args = arguments()
        if not subcommand in subcommand_map:
            subcommand = config().default_command()
            args = arguments(1)

        command = subcommand_map[subcommand](args, self.todolist,
            lambda o: write(sys.stdout, o),
            error,
            raw_input)

        if command.execute() == False:
            exit(1)

        if self.todolist.is_dirty():
            self.archive()
            todofile.write(str(self.todolist))

if __name__ == '__main__':
    CLIApplication().run()
