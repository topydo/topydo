# Topydo - A todo.txt client written in Python.
# Copyright (C) 2015 Bram Schoenmakers <bram@topydo.org>
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

from topydo.lib.Color import AbstractColor, Color
from topydo.lib.TopydoString import TopydoString

MAIN_OPTS = "ac:C:d:ht:v"
MAIN_LONG_OPTS = ('version')
READ_ONLY_COMMANDS = ('list', 'listcontext', 'listproject')

GENERIC_HELP="""Available commands:

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
* revert
* sort
* tag

Run `topydo help <subcommand>` for command-specific help.\
"""

def usage():
    """ Prints the command-line usage of topydo. """

    print("""\
Synopsis: topydo [-a] [-c <config>] [-C <colormode>] [-d <archive>] [-t <todo.txt>] subcommand [help|args]
          topydo -h
          topydo -v

-a : Do not archive todo items on completion.
-c : Specify an alternative configuration file.
-C : Specify color mode (0 = disable, 1 = enable 16 colors,
     16 = enable 16 colors, 256 = enable 256 colors, auto (default))
-d : Specify an alternative archive file (done.txt)
-h : This help text
-t : Specify an alternative todo file
-v : Print version and exit

""" + GENERIC_HELP)

def write(p_file, p_string):
    """
    Write p_string to file p_file, trailed by a newline character.

    ANSI codes are removed when the file is not a TTY (and colors are
    automatically determined).
    """
    if not config().colors(p_file.isatty()):
        p_string = escape_ansi(p_string)

    if p_string:
        p_file.write(p_string + "\n")


def lookup_color(p_color):
    """
    Converts an AbstractColor to a normal Color. Returns the Color itself
    when a normal color is passed.
    """
    if not lookup_color.colors:
        lookup_color.colors[AbstractColor.NEUTRAL] = Color('NEUTRAL')
        lookup_color.colors[AbstractColor.PROJECT] = config().project_color()
        lookup_color.colors[AbstractColor.CONTEXT] = config().context_color()
        lookup_color.colors[AbstractColor.META] = config().metadata_color()
        lookup_color.colors[AbstractColor.LINK] = config().link_color()

    try:
        return lookup_color.colors[p_color]
    except KeyError:
        return p_color

lookup_color.colors = {}

def insert_ansi(p_string):
    """ Returns a string with color information at the right positions.  """
    result = p_string.data

    for pos, color in sorted(p_string.colors.items(), reverse=True):
        color = lookup_color(color)

        result = result[:pos] + color.as_ansi() + result[pos:]

    return result

def output(p_string):
    if isinstance(p_string, list):
        p_string = "\n".join([insert_ansi(s) for s in p_string])
    elif isinstance(p_string, TopydoString):
        # convert color codes to ANSI
        p_string = insert_ansi(p_string)

    write(sys.stdout, p_string)

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

from topydo.lib import TodoFile
from topydo.lib import TodoList
from topydo.lib import TodoListBase
from topydo.lib.Utils import escape_ansi


def _retrieve_archive():
    """
    Returns a tuple with archive content: the first element is a TodoListBase
    and the second element is a TodoFile.
    """
    archive_file = TodoFile.TodoFile(config().archive())
    archive = TodoListBase.TodoListBase(archive_file.read())

    return (archive, archive_file)


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
        self._post_archive_action = None
        self.backup = None

    @staticmethod
    def _usage():
        usage()
        sys.exit(0)

    def _process_flags(self):
        args = sys.argv[1:]

        try:
            opts, args = getopt.getopt(args, MAIN_OPTS, MAIN_LONG_OPTS)
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
            elif opt == "-C":
                overrides[('topydo', 'force_colors')] = '1'
                overrides[('topydo', 'colors')] = value
            elif opt == "-t":
                overrides[('topydo', 'filename')] = value
            elif opt == "-d":
                overrides[('topydo', 'archive_filename')] = value
            elif opt in ("-v", "--version"):
                version()
            else:
                CLIApplicationBase._usage()

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
        archive, archive_file = _retrieve_archive()

        if self.backup:
            self.backup.add_archive(archive)

        if archive:
            from topydo.commands.ArchiveCommand import ArchiveCommand
            command = ArchiveCommand(self.todolist, archive)
            command.execute()

            if archive.dirty:
                archive_file.write(archive.print_todos())

    @staticmethod
    def is_read_only(p_command):
        """ Returns True when the given command class is read-only. """
        read_only_commands = tuple(cmd for cmd
                                   in ('revert', ) + READ_ONLY_COMMANDS)
        return p_command.name() in read_only_commands

    def _backup(self, p_command, p_args=None, p_label=None):
        if config().backup_count() > 0 and p_command and not CLIApplicationBase.is_read_only(p_command):
            p_args = p_args if p_args else []
            call = [p_command.name()] + p_args

            from topydo.lib.ChangeSet import ChangeSet
            label = p_label if p_label else call
            self.backup = ChangeSet(self.todolist, p_label=label)

    def _execute(self, p_command, p_args):
        """
        Execute a subcommand with arguments. p_command is a class (not an
        object).
        """
        self._backup(p_command, p_args)

        command = p_command(
            p_args,
            self.todolist,
            output,
            error,
            input)

        if command.execute() != False:
            self._post_archive_action = command.execute_post_archive_actions
            return True

        return False

    def _post_execute(self):
        """
        Should be called when executing the user requested command has been
        completed. It will do some maintenance and write out the final result
        to the todo.txt file.
        """

        if self.todolist.dirty:
            # do not archive when the value of the filename is an empty string
            # (i.e. explicitly left empty in the configuration
            if self.do_archive and config().archive():
                self._archive()
            elif config().archive() and self.backup:
                archive = _retrieve_archive()[0]
                self.backup.add_archive(archive)

            self._post_archive_action()

            if config().keep_sorted():
                from topydo.commands.SortCommand import SortCommand
                self._execute(SortCommand, [])

            if self.backup:
                self.backup.save(self.todolist)

            self.todofile.write(self.todolist.print_todos())
            self.todolist.dirty = False

        self.backup = None

    def run(self):
        raise NotImplementedError
