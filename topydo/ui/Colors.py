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

""" Provides color support suitable for urwid. """

COLOR_MAP = {
    'black': 'black',
    'red': 'dark red',
    'green': 'dark green',
    'yellow': 'brown',
    'blue': 'dark blue',
    'magenta': 'dark magenta',
    'cyan': 'dark cyan',
    'gray': 'light gray',
    'darkgray': 'dark gray',
    'light-red': 'light red',
    'light-green': 'light green',
    'light-yellow': 'yellow',
    'light-blue': 'light blue',
    'light-magenta': 'light magenta',
    'light-cyan': 'light cyan',
    'white': 'white',
}

def color_map256():
    color_map = dict()
    for i in range(256):
        color_map[str(i)] = 'h' + str(i)

    color_map.update(COLOR_MAP)

    return color_map
