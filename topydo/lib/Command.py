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

import getopt

from topydo.lib.printers.PrettyPrinter import PrettyPrinter


class InvalidCommandArgument(Exception):
    pass


class Command(object):
    def __init__(self, p_args, p_todolist, #pragma: no branch
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

        # make pretty printer available
        self.printer = PrettyPrinter()

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
        try:
            return self.args[p_number]
        except IndexError as ie:
            raise InvalidCommandArgument from ie

    def getopt(self, p_flags, p_long=None):
        p_long = p_long or []

        try:
            result = getopt.getopt(self.args, p_flags, p_long)
        except getopt.GetoptError as goe:
            self.error(str(goe))
            result = ([], self.args)

        return result

    @classmethod
    def name(cls):
        """" Returns short-name of the command. """
        return cls.__name__[:-7].lower()  # strip 'Command'

    def execute_post_archive_actions(self):
        """ Runs various hooks that should take place after archiving. """
        pass

    def usage(self):
        """ Returns a one-line synopsis for this command. """
        raise NotImplementedError

    def help(self):
        """ Returns the help text for this command. """
        raise NotImplementedError
