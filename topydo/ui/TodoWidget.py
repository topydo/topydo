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

import urwid

class TodoWidget(urwid.WidgetWrap):
    def __init__(self, p_todo):
        priority = p_todo.priority()
        priority_text = u""
        todo_text = p_todo.source()

        if priority:
            priority_text = "({})".format(priority)

            # strip the first characters off
            todo_text = todo_text[4:]

        priority_widget = urwid.Text(priority_text)
        text_widget = urwid.Text(todo_text)

        columns = urwid.Columns(
            [
                (3, priority_widget),
                ('weight', 1, text_widget),
            ],
            dividechars=1
        )

        super(TodoWidget, self).__init__(columns)
