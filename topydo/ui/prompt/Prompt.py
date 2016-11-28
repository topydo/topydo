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

""" Entry file for the topydo Prompt interface (CLI). """

import os.path
import shlex
import sys

from topydo.ui.CLIApplicationBase import CLIApplicationBase, error, usage
from topydo.ui.prompt.TopydoCompleter import TopydoCompleter
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.history import InMemoryHistory

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
from topydo.lib.TodoFileWatched import TodoFileWatched
from topydo.lib import TodoList


class PromptApplication(CLIApplicationBase):
    """
    This class implements a variant of topydo's CLI showing a shell and
    offering auto-completion thanks to the prompt toolkit.
    """

    def __init__(self):
        super().__init__()

        self._process_flags()
        self.completer = None
        self.todofile = TodoFileWatched(config().todotxt(), self._load_file)

    def _load_file(self):
        """
        Reads the configured todo.txt file and loads it into the todo list
        instance.
        """
        self.todolist.erase()
        self.todolist.add_list(self.todofile.read())
        self.completer = TopydoCompleter(self.todolist)

    def run(self):
        """ Main entry function. """
        history = InMemoryHistory()
        self._load_file()

        while True:
            # (re)load the todo.txt file (only if it has been modified)

            try:
                user_input = prompt(u'topydo> ', history=history,
                                    completer=self.completer,
                                    complete_while_typing=False)
                user_input = shlex.split(user_input)
            except EOFError:
                sys.exit(0)
            except KeyboardInterrupt:
                continue
            except ValueError as verr:
                error('Error: ' + str(verr))
                continue

            try:
                (subcommand, args) = get_subcommand(user_input)
            except ConfigError as ce:
                error('Error: ' + str(ce) + '. Check your aliases configuration')
                continue

            try:
                if self._execute(subcommand, args) != False:
                    self._post_execute()
            except TypeError:
                usage()


def main():
    """ Main entry point of the prompt interface. """
    PromptApplication().run()

if __name__ == '__main__':
    main()
