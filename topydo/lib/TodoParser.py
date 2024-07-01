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

"""
This module contains the parse function which parses a single line of a
todo.txt file.
"""

import re

from topydo.lib.Utils import date_string_to_date

_DATE_MATCH = r'\d{4}-\d{2}-\d{2}'

_COMPLETED_HEAD_MATCH = re.compile(
    r'x ((?P<completionDate>' + _DATE_MATCH + ') )?' + '((?P<creationDate>' +
    _DATE_MATCH + ') )?(?P<rest>.*)')

_NORMAL_HEAD_MATCH = re.compile(
    r'(\((?P<priority>[A-Z])\) )?' + '((?P<creationDate>' + _DATE_MATCH +
    ') )?(?P<rest>.*)')

_TAG_MATCH = re.compile(r'(?![0-9+]{1,2}:[0-9]{1,2}$)(?P<tag>[^:]+):(?P<value>.+)')
_PROJECT_MATCH = re.compile(r'\+(\S*\w)')
_CONTEXT_MATCH = re.compile(r'@(\S*\w)')


def parse_line(p_string):
    """
    Parses a single line as can be encountered in a todo.txt file.
    First checks whether the standard elements are present, such as priority,
    creation date, completeness check and the completion date.

    Then the rest of the analyzed for any occurrences of contexts, projects or
    tags.

    Returns an dictionary with the default values as shown below.
    """
    result = {
        'completed': False,
        'completionDate': None,
        'priority': None,
        'creationDate': None,
        'text': "",
        'projects': [],
        'contexts': [],
        'tags': {},
    }

    completed_head = _COMPLETED_HEAD_MATCH.match(p_string)
    normal_head = _NORMAL_HEAD_MATCH.match(p_string)

    rest = p_string

    if completed_head:
        result['completed'] = True

        completion_date = completed_head.group('completionDate')
        try:
            result['completionDate'] = date_string_to_date(completion_date)
        except ValueError:
            pass

        creation_date = completed_head.group('creationDate')

        try:
            result['creationDate'] = date_string_to_date(creation_date)
        except ValueError:
            pass

        rest = completed_head.group('rest')
    elif normal_head:
        result['priority'] = normal_head.group('priority')

        creation_date = normal_head.group('creationDate')

        try:
            result['creationDate'] = date_string_to_date(creation_date)
        except ValueError:
            pass

        rest = normal_head.group('rest')

    for word in rest.split():
        project = _PROJECT_MATCH.match(word)
        if project:
            result['projects'].append(project.group(1))

        context = _CONTEXT_MATCH.match(word)
        if context:
            result['contexts'].append(context.group(1))

        tag = _TAG_MATCH.match(word)
        if tag:
            tag_name = tag.group('tag')
            tag_value = tag.group('value')
            try:
                result['tags'][tag_name].append(tag_value)
            except KeyError:
                result['tags'][tag_name] = [tag_value]
        else:
            result['text'] += word + ' '

    # strip trailing space from resulting text
    result['text'] = result['text'][:-1]

    return result
