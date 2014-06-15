""" Provides a function to pretty print a list of todo items. """

import re

import Config

PRIORITY_COLORS = {
    'A': '\033[36m', # cyan
    'B': '\033[33m', # yellow
    'C': '\033[34m'  # blue
}

def add_colors(p_todo_str, p_todo):
    """ Adds colors to the todo string by inserting ANSI codes. """

    color = '\033[0m'
    try:
        color = PRIORITY_COLORS[p_todo.priority()]
    except KeyError:
        pass

    p_todo_str = '%s%s%s' % (color, p_todo_str, '\033[0m')

    if Config.HIGHLIGHT_PROJECTS_CONTEXTS:
        p_todo_str = re.sub(r'\B(\+|@)\S+', r'\033[31m\g<0>' + color, \
            p_todo_str)

    return p_todo_str

def pretty_print(p_todos, p_show_numbers=False, p_color=False):
    """
    Given a list of todo items, pretty print it and return a list of
    formatted strings.
    """

    result = []

    for todo in p_todos:
        todo_str = str(todo)

        if p_show_numbers:
            todo_str = "%3d %s" % (todo.number, todo_str)

        if Config.COLORS and p_color:
            todo_str = add_colors(todo_str, todo)

        result.append(todo_str)

    return result
