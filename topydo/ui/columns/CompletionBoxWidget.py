# Topydo - A todo.txt client written in Python.
# Copyright (C) 2017 Bram Schoenmakers <bram@topydo.org>
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

from topydo.ui.columns.Utils import PaletteItem


class CompletionBoxWidget(urwid.ListBox):
    def __init__(self):
        self.items = urwid.SimpleFocusListWalker([])
        self.min_width = 0

        super().__init__(self.items)

    def __len__(self):
        return len(self.items)

    @property
    def height(self):
        """ Returns height of the widget, with maximum set to 4 lines. """
        return min(len(self), 4)

    @property
    def margin(self):
        """
        Returns margin for rendering the widget always glued to the cursor.
        """
        return len(self.items[0].original_widget.text)

    def add_completions(self, p_completions):
        """
        Creates proper urwid.Text widgets for all completion candidates from
        p_completions list, and populates them into the items attribute.
        """
        palette = PaletteItem.MARKED
        for completion in p_completions:
            width = len(completion)
            if width > self.min_width:
                self.min_width = width
            w = urwid.Text(completion)
            self.items.append(urwid.AttrMap(w, None, focus_map=palette))
            self.items.set_focus(0)

    def clear(self):
        self.items.clear()
        self.min_width = 0

    def set_focus(self, p_position, p_coming_from=None):
        self.focus.set_attr_map({PaletteItem.MARKED: None})
        super().set_focus(p_position, p_coming_from)
        self.focus.set_attr_map({None: PaletteItem.MARKED})
