# Topydo - A todo.txt client written in Python.
# Copyright (C) 2015 Bram Schoenmakers <bram@topydo.org>
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

from topydo.lib.Color import AbstractColor
from topydo.lib.Todo import Todo
from topydo.lib.TopydoString import TopydoString
from topydo.ui.columns.Utils import PaletteItem

PALETTE_LOOKUP = {
    # omitting AbstractColor.NEUTRAL on purpose, so a text without any
    # attribute will be added to the markup
    AbstractColor.PROJECT: PaletteItem.PROJECT,
    AbstractColor.CONTEXT: PaletteItem.CONTEXT,
    AbstractColor.META: PaletteItem.METADATA,
    AbstractColor.LINK: PaletteItem.LINK,
}

def topydostringToMarkup(p_string):
    markup = []

    color_positions = sorted(p_string.colors.items())

    # in case no color positions are available, at least set something at the
    # start position
    if not color_positions:
        color_positions = [(0, None)]

    for i, (start_pos, color) in enumerate(color_positions):
        # color starts at indicated position
        start = start_pos

        # color ends at next color indication. if missing, run until the end of
        # the string
        try:
            end = color_positions[i+1][0]
        except IndexError:
            end = len(str(p_string))

        text = str(p_string)[start:end]

        if color in PALETTE_LOOKUP:
            markup.append((PALETTE_LOOKUP[color], text))
        else:
            # a plain text without any attribute set (including
            # AbstractColor.NEUTRAL)
            markup.append(text)

    color_at_start = color_positions and color_positions[0][0] == 0

    # priority color should appear at the start if present, build a nesting
    # markup
    if color_at_start and isinstance(p_string.metadata, Todo):
        priority = p_string.metadata.priority()

        if priority:
            markup = ('pri_' + priority, markup)

    return markup

class ConsoleWidget(urwid.LineBox):
    def __init__(self, p_text=""):
        urwid.register_signal(ConsoleWidget, ['close'])

        self.width = 0
        self.pile = urwid.Pile([])

        super().__init__(self.pile)

    def keypress(self, p_size, p_key):
        if p_key == 'enter' or p_key == 'q' or p_key == 'esc':
            urwid.emit_signal(self, 'close')

        # don't return the key, 'enter', 'escape', 'q' or ':' are your only
        # escape. ':' will reenter to the cmdline.
        elif p_key == ':':
            urwid.emit_signal(self, 'close', True)

    def selectable(self):
        return True

    def print_text(self, p_text):
        if isinstance(p_text, list):
            for text in p_text:
                self.print_text(text)

            return
        elif isinstance(p_text, TopydoString):
            text = urwid.Text(topydostringToMarkup(p_text))
        else:
            text = urwid.Text(p_text)

        self.pile.contents.append((text, ('pack', None)))

    def clear(self):
        self.pile.contents = []
