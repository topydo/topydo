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

class CommandLineWidget(urwid.Edit):
    def __init__(self, *args, **kwargs):
        super(CommandLineWidget, self).__init__(*args, **kwargs)
        urwid.register_signal(CommandLineWidget, ['blur', 'execute_command'])

    def clear(self):
        self.set_edit_text("")

    def _blur(self):
        self.clear()
        urwid.emit_signal(self, 'blur')

    def _emit_command(self):
        urwid.emit_signal(self, 'execute_command', self.edit_text)
        self.clear()

    def keypress(self, p_size, p_key):
        dispatch = {
            'enter': self._emit_command,
            'esc': self._blur,
        }

        try:
            dispatch[p_key]()
        except KeyError:
            super(CommandLineWidget, self).keypress(p_size, p_key)
