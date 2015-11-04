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
import textwrap

import arrow

from topydo.lib.Colors import NEUTRAL_COLOR, Colors
from topydo.lib.Config import config
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

    def __init__(self, p_indent=0, p_max_lines=None):
        super(PrettyPrinterIndentFilter, self).__init__()
        self.indent = p_indent
        self.max_lines = p_max_lines

    def filter(self, p_todo_str, _):
        """ Applies the indentation. """
        try:
            return(textwrap.fill(p_todo_str,
                                 initial_indent=' '*self.indent,
                                 subsequent_indent=' '*(10 + self.indent),
                                 # 10 spaces added to hanging indented lines to
                                 #  push the front of the line past the
                                 #  identification and priority in the line above
                                 width=get_terminal_size().columns - 1,
                                 # terminal width, less one (so we don't wrap
                                 #  to the next line)
                                 break_long_words=True,     # will break long URL's
                                 max_lines=self.max_lines,  # requires Python 3.4
                                 placeholder=' ...'))       # requires Python 3.4
        except TypeError:
            output = textwrap.fill(p_todo_str,
                                   initial_indent=' '*self.indent,
                                   subsequent_indent=' '*(10 + self.indent),
                                   width=get_terminal_size().columns - 1,
                                   break_long_words=True)  # will break long URL's
            if self.max_lines:
                return('\n'.join(output.splitlines()[:self.max_lines]))
                #  for use with the 'top' command, but it doesn't give the
                #  ellipse (...) at the end of the line if it continues on
            else:
                return(output)



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


class PrettyPrinterBasicPriorityFilter(PrettyPrinterFilter):

    """ Strips the bracked from the priority of the todo item. Add a (blank)
        space if not priority is specified (to maintain printing alignment)
    """

    def __init__(self, p_replacement=" "):
        super(PrettyPrinterBasicPriorityFilter, self).__init__()
        self.p_replacement = p_replacement

    def filter(self, p_todo_str, _):
        """ Find the priority """
        matches = re.search('^(?P<id>\| *\w+\| )?(\((?P<pri>[A-Z])\) )?', p_todo_str)
        # we are looking for the id string and priority at the beginning of the
        # line, in the form of:
        #   | 48| (V) ...
        #   |h2j| (C) ...

        # there will always be a match (so don't check for it), even if it's
        # 'nothing', because both match groups are optional
        if matches.group('id'):
            """ If we have an id """
            if matches.group('pri'):
                """ If we have a priority """
                return(matches.group('id') + matches.group('pri') + ' ' + p_todo_str[matches.span()[1]:])
            else:
                return(matches.group('id') + self.p_replacement + ' ' + p_todo_str[matches.span()[1]:])
        else:
            if matches.group('pri'):
                """ If we have a priority """
                return(matches.group('pri') + ' ' + p_todo_str[matches.span()[1]:])
            else:
                """ No match found """
                return(self.p_replacement + ' ' + p_todo_str)


class PrettyPrinterHumanDatesFilter(PrettyPrinterFilter):

    """ Turns dates to human readable versions. """

    def __init__(self):
        super(PrettyPrinterHumanDatesFilter, self).__init__()

    def date_from_match(self, matchgroup):
        """
        Takes a match group and then returns a date.

        Assumes the matchgroup has matches named 'year', 'month', and 'day'.

        The returned arrow object has hours, minutes, and seconds set to now.
        """
        linedate = arrow.now()  # set the time to 'now' so the comparisions work better
        linedate = linedate.replace(year=int(matchgroup.group('year')),
                                    month=int(matchgroup.group('month')),
                                    day=int(matchgroup.group('day')))
        return(linedate)

    def filter(self, p_todo_str, _):

        adding_dates = False

        """ First, the date added
            This, per the spec, will be at the front of the line,
            after the priority
        """
        line2 = p_todo_str
        pattern2 = re.compile('^(?P<line_start>(\| *\w+\| )?(\(?[A-Z ]\)? )?)(?P<is_date>(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2}) )')
        matches2 = pattern2.match(line2)
        if matches2:
            add_delta = self.date_from_match(matches2).humanize()
            line3 = matches2.group('line_start') + pattern2.sub('', line2)
            adding_dates = True
        else:
            add_delta = ''
            line3 = line2

        """ Due dates """
        pattern3 = re.compile('(?P<is_date> ' + config().tag_due() + ':(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2}) ?)')
        matches3 = pattern3.search(line3)
        if matches3:
            due_delta = 'due ' + self.date_from_match(matches3).humanize()

            if adding_dates is True:
                due_delta = ', ' + due_delta
            adding_dates = True
            line4 = pattern3.sub(' ', line3)
        else:
            due_delta = ''
            line4 = line3

        """ Threshold dates """
        pattern4 = re.compile('(?P<is_date> ' + config().tag_start() + ':(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2}) ?)')
        matches4 = pattern4.search(line3)
        if matches4:
            threshold_date = self.date_from_match(matches4)
            if threshold_date <= arrow.now():
                threshold_delta = 'threshold of ' + threshold_date.humanize()
            else:
                threshold_delta = 'threshold in ' + threshold_date.humanize(only_distance=True)

            if adding_dates is True:
                threshold_delta = ', ' + threshold_delta
            adding_dates = True
            line5 = pattern4.sub(' ', line4)
        else:
            threshold_delta = ''
            line5 = line4

        if adding_dates is True:
            line6 = line5.rstrip() + ' (' + add_delta + due_delta + \
                        threshold_delta + ')'
        else:
            line6 = line5

        return line6
