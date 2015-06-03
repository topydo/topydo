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

NEUTRAL_COLOR  = '\033[0m'

class Colors(object):
    def __init__(self):
        self.priority_colors = config().priority_colors()
        self.project_color = config().project_color()
        self.context_color = config().context_color()
        self.metadata_color = config().metadata_color()
        self.link_color = config().link_color()

    def _int_to_ansi(self, p_int, p_decorator='normal', p_safe=True):
        """
        Returns ansi code for color based on xterm color id (0-255) and
        decoration, where decoration can be one of: normal, bold, faint,
        italic, or underline. When p_safe is True, resulting ansi code is
        constructed in most compatible way, but with support for only base 16
        colors.
        """
        decoration_dict = {
                'normal': '0',
                'bold': '1',
                'faint': '2',
                'italic': '3',
                'underline': '4'
        }

        decoration = decoration_dict[p_decorator]

        try:
            if p_safe:
                if 8 > int(p_int) >=0:
                    return '\033[{};3{}m'.format(decoration, str(p_int))
                elif 16 > int(p_int):
                    p_int = int(p_int) - 8
                    return '\033[{};1;3{}m'.format(decoration, str(p_int))

            if 256 > int(p_int) >=0:
                return '\033[{};38;5;{}m'.format(decoration, str(p_int))
            else:
                return NEUTRAL_COLOR
        except ValueError:
            return None

    def _name_to_int(self, p_color_name):
        """ Returns xterm color id from color name. """
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
            return color_names_dict[p_color_name]
        except KeyError:
            return 404

    def _name_to_ansi(self, p_color_name, p_decorator):
        """ Returns ansi color code from color name. """
        number = self._name_to_int(p_color_name)

        return self._int_to_ansi(number, p_decorator)

    def _get_ansi(self, p_color, p_decorator):
        """ Returns ansi color code from color name or xterm color id. """
        if p_color == '':
            ansi = ''
        else:
            ansi = self._int_to_ansi(p_color, p_decorator, False)

            if not ansi:
                ansi = self._name_to_ansi(p_color, p_decorator)

        return ansi

    def get_priority_colors(self):
        pri_ansi_colors = dict()

        for pri in self.priority_colors:
            color = self._get_ansi(self.priority_colors[pri], 'normal')

            if color == '':
                color = NEUTRAL_COLOR

            pri_ansi_colors[pri] = color

        return pri_ansi_colors

    def get_project_color(self):
        return self._get_ansi(self.project_color, 'bold')

    def get_context_color(self):
        return self._get_ansi(self.context_color, 'bold')

    def get_metadata_color(self):
        return self._get_ansi(self.metadata_color, 'bold')

    def get_link_color(self):
        return self._get_ansi(self.link_color, 'underline')
