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

from collections import OrderedDict
from six import u

from topydo.lib.Colors import NEUTRAL_COLOR, Colors
from topydo.lib.Config import config
from topydo.lib.ListFormat import (filler, humanize_date, humanize_dates,
                                   strip_placeholder_braces)
from topydo.lib.Utils import get_terminal_size


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
                                r'\1' + link_color + r'\2\3' + color,
                                p_todo_str)

            p_todo_str += NEUTRAL_COLOR
            
            # color by priority
            p_todo_str = color + p_todo_str

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


class PrettyPrinterFormatFilter(PrettyPrinterFilter):
    def __init__(self, p_todolist, p_format=None):
        super(PrettyPrinterFormatFilter, self).__init__()
        self.todolist = p_todolist
        self.format = p_format or config().list_format()

    def filter(self, p_todo_str, p_todo):
        placeholders = OrderedDict()
        # absolute creation date
        placeholders['c'] = lambda t: t.creation_date().isoformat() if t.creation_date() else ''

        # relative creation date
        placeholders['C'] = lambda t: humanize_date(t.creation_date()) if t.creation_date() else ''

        # absolute due date
        placeholders['d'] = lambda t: t.due_date().isoformat() if t.due_date() else ''

        # relative due date
        placeholders['D'] = lambda t: humanize_date(t.due_date()) if t.due_date() else ''

        # relative dates:  due, start
        placeholders['h'] = lambda t: humanize_dates(t.due_date(), t.start_date())

        # relative dates in form:  creation, due, start
        placeholders['H'] = lambda t: humanize_dates(t.due_date(), t.start_date(), t.creation_date())

        # todo ID
        placeholders['i'] = lambda t: str(self.todolist.number(t))

        # todo ID pre-filled with 1 or 2 spaces if its length is <3
        placeholders['I'] = lambda t: filler(str(self.todolist.number(t)), 3)

        # list of tags (spaces) without hidden ones and due: and t:
        placeholders['k'] = lambda t: ' '.join([u('{}:{}').format(tag, value)
                                    for tag, value in sorted(p_todo.tags()) if
                                    tag not in config().hidden_tags() + [config().tag_start(), config().tag_due()]])

        # list of all tags (spaces)
        placeholders['K'] = lambda t: ' '.join([u('{}:{}').format(tag, value)
                                    for tag, value in sorted(p_todo.tags())])

        # priority
        placeholders['p'] = lambda t: t.priority() if t.priority() else ''

        # text
        placeholders['s'] = lambda t: t.text()

        # absolute start date
        placeholders['t'] = lambda t: t.start_date().isoformat() if t.start_date() else ''

        # relative start date
        placeholders['T'] = lambda t: humanize_date(t.start_date()) if t.start_date() else ''

        # absolute completion date
        placeholders['x'] = lambda t: 'x ' + t.completion_date().isoformat() if t.is_completed() else ''

        # relative completion date
        placeholders['X'] = lambda t: 'x ' + humanize_date(t.completion_date()) if t.is_completed() else ''

        # literal %
        placeholders['%'] = lambda _: '%'

        # text (truncated if necessary)
        placeholders['S'] = lambda t: t.text()


        p_todo_str = self.format

        for placeholder, getter in placeholders.items():
            repl = getter(p_todo)
            pattern = (r'(?P<start>.*)'
                       r'%(?P<before>{{.+?}})?'
                       r'(?P<placeholder>{ph}|\[{ph}\])'
                       r'(?P<after>{{.+?}})?'
                       r'(?P<whitespace> *)'
                       r'(?P<end>.*)').format(ph=placeholder)
            match = re.match(pattern, p_todo_str)
            if match:
                if repl == '':
                    p_todo_str = re.sub(pattern, match.group('start') + match.group('end'), p_todo_str)
                else:

                    p_todo_str = re.sub(pattern, strip_placeholder_braces, p_todo_str)
                    p_todo_str = re.sub(r'%({ph}|\[{ph}\])'.format(ph=placeholder), repl, p_todo_str)
                    p_todo_str = p_todo_str.rstrip()

                    if placeholder == 'S':
                        p_todo_str = re.sub(' *\t *', '\t', p_todo_str)
                        line_width = get_terminal_size().columns
                        if len(p_todo_str) >= line_width:
                            text_lim = line_width - len(p_todo_str) - 4
                            p_todo_str = re.sub(re.escape(repl), repl[:text_lim] + '...', p_todo_str)

        # cut trailing space left when last placeholder in p_todo_str is empty and its predecessor is not
        return p_todo_str.rstrip()


class PrettyPrinterAlignFilter(PrettyPrinterFilter):
    """
    Final make-up for todo item line.
    Currently it only provides right alignment from place specified in
    list_format config-option (subsitutes tab-character with as many spaces as
    it is needed to fill the whole line).
    """

    def __init__(self):
        super(PrettyPrinterAlignFilter, self).__init__()

    def filter(self, p_todo_str, _):
        tab = re.search('.*\t', p_todo_str)

        if tab:
            line_width = get_terminal_size().columns
            to_fill = line_width - len(p_todo_str)

            if to_fill > 0:
                p_todo_str = re.sub('\t', ' '*to_fill, p_todo_str)
            else:
                p_todo_str = re.sub('\t', ' ', p_todo_str)

        return p_todo_str
