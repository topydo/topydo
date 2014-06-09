"""
This module contains the parse function which parses a single line of a
todo.txt file.
"""

import re

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
        result['completionDate'] = completed_head.group('completionDate')
        result['creationDate'] = completed_head.group('creationDate')
        rest = completed_head.group('rest')
    elif normal_head:
        result['priority'] = normal_head.group('priority')
        result['creationDate'] = normal_head.group('creationDate')
        rest = normal_head.group('rest')

    for word in rest.split():
        project = re.match(r'\+(.*)', word)
        if project:
            result['projects'].append(project.group(1))

        context = re.match('@(.*)', word)
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

