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
from six import u

class ConsoleWidget(urwid.LineBox):
    def __init__(self, p_text=u("")):
        urwid.register_signal(ConsoleWidget, ['close'])

        self.text = urwid.Text(p_text)
        super(ConsoleWidget, self).__init__(self.text)

    def keypress(self, p_size, p_key):
        if p_key == 'enter' or p_key == 'q' or p_key == 'esc':
            urwid.emit_signal(self, 'close')

        # don't return the key, 'enter', 'escape' or 'q' are your only escape.

    def selectable(self):
        return True

    def print_text(self, p_text):
        self.text.set_text(self.text.text + p_text)

    def clear(self):
        self.text.set_text(u(""))
