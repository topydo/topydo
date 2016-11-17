# Topydo - A todo.txt client written in Python.
# Copyright (C) 2015 Bram Schoenmakers <bram@topydo.org>
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
Provides a printer that transforms a list of Todo items to a JSON structure
such that other applications can process it.
"""

import json

from topydo.lib.printers.PrettyPrinter import Printer


def _convert_todo(p_todo):
    """ Converts a Todo instance to a dictionary. """
    creation_date = p_todo.creation_date()
    completion_date = p_todo.completion_date()

    result = {
        'source': p_todo.source(),
        'text': p_todo.text(),
        'priority': p_todo.priority(),
        'completed': p_todo.is_completed(),
        'tags': p_todo.tags(),
        'projects': list(p_todo.projects()),
        'contexts': list(p_todo.contexts()),
        'creation_date':
            creation_date.isoformat() if creation_date else None,
        'completion_date':
            completion_date.isoformat() if completion_date else None
    }

    return result


class JsonPrinter(Printer):
    """
    A printer that converts a list of Todo items to a string in JSON format.
    """

    def __init__(self):
        super().__init__()

    def print_todo(self, p_todo):
        return json.dumps(_convert_todo(p_todo), ensure_ascii=False,
                          sort_keys=True)

    def print_list(self, p_todos):
        result = []

        for todo in p_todos:
            result.append(_convert_todo(todo))

        return json.dumps(result, ensure_ascii=False, sort_keys=True)
