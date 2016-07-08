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

import re
import urwid

from topydo.lib.Config import config
from topydo.lib.ListFormat import ListFormatParser
from topydo.lib.ProgressColor import progress_color
from topydo.ui.columns.Utils import PaletteItem, to_urwid_color

# pass a None todo list, since we won't use %i or %I here
PRIO_FORMATTER = ListFormatParser(None, "%{(}p{)}")
TEXT_FORMATTER = ListFormatParser(None, "%s %k\n%h")

PRJ_CON_PATTERN = r'\B(?:\+|@)(?:\S*\w)'
TAG_PATTERN = r'\b\S+:[^/\s]\S*\b'
URL_PATTERN = r'(?:^|\s)(?:\w+:){1}(?://\S+)'


def _markup(p_todo, p_focus):
    """
    Returns an attribute spec for the colors that correspond to the given todo
    item.
    """
    pri = p_todo.priority()
    pri = 'pri_' + pri if pri else PaletteItem.DEFAULT

    if not p_focus:
        attr_dict = {None: pri}
    else:
        # use '_focus' palette entries instead of standard ones
        attr_dict = {None: pri + '_focus'}
        attr_dict[PaletteItem.PROJECT] = PaletteItem.PROJECT_FOCUS
        attr_dict[PaletteItem.CONTEXT] = PaletteItem.CONTEXT_FOCUS
        attr_dict[PaletteItem.METADATA] = PaletteItem.METADATA_FOCUS
        attr_dict[PaletteItem.LINK] = PaletteItem.LINK_FOCUS

    return attr_dict


class TodoWidget(urwid.WidgetWrap):
    def __init__(self, p_todo, p_number):
        # clients use this to associate this widget with the given todo item
        self.todo = p_todo

        todo_text = TEXT_FORMATTER.parse(p_todo)
        priority_text = PRIO_FORMATTER.parse(p_todo)

        # split todo_text at each occurrence of tag/project/context/url
        txt_pattern = r'|'.join([PRJ_CON_PATTERN, TAG_PATTERN, URL_PATTERN])
        txt_pattern = r'(' + txt_pattern + r')'
        txt_splitted = re.split(txt_pattern, todo_text)
        txt_markup = []

        # Examine each substring and apply relevant palette entry if needed
        for substring in txt_splitted:
            # re.split can generate empty strings when capturing group is used
            if not substring:
                continue
            if re.match(TAG_PATTERN, substring):
                txt_markup.append((PaletteItem.METADATA, substring))
            elif re.match(URL_PATTERN, substring):
                txt_markup.append((PaletteItem.LINK, substring))
            elif re.match(PRJ_CON_PATTERN, substring):
                if substring.startswith('+'):
                    txt_markup.append((PaletteItem.PROJECT, substring))
                else:
                    txt_markup.append((PaletteItem.CONTEXT, substring))
            else:
                txt_markup.append(substring)

        id_widget = urwid.Text(str(p_number), align='right')
        priority_widget = urwid.Text(priority_text)
        self.text_widget = urwid.Text(txt_markup)

        progress = to_urwid_color(progress_color(p_todo)) if config().colors() else PaletteItem.DEFAULT
        progress_bar = urwid.AttrMap(
                urwid.SolidFill(' '),
                urwid.AttrSpec(PaletteItem.DEFAULT, progress, 256),
                urwid.AttrSpec(PaletteItem.DEFAULT, progress, 256),
        )

        self.columns = urwid.Columns(
            [
                (1, progress_bar),
                (4, id_widget),
                (3, priority_widget),
                ('weight', 1, self.text_widget),
            ],
            dividechars=1,
            box_columns=[0] # the progress bar adapts its height to the rest
        )

        self.widget = urwid.AttrMap(
            self.columns,
            _markup(p_todo, p_focus=False),
            _markup(p_todo, p_focus=True)
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

    def mark(self):
        attr_map = {
            None:                 PaletteItem.MARKED,
            PaletteItem.LINK:     PaletteItem.MARKED,
            PaletteItem.CONTEXT:  PaletteItem.MARKED,
            PaletteItem.PROJECT:  PaletteItem.MARKED,
            PaletteItem.METADATA: PaletteItem.MARKED,
        }
        self.widget.set_attr_map(attr_map)

    def unmark(self):
        self.widget.set_attr_map(_markup(self.todo, False))
