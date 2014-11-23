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

""" Provides a function to pretty print a list of todo items. """

import re

from topydo.lib.Config import config

PRIORITY_COLORS = {
    'A': '\033[36m', # cyan
    'B': '\033[33m', # yellow
    'C': '\033[34m'  # blue
}

PROJECT_COLOR = '\033[31m' # red
NEUTRAL_COLOR = '\033[0m'

def pp_color(p_todo_str, p_todo):
    """
    Adds colors to the todo string by inserting ANSI codes.

    Should be passed as a filter in the filter list of pretty_print()
    """

    if config().colors():
        color = NEUTRAL_COLOR
        try:
            color = PRIORITY_COLORS[p_todo.priority()]
        except KeyError:
            pass

        p_todo_str = '%s%s%s' % (color, p_todo_str, NEUTRAL_COLOR)

        if config().highlight_projects_contexts():
            p_todo_str = re.sub(
                r'\B(\+|@)(\S*\w)',
                PROJECT_COLOR + r'\g<0>' + color,
                p_todo_str)

        p_todo_str += NEUTRAL_COLOR

    return p_todo_str

def pp_indent(p_indent=0):
    return lambda s, t: ' ' * p_indent + s

def pretty_print(p_todo, p_filters=None):
    """
    Given a todo item, pretty print it and return a list of formatted strings.

    p_filters is a list of functions that transform the output string, each
    function accepting two arguments:

    * the todo's text that has to be modified;
    * the todo object itself which allows for obtaining relevant information.

    Example is pp_color in this fle.
    """
    p_filters = p_filters or []

    todo_str = str(p_todo)

    for f in p_filters:
        todo_str = f(todo_str, p_todo)

    return todo_str

def pretty_print_list(p_todos, p_filters=None):
    """
    Given a list of todo items, pretty print it and return a list of
    formatted strings.
    """
    p_filters = p_filters or []
    return [pretty_print(todo, p_filters) for todo in p_todos]
