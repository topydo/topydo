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

from six import text_type, u

from topydo.lib.Config import config
from topydo.ui.Colors import color_map256

import urwid

class TodoWidget(urwid.WidgetWrap):
    def __init__(self, p_todo, p_number):
        self.todo = p_todo

        priority = self.todo.priority()
        priority_text = u("")
        todo_text = self.todo.source()

        if priority:
            priority_text = "({})".format(priority)

            # strip the first characters off
            todo_text = todo_text[4:]

        id_widget = urwid.Text(text_type(p_number), align='right')
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
            self._markup(p_todo, False), # no focus
            self._markup(p_todo, True) # focus
        )

        super(TodoWidget, self).__init__(self.widget)

    def _markup(self, p_todo, p_focus):
        priority_colors = config().priority_colors()
        color_map = color_map256()

        try:
            # retrieve the assigned value in the config file
            fg_color = priority_colors[p_todo.priority()]

            # convert to a color that urwid understands
            fg_color = color_map[fg_color]
        except KeyError:
            fg_color = 'black' if p_focus else 'default'

        bg_color = 'light gray' if p_focus else 'default'

        return urwid.AttrSpec(fg_color, bg_color, 256)

    def keypress(self, p_size, p_key):
        """
        Override keypress to prevent the wrapped Columns widget to
        receive any key.
        """
        return p_key

    def selectable(self):
        # make sure that ListBox will highlight this widget
        return True
