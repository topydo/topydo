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

"""
Contains a base class for a CLI implementation of topydo and functions for the
I/O on the command-line.
"""

import getopt
import sys
from six import PY2
from six.moves import input

MAIN_OPTS = "ac:d:ht:v"

def usage():
    """ Prints the command-line usage of topydo. """

    print("""\
Synopsis: topydo [-a] [-c <config>] [-d <archive>] [-t <todo.txt>] subcommand [help|args]
          topydo -h
          topydo -v

-a : Do not archive todo items on completion.
-c : Specify an alternative configuration file.
-d : Specify an alternative archive file (done.txt)
-h : This help text
-t : Specify an alternative todo file
-v : Print version and exit

Available commands:

* add
* append (app)
* del (rm)
* dep
* depri
* do
* edit
* ls
* listcon (lscon)
* listprojects (lsprj)
* postpone
* pri
* sort
* tag

Run `topydo help <subcommand>` for command-specific help.
""")

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

def version():
    """ Print the current version and exit. """
    from topydo.lib.Version import VERSION, LICENSE
    print("topydo {}\n".format(VERSION))
    print(LICENSE)
    sys.exit(0)

from topydo.lib.Config import config, ConfigError

# First thing is to poke the configuration and check whether it's sane
# The modules below may already read in configuration upon import, so
# make sure to bail out if the configuration is invalid.
try:
    config()
except ConfigError as config_error:
    error(str(config_error))
    sys.exit(1)

from topydo.commands.ArchiveCommand import ArchiveCommand
from topydo.commands.SortCommand import SortCommand
from topydo.lib import TodoFile
from topydo.lib import TodoList
from topydo.lib import TodoListBase
from topydo.lib.Utils import escape_ansi

class CLIApplicationBase(object):
    """
    Base class for a Command Line Interfaces (CLI) for topydo. Examples are the
    original CLI and the Prompt interface.

    Handles input/output of the various subcommands.
    """
    def __init__(self):
        self.todolist = TodoList.TodoList([])
        self.todofile = None
        self.do_archive = True

    def _usage(self):
        usage()
        sys.exit(0)

    def _process_flags(self):
        args = sys.argv[1:]

        if PY2:
            args = [arg.decode('utf-8') for arg in args]

        try:
            opts, args = getopt.getopt(args, MAIN_OPTS)
        except getopt.GetoptError as e:
            error(str(e))
            sys.exit(1)

        alt_config_path = None
        overrides = {}

        for opt, value in opts:
            if opt == "-a":
                self.do_archive = False
            elif opt == "-c":
                alt_config_path = value
            elif opt == "-t":
                overrides[('topydo', 'filename')] = value
            elif opt == "-d":
                overrides[('topydo', 'archive_filename')] = value
            elif opt == "-v":
                version()
            else:
                self._usage()

        if alt_config_path:
            config(alt_config_path, overrides)
        elif len(overrides):
            config(p_overrides=overrides)

        return args

    def _archive(self):
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
                archive_file.write(archive.print_todos())

    def _help(self, args):
        if args == None:
            pass # TODO
        else:
            pass # TODO

    def _input(self):
        """
        Returns a function that retrieves user input.
        """
        return input

    def _execute(self, p_command, p_args):
        """
        Execute a subcommand with arguments. p_command is a class (not an
        object).
        """
        command = p_command(
            p_args,
            self.todolist,
            lambda o: write(sys.stdout, o),
            error,
            self._input())

        if command.execute() != False:
            return True

        return False

    def _post_execute(self):
        """
        Should be called when executing the user requested command has been
        completed. It will do some maintenance and write out the final result
        to the todo.txt file.
        """

        # do not archive when the value of the filename is an empty string
        # (i.e. explicitly left empty in the configuration
        if self.todolist.is_dirty():
            if self.do_archive and config().archive():
                self._archive()

            if config().keep_sorted():
                self._execute(SortCommand, [])

            self.todofile.write(self.todolist.print_todos())

    def run(self):
        raise NotImplementedError

