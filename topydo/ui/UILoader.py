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

import getopt
import sys

from topydo.ui.cli.CLI import CLIApplication
from topydo.ui.CLIApplicationBase import MAIN_OPTS, MAIN_LONG_OPTS, error

# enable color on windows CMD
if "win32" in sys.platform:
    import colorama
    colorama.init()


def main():
    """ Main entry point of the CLI. """
    try:
        args = sys.argv[1:]

        try:
            _, args = getopt.getopt(args, MAIN_OPTS, MAIN_LONG_OPTS)
        except getopt.GetoptError as e:
            error(str(e))
            sys.exit(1)

        if args[0] == 'prompt':
            try:
                from topydo.ui.prompt.Prompt import PromptApplication
                PromptApplication().run()
            except ImportError:
                error("Some additional dependencies for prompt mode were not installed, please install with 'pip install topydo[prompt]'")
        elif args[0] == 'columns':
            try:
                from topydo.ui.columns.Main import UIApplication
                UIApplication().run()
            except ImportError:
                error("Some additional dependencies for column mode were not installed, please install with 'pip install topydo[columns]'")
        else:
            CLIApplication().run()
    except IndexError:
        CLIApplication().run()

if __name__ == '__main__':
    main()
