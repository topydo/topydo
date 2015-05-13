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

from topydo.lib.Config import config

from topydo.lib.AddCommand import AddCommand
from topydo.lib.AppendCommand import AppendCommand
from topydo.lib.DeleteCommand import DeleteCommand
from topydo.lib.DepCommand import DepCommand
from topydo.lib.DepriCommand import DepriCommand
from topydo.lib.DoCommand import DoCommand
from topydo.lib.EditCommand import EditCommand
from topydo.lib.IcalCommand import IcalCommand
from topydo.lib.ListCommand import ListCommand
from topydo.lib.ListContextCommand import ListContextCommand
from topydo.lib.ListProjectCommand import ListProjectCommand
from topydo.lib.PostponeCommand import PostponeCommand
from topydo.lib.PriorityCommand import PriorityCommand
from topydo.lib.SortCommand import SortCommand
from topydo.lib.TagCommand import TagCommand

_SUBCOMMAND_MAP = {
    'add': AddCommand,
    'app': AppendCommand,
    'append': AppendCommand,
    'del': DeleteCommand,
    'dep': DepCommand,
    'depri': DepriCommand,
    'do': DoCommand,
    'edit': EditCommand,
    'ical': IcalCommand,
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
    result = None
    args = p_args

    try:
        subcommand = p_args[0]

        if subcommand in _SUBCOMMAND_MAP:
            result = _SUBCOMMAND_MAP[subcommand]
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
                result = _SUBCOMMAND_MAP[p_command]
                # leave args unchanged
    except IndexError:
        p_command = config().default_command()
        if p_command in _SUBCOMMAND_MAP:
            result = _SUBCOMMAND_MAP[p_command]

    return (result, args)

