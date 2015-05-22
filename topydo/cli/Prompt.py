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

""" Entry file for the topydo Prompt interface (CLI). """

import sys

from topydo.cli.CLIApplicationBase import CLIApplicationBase, error, usage
from topydo.cli.TopydoCompleter import TopydoCompleter
from prompt_toolkit.shortcuts import get_input
from prompt_toolkit.history import History

from topydo.lib.Config import config, ConfigError

# First thing is to poke the configuration and check whether it's sane
# The modules below may already read in configuration upon import, so
# make sure to bail out if the configuration is invalid.
try:
    config()
except ConfigError as config_error:
    error(str(config_error))
    sys.exit(1)

from topydo.Commands import get_subcommand
from topydo.commands.SortCommand import SortCommand
from topydo.lib import TodoFile
from topydo.lib import TodoList

class PromptApplication(CLIApplicationBase):
    """
    This class implements a variant of topydo's CLI showing a shell and
    offering auto-completion thanks to the prompt toolkit.
    """
    def __init__(self):
        super(PromptApplication, self).__init__()

    def run(self):
        """ Main entry function. """
        args = self._process_flags()

        self.todofile = TodoFile.TodoFile(self.path)
        self.todolist = TodoList.TodoList(self.todofile.read())

        # suppress upstream issue with Python 2.7
        # pylint: disable=no-value-for-parameter
        completer = TopydoCompleter(self.todolist)
        history = History()

        while True:
            try:
                user_input = get_input(u'topydo> ', history=history, completer=completer).split()
            except (EOFError, KeyboardInterrupt):
                sys.exit(0)

            (subcommand, args) = get_subcommand(user_input)

            try:
                if self._execute(subcommand, args) != False:
                    if self.todolist.is_dirty():
                        self._archive()

                        if config().keep_sorted():
                            self._execute(SortCommand, [])

                        self.todofile.write(str(self.todolist))
            except TypeError:
                usage()

def main():
    """ Main entry point of the CLI. """
    PromptApplication().run()

if __name__ == '__main__':
    main()
