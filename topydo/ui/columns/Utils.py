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

class PaletteItem:
    PROJECT = 'project'
    PROJECT_FOCUS = 'project_focus'
    CONTEXT = 'context'
    CONTEXT_FOCUS = 'context_focus'
    METADATA = 'metadata'
    METADATA_FOCUS = 'metadata_focus'
    LINK = 'link'
    LINK_FOCUS = 'link_focus'

    DEFAULT = 'default'
    DEFAULT_FOCUS = 'default_focus'
    MARKED = 'marked'


def to_urwid_color(p_color):
    """
    Given a Color object, transform it to a color that urwid understands.
    """
    if not p_color.is_valid():
        return 'black'
    elif p_color.is_neutral():
        return 'default'
    else:
        return 'h{}'.format(p_color.color)
