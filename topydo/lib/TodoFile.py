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
This module deals with todo.txt files.
"""

class TodoFile(object):
    """
    This class represents a todo.txt file, which can be read from or written
    to.
    """

    def __init__(self, p_path):
        self.path = p_path

    def read(self):
        """ Reads the todo.txt file and returns a list of todo items.  """
        todos = []
        try:
            todofile = open(self.path, 'r')
            todos = todofile.readlines()
            todofile.close()
        except IOError:
            pass

        return todos

    def write(self, p_todos):
        """
        Writes all the todo items in the p_todos array to a todo.txt file.
        """

        todofile = open(self.path, 'w')

        if p_todos is list:
            for todo in p_todos:
                todofile.write(str(todo))
        else:
            todofile.write(p_todos)

        todofile.close()
