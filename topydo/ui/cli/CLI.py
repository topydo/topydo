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

""" Entry file for the Python todo.txt CLI. """

import sys

from topydo.Commands import get_subcommand
from topydo.lib import TodoFile, TodoList
from topydo.lib.Config import ConfigError, config
from topydo.ui.CLIApplicationBase import CLIApplicationBase, error

# First thing is to poke the configuration and check whether it's sane
# The modules below may already read in configuration upon import, so
# make sure to bail out if the configuration is invalid.
try:
    config()
except ConfigError as config_error:
    error(str(config_error))
    sys.exit(1)



class CLIApplication(CLIApplicationBase):
    """
    Class that represents the (original) Command Line Interface of Topydo.
    """

    def __init__(self):
        super().__init__()

    def run(self):
        """ Main entry function. """
        args = self._process_flags()

        self.todofile = TodoFile.TodoFile(config().todotxt())
        self.todolist = TodoList.TodoList(self.todofile.read())

        try:
            (subcommand, args) = get_subcommand(args)
        except ConfigError as ce:
            error('Error: ' + str(ce) + '. Check your aliases configuration')
            sys.exit(1)

        if subcommand is None:
            CLIApplicationBase._usage()

        if self._execute(subcommand, args) == False:
            sys.exit(1)
        else:
            self._post_execute()


def main():
    """ Main entry point of the CLI. """
    CLIApplication().run()

if __name__ == '__main__':
    main()
