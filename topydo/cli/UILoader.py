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

""" Entry file for the Python todo.txt CLI. """

import sys
from topydo.cli.CLI import CLIApplication
from topydo.cli.Prompt import PromptApplication

def main():
    """ Main entry point of the CLI. """
    try:
        if sys.argv[1] == 'prompt':
            PromptApplication().run()
        else:
            CLIApplication().run()
    except IndexError:
        CLIApplication().run()

if __name__ == '__main__':
    main()
