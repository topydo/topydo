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

import os
from subprocess import call

from topydo.lib.Command import Command
from topydo.lib.Config import config

class EditCommand(Command):
    def __init__(self, p_args, p_todolist, p_output, p_error, p_input):
        super(EditCommand, self).__init__(p_args, p_todolist, p_output,
            p_error, p_input)

    def execute(self):
        if not super(EditCommand, self).execute():
            return False

        editor = os.environ['EDITOR'] or 'vi'
        todo = config().todotxt()

        return call([editor, todo]) == 0

    def usage(self):
        return """Synopsis: edit"""

    def help(self):
        return """Launches a text editor with the todo.txt file.

By default it will use $EDITOR in your environment, otherwise it will fall back
to 'vi'.
"""
