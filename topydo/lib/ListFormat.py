# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2015 Bram Schoenmakers <bram@topydo.org>
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

""" Utilities for formatting output with "list_format" option."""

import arrow
import re

from topydo.lib.Config import config
from topydo.lib.ProgressColor import progress_color
from topydo.lib.Utils import get_terminal_size, escape_ansi, humanize_date

MAIN_PATTERN = (r'^({{(?P<before>.+?)}})?'
                r'(?P<placeholder>{ph}|\[{ph}\])'
                r'({{(?P<after>.+?)}})?'
                r'(?P<whitespace> *)')

def _columns():
    """ Returns the number of columns of the terminal. """
    return get_terminal_size().columns

def _filler(p_str, p_len):
    """
    Returns p_str preceded by additional spaces if p_str is shorter than p_len.
    """
    to_fill = p_len - len(p_str)
    return to_fill*' ' + p_str

def humanize_dates(p_due=None, p_start=None, p_creation=None):
    """
    Returns string with humanized versions of p_due, p_start and p_creation.
    Examples:
    - all dates: "16 days ago, due in a month, started 2 days ago"
    - p_due and p_start: "due in a month, started 2 days ago"
    - p_creation and p_due: "16 days ago, due in a month"
    """
    dates_list = []
    if p_creation:
        dates_list.append(humanize_date(p_creation))
    if p_due:
        dates_list.append('due ' + humanize_date(p_due))
    if p_start:
        now = arrow.now().date()
        dates_list.append('{} {}'.format(
            'started' if p_start <= now else 'starts',
            humanize_date(p_start)
        ))

    return ', '.join(dates_list)

def _strip_placeholder_braces(p_matchobj):
    """
    Returns string with conditional braces around placeholder stripped and
    percent sign glued into placeholder character.

    Returned string is composed from 'start', 'before', 'placeholder', 'after',
    'whitespace', and 'end' match-groups of p_matchobj. Conditional braces are
    stripped from 'before' and 'after' groups. 'whitespace', 'start', and 'end'
    groups are preserved without any change.

    Using this function as an 'repl' argument in re.sub it is possible to turn:
        %{(}B{)}
    into:
        (%B)
    """
    before = p_matchobj.group('before') or ''
    placeholder = p_matchobj.group('placeholder')
    after = p_matchobj.group('after') or ''
    whitespace = p_matchobj.group('whitespace') or ''

    return before + '%' + placeholder + after + whitespace

def _unescape_percent_sign(p_str):
    """ Strips backslashes from escaped percent signs in p_str. """
    unescaped_str = re.sub(r'\\%', '%', p_str)

    return unescaped_str

def _remove_redundant_spaces(p_str):
    """ Removes spaces surrunding <TAB> character (\t) from p_str. """
    clean_str = re.sub(' *\t *', '\t', p_str)

    return clean_str

def _truncate(p_str, p_repl):
    """
    Returns p_str with truncated and ended with '...' version of p_repl.

    Place of the truncation is calculated depending on p_max_width.
    """
    # 4 is for '...' and an extra space at the end
    text_lim = _columns() - len(escape_ansi(p_str)) - 4
    truncated_str = re.sub(re.escape(p_repl), p_repl[:text_lim] + '...', p_str)

    return truncated_str

def _right_align(p_str):
    """
    Returns p_str with content after <TAB> character aligned right.

    Right alignment is done using proper number of spaces calculated from
    'line_width' attribute.
    """
    to_fill = _columns() - len(escape_ansi(p_str))

    if to_fill > 0:
        p_str = re.sub('\t', ' '*to_fill, p_str)
    else:
        p_str = re.sub('\t', ' ', p_str)

    return p_str

def color_block(p_todo):
    return '{} {}'.format(
        progress_color(p_todo).as_ansi(p_background=True),
        config().priority_color(p_todo.priority()).as_ansi(),
    )

class ListFormatParser(object):
    """ Parser of format string. """
    def __init__(self, p_todolist, p_format=None):
        self.format_string = re.sub(r'\\t', '\t', p_format or config().list_format())
        self.todolist = p_todolist
        self.one_line = False
        self.placeholders = {
            # absolute creation date
            'c': lambda t: t.creation_date().isoformat() if t.creation_date() else '',

            # relative creation date
            'C': lambda t: humanize_date(t.creation_date()) if t.creation_date() else '',

            # absolute due date
            'd': lambda t: t.due_date().isoformat() if t.due_date() else '',

            # relative due date
            'D': lambda t: humanize_date(t.due_date()) if t.due_date() else '',

            # relative dates:  due, start
            'h': lambda t: humanize_dates(t.due_date(), t.start_date()),

            # relative dates in form:  creation, due, start
            'H': lambda t: humanize_dates(t.due_date(), t.start_date(), t.creation_date()),

            # todo ID
            'i': lambda t: str(self.todolist.number(t)),

            # todo ID pre-filled with 1 or 2 spaces if its length is <3
            'I': lambda t: _filler(str(self.todolist.number(t)), 3),


            # list of tags (spaces) without hidden ones and due: and t:
            'k': lambda t: ' '.join([u'{}:{}'.format(tag, value)
                                     for tag, value in sorted(t.tags()) if
                                     tag not in config().hidden_tags() +
                                     [config().tag_start(), config().tag_due()]]),

            # list of all tags (spaces)
            'K': lambda t: ' '.join([u'{}:{}'.format(tag, value)
                                     for tag, value in sorted(t.tags())]),

            # priority
            'p': lambda t: t.priority() if t.priority() else '',

            # priority (or placeholder space)
            'P': lambda t: t.priority() if t.priority() else ' ',

            # raw text
            'r': lambda t: t.source(),

            # text
            's': lambda t: t.text(),

            # text (truncated if necessary)
            'S': lambda t: t.text(),

            # absolute start date
            't': lambda t: t.start_date().isoformat() if t.start_date() else '',

            # relative start date
            'T': lambda t: humanize_date(t.start_date()) if t.start_date() else '',

            # absolute completion date
            'x': lambda t: 'x ' + t.completion_date().isoformat() if t.is_completed() else '',

            # relative completion date
            'X': lambda t: 'x ' + humanize_date(t.completion_date()) if t.is_completed() else '',

            'z': lambda t: color_block(t) if config().colors() else ' ',
        }
        self.format_list = self._preprocess_format()

    def _preprocess_format(self):
        """
        Preprocess the format_string attribute.

        Splits the format string on each placeholder and returns a list of
        tuples containing substring, placeholder name, and function
        retrieving content for placeholder (getter).

        Relevant placeholder functions (getters) are taken from
        'placeholders' attribute which is a dict. If no matching placeholder
        is found in 'placeholders' getter is set to None. Getter and
        placeholder are also always set to None in first element of the
        returned list, because it never contain a real placeholder (read
        re.split documentation for further information).
        """
        format_split = re.split(r'(?<!\\)%', self.format_string)
        preprocessed_format = []

        for idx, substr in enumerate(format_split):
            if idx == 0:
                getter = None
                placeholder = None
            else:
                pattern = MAIN_PATTERN.format(ph=r'\S')
                try:
                    placeholder = re.match(pattern, substr).group('placeholder').strip('[]')
                except AttributeError:
                    placeholder = None

                if placeholder == 'S':
                    self.one_line = True

                try:
                    getter = self.placeholders[placeholder]
                except KeyError:
                    getter = None
                    substr = re.sub(pattern, '', substr)

            format_elem = (substr, placeholder, getter)
            preprocessed_format.append(format_elem)

        return preprocessed_format

    def parse(self, p_todo):
        """
        Returns fully parsed string from 'format_string' attribute with all
        placeholders properly substituted by content obtained from p_todo.

        It uses preprocessed form of 'format_string' (result of
        ListFormatParser._preprocess_format) stored in 'format_list'
        attribute.
        """
        parsed_list = []
        repl_trunc = None

        for substr, placeholder, getter in self.format_list:
            repl = getter(p_todo) if getter else ''
            pattern = MAIN_PATTERN.format(ph=placeholder)

            if placeholder == 'S':
                repl_trunc = repl

            if repl == '':
                substr = re.sub(pattern, '', substr)
            else:
                substr = re.sub(pattern, _strip_placeholder_braces, substr)
                substr = re.sub(r'(?<!\\)%({ph}|\[{ph}\])'.format(ph=placeholder), repl, substr)

            parsed_list.append(substr)

        parsed_str = _unescape_percent_sign(''.join(parsed_list))
        parsed_str = _remove_redundant_spaces(parsed_str)

        if self.one_line and len(escape_ansi(parsed_str)) >= _columns():
            parsed_str = _truncate(parsed_str, repl_trunc)

        if re.search('.*\t', parsed_str):
            parsed_str = _right_align(parsed_str)

        return parsed_str.rstrip()
