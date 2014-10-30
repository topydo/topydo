# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 Bram Schoenmakers <me@bramschoenmakers.nl>
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

import Utils

def parse_line(p_string):
    """
    Parses a single line as can be encountered in a todo.txt file.
    First checks whether the standard elements are present, such as priority,
    creation date, completeness check and the completion date.

    Then the rest of the analyzed for any occurences of contexts, projects or
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
        'tags': []
    }

    date = r'\d{4}-\d{2}-\d{2}'
    completed_head = re.match(
        r'x ((?P<completionDate>' + date + ') )' +
        '((?P<creationDate>' + date + ') )?(?P<rest>.*)',
        p_string
    )

    normal_head = re.match(
        r'(\((?P<priority>[A-Z])\) )?' +
        '((?P<creationDate>' + date + ') )?(?P<rest>.*)',
        p_string
    )

    rest = p_string

    if completed_head:
        result['completed'] = True

        completion_date = completed_head.group('completionDate')
        result['completionDate'] = Utils.date_string_to_date(completion_date)

        creation_date = completed_head.group('creationDate')
        result['creationDate'] = Utils.date_string_to_date(creation_date)

        rest = completed_head.group('rest')
    elif normal_head:
        result['priority'] = normal_head.group('priority')

        creation_date = normal_head.group('creationDate')
        result['creationDate'] = Utils.date_string_to_date(creation_date)

        rest = normal_head.group('rest')

    for word in rest.split():
        project = re.match(r'\+(\S*\w)', word)
        if project:
            result['projects'].append(project.group(1))

        context = re.match(r'@(\S*\w)', word)
        if context:
            result['contexts'].append(context.group(1))

        tag = re.match('(?P<key>[^:]*):(?P<value>.*)', word)
        if tag:
            result['tags'].append((tag.group('key'), tag.group('value')))
            continue

        result['text'] += word + ' '

    # strip trailing space from resulting text
    result['text'] = result['text'][:-1]

    return result

