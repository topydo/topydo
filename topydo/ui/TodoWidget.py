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

from topydo.lib.Config import config
from topydo.lib.ListFormat import ListFormatParser
from topydo.ui.Colors import COLOR_MAP

import urwid

# pass a None todo list, since we won't use %i or %I here
PRIO_FORMATTER = ListFormatParser(None, "%{(}p{)}")
TEXT_FORMATTER = ListFormatParser(None, "%s %k\n%h")

def _markup(p_todo, p_focus):
    """
    Returns an attribute spec for the colors that correspond to the given todo
    item.
    """

    priority_colors = config().priority_colors()

    try:
        # retrieve the assigned value in the config file
        fg_color = priority_colors[p_todo.priority()]

        # convert to a color that urwid understands
        fg_color = COLOR_MAP[fg_color]
    except KeyError:
        fg_color = 'black' if p_focus else 'default'

    bg_color = 'light gray' if p_focus else 'default'

    return urwid.AttrSpec(fg_color, bg_color, 256)

class TodoWidget(urwid.WidgetWrap):
    def __init__(self, p_todo, p_number):
        # clients use this to associate this widget with the given todo item
        self.todo = p_todo

        todo_text = TEXT_FORMATTER.parse(p_todo)
        priority_text = PRIO_FORMATTER.parse(p_todo)

        id_widget = urwid.Text(str(p_number), align='right')
        priority_widget = urwid.Text(priority_text)
        self.text_widget = urwid.Text(todo_text)

        self.columns = urwid.Columns(
            [
                (4, id_widget),
                (3, priority_widget),
                ('weight', 1, self.text_widget),
            ],
            dividechars=1
        )

        self.widget = urwid.AttrMap(
            self.columns,
            _markup(p_todo, False), # no focus
            _markup(p_todo, True) # focus
        )

        super().__init__(self.widget)

    def keypress(self, p_size, p_key):
        """
        Override keypress to prevent the wrapped Columns widget to
        receive any key.
        """
        return p_key

    def selectable(self):
        # make sure that ListBox will highlight this widget
        return True
