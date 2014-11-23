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

from topydo.lib.Todo import Todo
from topydo.lib.TodoFile import TodoFile
from topydo.lib.TodoList import TodoList

def load_file(p_filename):
    """
    Loads a todo file from the given filename and returns a list of todos.
    """
    todolist = load_file_to_raw_list(p_filename)
    return [Todo(src) for src in todolist]

def load_file_to_raw_list(p_filename):
    """
    Loads a todo file from the given filename and returns a list of todo
    strings (unparsed).
    """
    todofile = TodoFile(p_filename)
    return todofile.read()

def load_file_to_todolist(p_filename):
    """
    Loads a todo file to a TodoList instance.
    """
    todolist = load_file_to_raw_list(p_filename)
    return TodoList(todolist)

def todolist_to_string(p_list):
    """ Converts a todo list to a single string. """
    return '\n'.join([str(t) for t in p_list])
