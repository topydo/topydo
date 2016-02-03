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

""" This module serves for managing output colors. """

from topydo.lib.Config import config
from topydo.lib.Colorblock import progress_color_code

NEUTRAL_COLOR = 0
PROJECT_COLOR = 1
CONTEXT_COLOR = 2
PRIORITY_COLOR = 3
LINK_COLOR = 4
METADATA_COLOR = 5
PROGRESS_COLOR = 6

def get_color(p_type, p_todo, p_256color=False):
    """
    Returns an integer representing a color.

    With 16 colors, an integer [0..16] is returned, with 256 colors the
    corresponding xterm code is returned.

    -1 represents the neutral color.
    """
    def normalize_color(p_input):
        color_names_dict = {
            'black': 0,
            'red': 1,
            'green': 2,
            'yellow': 3,
            'blue': 4,
            'magenta': 5,
            'cyan': 6,
            'gray': 7,
            'darkgray': 8,
            'light-red': 9,
            'light-green': 10,
            'light-yellow': 11,
            'light-blue': 12,
            'light-magenta': 13,
            'light-cyan': 14,
            'white': 15,
        }

        try:
            return color_names_dict[p_input]
        except KeyError:
            return p_input

    def priority_color():
        priority_colors = config().priority_colors()

        try:
            return priority_colors[p_todo.priority()]
        except KeyError:
            return -1

    if p_type == CONTEXT_COLOR:
        result = config().context_color()
    elif p_type == PROJECT_COLOR:
        result = config().project_color()
    elif p_type == PRIORITY_COLOR:
        result = priority_color()
    elif p_type == METADATA_COLOR:
        result = config().metadata_color()
    elif p_type == LINK_COLOR:
        result = config().link_color()
    elif p_type == PROGRESS_COLOR:
        result = progress_color_code(p_todo, p_safe=(not p_256color))
    else:
        result = -1

    return normalize_color(result)

def get_ansi_color(p_type, p_todo, p_256color=False, p_background=None, p_decoration='normal'):
    """
    Returns ansi code for color based on xterm color id (0-255) and
    decoration, where decoration can be one of: normal, bold, faint,
    italic, or underline. When p_safe is True, resulting ansi code is
    constructed in most compatible way, but with support for only base 16
    colors.
    """

    def ansicode(p_int, p_background=False):
        ansi = 4 if p_background else 3

        if p_256color and p_int >= 0:
            return ';{}8;5;{}'.format(ansi, p_int)
        else:
            return ''

        if 0 <= p_int < 8:
            return ';{}{}'.format(ansi, p_int)
        elif 8 <= p_int < 16:
            return ';1;{}{}'.format(ansi, p_int - 8)
        else:
            return ''

    decoration_dict = {
        'normal': '0',
        'bold': '1',
        'faint': '2',
        'italic': '3',
        'underline': '4'
    }

    decoration = decoration_dict[p_decoration]
    foreground = get_color(p_type, p_todo, p_256color)
    background = get_color(p_background, p_todo, p_256color) if p_background else -1

    return '\033[{}{}{}m'.format(
        decoration,
        ansicode(foreground),
        ansicode(background, p_background=True)
    )

