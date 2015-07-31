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
This module is aware of all supported submodules and hands out a Command
instance based on an argument list.
"""

import sys

from topydo.lib.Config import config

_SUBCOMMAND_MAP = {
    'add': 'AddCommand',
    'app': 'AppendCommand',
    'append': 'AppendCommand',
    'del': 'DeleteCommand',
    'dep': 'DepCommand',
    'depri': 'DepriCommand',
    'do': 'DoCommand',
    'edit': 'EditCommand',
    'exit': 'ExitCommand', # used for the prompt
    'ls': 'ListCommand',
    'lscon': 'ListContextCommand',
    'listcon': 'ListContextCommand',
    'listcontext': 'ListContextCommand',
    'listcontexts': 'ListContextCommand',
    'lsprj': 'ListProjectCommand',
    'lsproj': 'ListProjectCommand',
    'listprj': 'ListProjectCommand',
    'listproj': 'ListProjectCommand',
    'listproject': 'ListProjectCommand',
    'listprojects': 'ListProjectCommand',
    'postpone': 'PostponeCommand',
    'pri': 'PriorityCommand',
    'quit': 'ExitCommand',
    'rm': 'DeleteCommand',
    'sort': 'SortCommand',
    'tag': 'TagCommand',
}

def get_subcommand(p_args):
    """
    Retrieves the to-be executed Command and returns a tuple
    (Command, args).

    If args is an empty list, then the Command that corresponds with the
    default command specified in the configuration will be returned.

    If the first argument is 'help' and the second a valid subcommand, the
    help text this function returns the Command instance of that subcommand
    with a single argument 'help' (every Command has a help text).

    If no valid command could be found, the subcommand part of the tuple
    is None.
    """
    def import_subcommand(p_subcommand):
        """
        Returns the class of the requested subcommand. An invalid p_subcommand
        will result in an ImportError, since this is a programming mistake
        (most likely an error in the _SUBCOMMAND_MAP).
        """
        classname = _SUBCOMMAND_MAP[p_subcommand]
        modulename = 'topydo.commands.{}'.format(classname)

        __import__(modulename, globals(), locals(), [classname], 0)
        return getattr(sys.modules[modulename], classname)

    result = None
    args = p_args

    try:
        subcommand = p_args[0]

        if subcommand in _SUBCOMMAND_MAP:
            result = import_subcommand(subcommand)
            args = args[1:]
        elif subcommand == 'help':
            try:
                subcommand = args[1]

                if subcommand in _SUBCOMMAND_MAP:
                    args = [subcommand, 'help']
                    return get_subcommand(args)
            except IndexError:
                # will result in empty result
                pass
        else:
            p_command = config().default_command()
            if p_command in _SUBCOMMAND_MAP:
                result = import_subcommand(p_command)
                # leave args unchanged
    except IndexError:
        p_command = config().default_command()
        if p_command in _SUBCOMMAND_MAP:
            result = import_subcommand(p_command)

    return (result, args)

