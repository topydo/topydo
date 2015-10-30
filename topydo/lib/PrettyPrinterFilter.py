# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2015 Bram Schoenmakers <me@bramschoenmakers.nl>
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

""" Provides filters used for pretty printing. """

import re

from six import u

from topydo.lib.Colors import NEUTRAL_COLOR, Colors
from topydo.lib.Config import config
from topydo.lib.ListFormat import filler, humanize_date


class PrettyPrinterFilter(object):
    """
    Base class for a pretty printer filter.

    Subclasses must re-implement the filter method.
    """

    def filter(self, p_todo_str, _):
        """
        Applies a filter to p_todo_str and returns a modified version of it.
        """
        raise NotImplementedError


class PrettyPrinterColorFilter(PrettyPrinterFilter):
    """
    Adds colors to the todo string by inserting ANSI codes.

    Should be passed as a filter in the filter list of pretty_print()
    """

    def filter(self, p_todo_str, p_todo):
        """ Applies the colors. """
        colorscheme = Colors()
        priority_colors = colorscheme.get_priority_colors()
        project_color = colorscheme.get_project_color()
        context_color = colorscheme.get_context_color()
        metadata_color = colorscheme.get_metadata_color()
        link_color = colorscheme.get_link_color()

        if config().colors():
            color = NEUTRAL_COLOR
            try:
                color = priority_colors[p_todo.priority()]
            except KeyError:
                pass

            # color by priority
            p_todo_str = color + p_todo_str

            # color projects / contexts
            p_todo_str = re.sub(
                r'\B(\+|@)(\S*\w)',
                lambda m: (
                    context_color if m.group(0)[0] == "@"
                    else project_color) + m.group(0) + color,
                p_todo_str)

            # tags
            p_todo_str = re.sub(r'\b\S+:[^/\s]\S*\b',
                                metadata_color + r'\g<0>' + color,
                                p_todo_str)

            # add link_color to any valid URL specified outside of the tag.
            p_todo_str = re.sub(r'(^|\s)(\w+:){1}(//\S+)',
                                ' ' + link_color + r'\2\3' + color,
                                p_todo_str)

            p_todo_str += NEUTRAL_COLOR

        return p_todo_str


class PrettyPrinterIndentFilter(PrettyPrinterFilter):
    """ Adds indentation to the todo item. """

    def __init__(self, p_indent=0):
        super(PrettyPrinterIndentFilter, self).__init__()
        self.indent = p_indent

    def filter(self, p_todo_str, _):
        """ Applies the indentation. """
        return ' ' * self.indent + p_todo_str


class PrettyPrinterNumbers(PrettyPrinterFilter):
    """ Prepends the todo's number, retrieved from the todolist. """

    def __init__(self, p_todolist):
        super(PrettyPrinterNumbers, self).__init__()
        self.todolist = p_todolist

    def filter(self, p_todo_str, p_todo):
        """ Prepends the number to the todo string. """
        return u("|{:>3}| {}").format(self.todolist.number(p_todo), p_todo_str)


class PrettyPrinterHideTagFilter(PrettyPrinterFilter):
    """ Removes all occurrences of the given tags from the text. """

    def __init__(self, p_hidden_tags):
        super(PrettyPrinterHideTagFilter, self).__init__()
        self.hidden_tags = p_hidden_tags

    def filter(self, p_todo_str, _):
        for hidden_tag in self.hidden_tags:
            # inspired from remove_tag in TodoBase
            p_todo_str = re.sub(r'\s?\b' + hidden_tag + r':\S+\b', '',
                                p_todo_str)

        return p_todo_str


class PrettyPrinterFormatFilter(PrettyPrinterFilter):
    def __init__(self, p_todolist, p_format=None):
        super(PrettyPrinterFormatFilter, self).__init__()
        self.todolist = p_todolist
        self.format = p_format or config().list_format()

    def filter(self, p_todo_str, p_todo):
        placeholders = {
            # absolute creation date
            'c': lambda t: t.creation_date().isoformat() if t.creation_date() else '',

            # relative creation date
            'C': lambda t: humanize_date(t.creation_date()) if t.creation_date() else '',

            # absolute due date
            'd': lambda t: t.due_date().isoformat() if t.due_date() else '',

            # relative due date
            'D': lambda t: humanize_date(t.due_date()) if t.due_date() else '',

            # todo ID
            'i': lambda t: str(self.todolist.number(t)),

            # todo ID pre-filled with 1 or 2 spaces if its length is <3
            'I': lambda t: filler(str(self.todolist.number(t)), 3),

            # list of tags (spaces)
            'K': lambda t: ' '.join(['{}:{}'.format(tag, value)
                                     for tag, value in sorted(p_todo.tags())]),

            # priority
            'p': lambda t: t.priority() if t.priority() else '',

            # text
            's': lambda t: t.text(),

            # absolute start date
            't': lambda t: t.start_date().isoformat() if t.start_date() else '',

            # relative start date
            'T': lambda t: humanize_date(t.start_date()) if t.start_date() else '',

            # literal %
            '%': lambda _: '%',
        }

        p_todo_str = self.format

        for placeholder, getter in placeholders.items():
            repl = getter(p_todo)
            pattern = (r'(?P<start>.*)'
                       r'%(?P<before>{{.+?}})?'
                       r'\[?(?P<placeholder>{})\]?'
                       r'(?P<after>{{.+?}})?'
                       r'(?P<whitespace>\s)*'
                       r'(?P<end>.*)').format(placeholder)
            if repl == '':
                p_todo_str = re.sub(pattern, match.group('start') + match.group('end'), p_todo_str)
            else:
                def strip_braces(p_matchobj):
                    try:
                        before = p_matchobj.group('before').strip('{}')
                    except AttributeError:
                        before = ''

                    placeholder = p_matchobj.group('placeholder')

                    try:
                        after = p_matchobj.group('after').strip('{}')
                    except AttributeError:
                        after = ''

                    whitespace = p_matchobj.group('whitespace') or ''
                    start = p_matchobj.group('start') or ''
                    end = p_matchobj.group('end') or ''

                    return start + before + '%' + placeholder + after + whitespace + end

                p_todo_str = re.sub(pattern, strip_braces, p_todo_str)
                p_todo_str = re.sub(r'%{}'.format(placeholder), repl, p_todo_str)

        return p_todo_str

