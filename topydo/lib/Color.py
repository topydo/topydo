# Topydo - A todo.txt client written in Python.
# Copyright (C) 2016 Bram Schoenmakers <bram@topydo.org>
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

""" This module provides a class that represents a color. """


class AbstractColor:
    NEUTRAL = 0
    PROJECT = 1
    CONTEXT = 2
    META = 3
    LINK = 4


class Color:
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

    def __init__(self, p_value=None):
        """ p_value is user input, be it a word color or an xterm code """
        self._value = None
        self.color = p_value

    @property
    def color(self):
        return self._value

    @color.setter
    def color(self, p_value):
        try:
            if not p_value:
                self._value = None
            elif p_value in Color.color_names_dict:
                self._value = Color.color_names_dict[p_value]
            else:
                self._value = int(p_value)

                # values not in the 256 range are normalized to be neutral
                if not 0 <= self._value < 256:
                    raise ValueError
        except ValueError:
            # garbage was entered, make it neutral, so at least some
            # highlighting may take place
            self._value = -1

    def is_neutral(self):
        """
        A neutral color is the default color on the shell, setting this color
        will reset all other attributes (background, foreground, decoration).
        """
        return self._value == -1

    def is_valid(self):
        """
        Whether the color is a valid color.
        """
        return self._value is not None

    def as_ansi(self, p_decoration='normal', p_background=False):
        if not self.is_valid():
            return ''
        elif self.is_neutral():
            return '\033[0m'

        is_high_color = 8 <= self._value < 16
        is_256 = 16 <= self._value < 255

        decoration_dict = {
            'normal': '0',
            'bold': '1',
            'faint': '2',
            'italic': '3',
            'underline': '4',
        }
        decoration = decoration_dict[p_decoration]

        base = 40 if p_background else 30
        if is_high_color:
            color = '1;{}'.format(base + self._value - 8)
        elif is_256:
            color = '{};5;{}'.format(base + 8, self._value)
        else:
            # it's a low color
            color = str(base + self._value)

        return '\033[{};{}m'.format(
            decoration,
            color
        )

