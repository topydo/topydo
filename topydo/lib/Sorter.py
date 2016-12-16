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

""" This module provides functionality to sort lists with todo items. """

from collections import OrderedDict, namedtuple
from itertools import groupby
import re
from datetime import date

from topydo.lib.Config import config
from topydo.lib.Importance import average_importance, importance
from topydo.lib.Utils import humanize_date


Field = namedtuple('Field', ['sort', 'group', 'label'])

FIELDS = {
    'completed': Field(
        # when a task has no completion date, push it to the end by assigning it
        # the maximum possible date.
        sort=(lambda t: t.completion_date() if t.completion_date() else date.max),
        group=(lambda t: humanize_date(t.completion_date()) if t.completion_date() else 'None'),
        label='Completed',
    ),
    'context': Field(
        sort=lambda t: sorted(c.lower() for c in t.contexts()) or ['zz'],
        group=lambda t: sorted(t.contexts()) or ['None'],
        label='Context'
    ),
    'created': Field(
        # when a task has no creation date, push it to the end by assigning it
        # the maximum possible date.
        sort=(lambda t: t.creation_date() if t.creation_date() else date.max),
        group=(lambda t: humanize_date(t.creation_date()) if t.creation_date() else 'None'),
        label='Created',
    ),
    'importance': Field(
        sort=importance,
        group=importance,
        label='Importance',
    ),
    'importance-avg': Field(
        sort= average_importance,
        group=lambda t: round(average_importance(t), 1),
        label='Importance (avg)',
    ),
    'length': Field(
        sort=lambda t: t.length(),
        group=lambda t: t.length(),
        label='Length',
    ),
    'priority': Field(
        sort=(lambda t: t.priority() or 'ZZ'),
        group=(lambda t: t.priority() or 'None'),
        label='Priority',
    ),
    'project': Field(
        sort=lambda t: sorted(p.lower() for p in t.projects()) or ['zz'],
        group=lambda t: sorted(t.projects()) or ['None'],
        label='Project',
    ),
    'text': Field(
        sort=lambda t: t.text().lower(),
        group=lambda t: t.text(),
        label='Text',
    ),
}

# map UI properties to properties in the FIELDS hash
FIELD_MAP = {
    'completed': 'completed',
    'completion': 'completed',
    'completion_date': 'completed',
    'done': 'completed',

    'context': 'context',
    'contexts': 'context',

    'created': 'created',
    'creation': 'created',
    'creation_date': 'created',

    'importance': 'importance',

    'importance-avg': 'importance-avg',
    'importance-average': 'importance-avg',

    'length': 'length',
    'len': 'length',

    'prio': 'priority',
    'priorities': 'priority',
    'priority': 'priority',

    'project': 'project',
    'projects': 'project',

    'text': 'text',
}

def _apply_sort_functions(p_todos, p_functions):
    sorted_todos = p_todos

    for function, order in reversed(p_functions):
        sorted_todos = sorted(sorted_todos, key=function,
                              reverse=(order == 'desc'))

    return sorted_todos


class Sorter(object):
    """
    This class sorts a todo list.

    Upon instantiation, a sort string should be passed to the class. Then, a
    list of todos must be passed to the sort method, which returns a copy of
    the list according to the sort string.

    A sort string is a comma separated line of field names, possibly prefixed
    with 'asc:' or 'desc' to denote the order in which that field must be
    sorted.

    Example:

        desc:importance,priority,asc:creation

    Meaning: a descending sort on the importance value, if equal, an ascending
    sort on priority and finally, if still equal an ascending sort on the
    creation field. Note that ascending is the default.

    The idea is that a list of sort functions is gathered, where the most
    specific search is done first. This relies on the fact that sorting is
    stable.
    """

    def __init__(self, p_sortstring="desc:priority", p_groupstring=""):
        self.groupfunctions = self._parse(p_groupstring, p_group=True) if p_groupstring else []
        self.pregroupfunctions = self._parse(p_groupstring, p_group=False) if p_groupstring else []
        self.sortfunctions = self._parse(p_sortstring, p_group=False)

    def sort(self, p_todos):
        """
        Sorts the list of todos given as a parameter, returns a new sorted
        list.

        The list is traversed in reverse order, such that the most specific
        sort operation is done first, relying on the stability of the sorted()
        function.
        """
        return _apply_sort_functions(p_todos, self.sortfunctions)

    def group(self, p_todos):
        """
        Groups the todos according to the given group string.
        """
        # preorder todos for the group sort
        p_todos = _apply_sort_functions(p_todos, self.pregroupfunctions)

        # initialize result with a single group
        result = OrderedDict([((), p_todos)])

        for (function, label), _ in self.groupfunctions:
            oldresult = result
            result = OrderedDict()
            for oldkey, oldgroup in oldresult.items():
                for key, _group in groupby(oldgroup, function):
                    newgroup = list(_group)

                    if not isinstance(key, list):
                        key = [key]

                    for subkey in key:
                        subkey = "{}: {}".format(label, subkey)
                        newkey = oldkey + (subkey,)

                        if newkey in result:
                            result[newkey] = result[newkey] + newgroup
                        else:
                            result[newkey] = newgroup

        # sort all groups
        for key, _group in result.items():
            result[key] = self.sort(_group)

        return result

    def _parse(self, p_string, p_group):
        """
        Parses a sort/group string and returns a list of functions and the
        desired order.
        """
        def get_field_function(p_field, p_group=False):
            """
            Turns a field, part of a sort/group string, into a lambda that
            takes a todo item and returns the field value.
            """
            compose = lambda i: i.sort if not p_group else (i.group, i.label)

            def group_value(p_todo):
                """
                Returns a value to assign the given todo to a group. Date tags
                are grouped according to the relative date (1 day, 1 month,
                ...)
                """
                result = 'No value'

                if p_todo.has_tag(p_field):
                    if p_field == config().tag_due():
                        result = humanize_date(p_todo.due_date())
                    elif p_field == config().tag_start():
                        result = humanize_date(p_todo.start_date())
                    else:
                        result = p_todo.tag_value(p_field)

                return result

            if p_field in FIELD_MAP:
                return compose(FIELDS[FIELD_MAP[p_field]])
            else:
                # treat it as a tag value
                return compose(Field(
                    sort=lambda t: '0' + t.tag_value(p_field) if t.has_tag(p_field) else '1',
                    group=group_value,
                    label=p_field,
                ))

        result = []
        fields = p_string.lower().split(',')

        for field in fields:
            parsed_field = re.match(
                r'(?P<order>(asc|desc)(ending)?:)?(?P<field>\S+)',
                field)

            if not parsed_field:
                continue

            order = parsed_field.group('order')
            order = 'desc' if order and order.startswith('desc') else 'asc'

            field = parsed_field.group('field')
            if field:
                function = get_field_function(field, p_group)

                # reverse order for priority: lower characters have higher
                # priority
                if field in FIELD_MAP and FIELD_MAP[field] == 'priority':
                    order = 'asc' if order == 'desc' else 'desc'

                result.append((function, order))

        return result

