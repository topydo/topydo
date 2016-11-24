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

from collections import OrderedDict
from itertools import groupby
import re
from datetime import date

from topydo.lib.Importance import average_importance, importance


def is_priority_field(p_field):
    """ Returns True when the field name denotes the priority. """
    return p_field.startswith('prio')


def get_field_function(p_field):
    """
    Given a property (string) of a todo, return a function that attempts to
    access that property. If the property could not be located, return the
    identity function.
    """
    # default result
    result = lambda a: a

    if is_priority_field(p_field):
        # assign dummy priority when a todo has no priority
        result = lambda a: a.priority() or 'ZZ'
    elif p_field == 'context' or p_field == 'contexts':
        result = lambda a: sorted([c.lower() for c in a.contexts()])
    elif p_field == 'creationdate' or p_field == 'creation':
        # when a task has no creation date, push it to the end by assigning it
        # the maximum possible date.
        result = (lambda a: a.creation_date() if a.creation_date()
                  else date.max)
    elif p_field == 'done' or p_field == 'completed' or p_field == 'completion':
        result = (lambda a: a.completion_date() if a.completion_date()
                  else date.max)
    elif p_field == 'importance':
        result = importance
    elif p_field == 'importance-avg' or p_field == 'importance-average':
        result = average_importance
    elif p_field == 'length':
        result = lambda a: a.length()
    elif p_field == 'project' or p_field == 'projects':
        result = lambda a: sorted([c.lower() for c in a.projects()])
    elif p_field == 'text':
        result = lambda a: a.text()
    else:
        # try to find the corresponding tag
        # when a tag is not present, push it to the end of the list by giving
        # it an artificially higher value
        result = (lambda a: "0" + a.tag_value(p_field) if a.has_tag(p_field)
                  else "1")

    return result


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
        self.groupfunctions = self._parse(p_groupstring) if p_groupstring else []
        self.sortfunctions = self._parse(p_sortstring)

    def sort(self, p_todos):
        """
        Sorts the list of todos given as a parameter, returns a new sorted
        list.

        The list is traversed in reverse order, such that the most specific
        sort operation is done first, relying on the stability of the sorted()
        function.
        """
        sorted_todos = p_todos
        for function, order in reversed(self.sortfunctions):
            sorted_todos = sorted(sorted_todos, key=function,
                                  reverse=(order == 'desc'))

        return sorted_todos

    def group(self, p_todos):
        """
        Groups the todos according to the given group string. Assumes that the
        given todos have already been sorted with self.sort().
        """
        # preorder todos for the group sort
        for function, _ in self.groupfunctions:
            p_todos = sorted(p_todos, key=function)

        # initialize result with a single group
        result = OrderedDict([((), p_todos)])

        for function, _ in self.groupfunctions:
            oldresult = result
            result = OrderedDict()
            for oldkey, oldgroup in oldresult.items():
                for key, group in groupby(oldgroup, function):
                    newgroup = list(group)

                    if not isinstance(key, list):
                        key = [key]

                    for subkey in key:
                        newkey = oldkey + (subkey,)

                        if newkey in result:
                            result[newkey] = result[newkey] + newgroup
                        else:
                            result[newkey] = newgroup

        # sort all groups
        for key, group in result.items():
            result[key] = self.sort(group)

        return result

    def _parse(self, p_string):
        """
        Parses a sort string and returns a list of functions and the
        desired order.
        """
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
                function = get_field_function(field)

                # reverse order for priority: lower characters have higher
                # priority
                if is_priority_field(field):
                    order = 'asc' if order == 'desc' else 'desc'

                result.append((function, order))

        return result


if __name__ == '__main__':
    from topydo.lib.Todo import Todo
    todos = [
        Todo('Foo +A @A type:a'),
        Todo('Foo +A @B type:b'),
        Todo('Bar +B @B type:b'),
        Todo('Baz +A +B @B'),
    ]

    s = Sorter('desc:context', 'project,type')

    for key, group in s.group(todos).items():
        print(key)
        for item2 in group:
            print(item2.source())
