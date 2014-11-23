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

import getopt

class InvalidCommandArgument(Exception):
    pass

class Command(object):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        """
        Sets up the basic properties for executing a subcommand.

        p_args is a list of arguments that can be passed to this subcommand.
        These can be retrieved with argument().

        p_todolist is a reference to the todolist instance to operate on.

        p_out is a function to be called to print (standard) output. Defaults
        to a noop.

        p_err is a function to be called to print errors. Defaults to a noop.

        p_prompt is a function that accepts a prompt string as its own argument
        and returns the answer to that prompt (normally entered by the user in
        some way). The default is a noop prompt.
        """
        self.args = p_args
        self.todolist = p_todolist

        # inputs and outputs
        self.out = p_out
        self.error = p_err
        self.prompt = p_prompt

    def execute(self):
        """
        Execute the command. Intercepts the help subsubcommand to show the help
        text.
        """
        if self.args and self.argument(0) == "help":
            self.error(self.usage() + "\n\n" + self.help())
            return False

        return True

    def argument(self, p_number):
        """ Retrieves a value from the argument list at the given position. """
        value = None
        try:
            value = self.args[p_number]
        except IndexError:
            raise InvalidCommandArgument

        return value

    def getopt(self, p_flags, p_long=None):
        p_long = p_long or []

        try:
            result = getopt.getopt(self.args, p_flags, p_long)
        except getopt.GetoptError as goe:
            self.error(str(goe))
            result = ([], self.args)

        return result

    def usage(self):
        return "No usage text available for this command."

    def help(self):
        return "No help text available for this command."

