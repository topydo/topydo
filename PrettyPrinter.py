""" Provides a function to pretty print a list of todo items. """

import re

import Config

PRIORITY_COLORS = {
    'A': '\033[36m', # cyan
    'B': '\033[33m', # yellow
    'C': '\033[34m'  # blue
}

PROJECT_COLOR = '\033[31m' # red
NEUTRAL_COLOR = '\033[0m'

def pp_color(p_todo_str, p_todo):
    """
    Adds colors to the todo string by inserting ANSI codes.

    Should be passed as a filter in the filter list of pretty_print()
    """

    if Config.COLORS:
        color = NEUTRAL_COLOR
        try:
            color = PRIORITY_COLORS[p_todo.priority()]
        except KeyError:
            pass

        p_todo_str = '%s%s%s' % (color, p_todo_str, NEUTRAL_COLOR)

        if Config.HIGHLIGHT_PROJECTS_CONTEXTS:
            p_todo_str = re.sub(r'\B(\+|@)\S+', PROJECT_COLOR + r'\g<0>' + color, \
                p_todo_str)

    return p_todo_str

def pp_number(p_todo_str, p_todo):
    """
    Inserts the todo number at the start of the string.

    Should be passed as a filter in the filter list of pretty_print()
    """
    return "%3d %s" % (p_todo.attributes['number'], p_todo_str)

def pretty_print(p_todos, p_filters=[]):
    """
    Given a list of todo items, pretty print it and return a list of
    formatted strings.

    p_filters is a list of functions that transform the output string, each
    function accepting two arguments:

    * the todo's text that has to be modified;
    * the todo object itself which allows for obtaining relevant information.

    Examples are pp_color and pp_number in this file.
    """

    result = []

    for todo in p_todos:
        todo_str = str(todo)

        for f in p_filters:
            todo_str = f(todo_str, todo)

        result.append(todo_str)

    return result
