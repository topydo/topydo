""" This module provides functionality to sort lists with todo items. """

import datetime
import re

import Config
from Importance import importance

def is_priority_field(p_field):
    """ Returns True when the field name denotes the priority. """
    return p_field.startswith('prio')

def get_field_function(p_field):
    """
    Given a property (string) of a todo, return a function that attempts to
    access that property. If the property could not be located, return the
    identity function.
    """
    result = lambda a: a

    if is_priority_field(p_field):
        result = lambda a: a.priority()
    elif p_field == 'creationdate' or p_field == 'creation':
        # when a task has no creation date, push it to the end by assigning it
        # the maximum possible date.
        result = (lambda a: a.creation_date() if a.creation_date() \
            else datetime.date.max)
    elif p_field == 'done' or p_field == 'completed' or p_field == 'completion':
        result = (lambda a: a.completion_date() if a.completion_date() \
            else datetime.date.max)
    elif p_field == 'importance':
        result = lambda a: importance(a, Config.IGNORE_WEEKENDS)
    elif p_field == 'text':
        result = lambda a: a.text()
    else:
        # try to find the corresponding tag
        # when a tag is not present, push it to the end of the list by giving
        # it an artificially higher value
        result = (lambda a: "0" + a.tag_value(p_field) if a.has_tag(p_field) \
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
    def __init__(self, p_sortstring="desc:priority"):
        self.sortstring = p_sortstring
        self.functions = []
        self._parse()

    def sort(self, p_todos):
        """
        Sorts the list of todos given as a parameter, returns a new sorted
        list.

        The list is traversed in reverse order, such that the most specific
        sort operation is done first, relying on the stability of the sorted()
        function.
        """

        sorted_todos = p_todos
        for function, order in reversed(self.functions):
            sorted_todos = sorted(sorted_todos, None, function, order == 'desc')

        return sorted_todos

    def _parse(self):
        """
        Parses a sort string and returns a list of functions and the
        desired order.
        """
        fields = self.sortstring.lower().split(',')

        for field in fields:
            parsed_field = re.match( \
                r'((?P<order>asc(ending)?|desc(ending)?):)?(?P<field>\S+)', \
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

                self.functions.append((function, order))
