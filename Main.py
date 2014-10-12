#!/usr/bin/env python
""" Entry file for the Python todo.txt CLI. """

import sys

from AddCommand import AddCommand
from AppendCommand import AppendCommand
from ArchiveCommand import ArchiveCommand
from DepCommand import DepCommand
import Config
from DoCommand import DoCommand
from ListCommand import ListCommand
from ListContextCommand import ListContextCommand
from ListProjectCommand import ListProjectCommand
from PrettyPrinter import *
from PriorityCommand import PriorityCommand
import TodoFile
import TodoList
from Utils import convert_todo_number

def usage():
    """ Prints the usage of the todo.txt CLI """
    exit(1)

def arguments(p_start=2):
    """
    Retrieves all values from the argument list starting from the given
    position.

    This is a parameter, because argv has a different structure when no
    subcommand was given and it fallbacks to the default subcommand.
    """
    try:
        values = sys.argv[p_start:]
    except IndexError:
        usage()

    return values

class CLIApplication(object):
    def __init__(self):
        self.todolist = TodoList.TodoList([])

    def archive(self):
        """
        Performs an archive action on the todolist.

        This means that all completed tasks are moved to the archive file
        (defaults to done.txt).
        """
        archive_file = TodoFile.TodoFile(Config.ARCHIVE_FILENAME)
        archive = TodoList.TodoList(archive_file.read())

        if archive:
            command = ArchiveCommand(self.todolist, archive)
            command.execute()

            if archive.is_dirty():
                archive_file.write(archive)


    def run(self):
        """ Main entry function. """
        todofile = TodoFile.TodoFile(Config.FILENAME)
        self.todolist = TodoList.TodoList(todofile.read())

        try:
            subcommand = sys.argv[1]
        except IndexError:
            subcommand = Config.DEFAULT_ACTION

        subcommand_map = {
          'add': AddCommand,
          'app': AppendCommand,
          'append': AppendCommand,
          'dep': DepCommand,
          'do': DoCommand,
          'ls': ListCommand,
          'lscon': ListContextCommand,
          'listcon': ListContextCommand,
          'lsprj': ListProjectCommand,
          'lsproj': ListProjectCommand,
          'listprj': ListProjectCommand,
          'listproj': ListProjectCommand,
          'listproject': ListProjectCommand,
          'listprojects': ListProjectCommand,
          'pri': PriorityCommand,
        }

        args = arguments()
        if not subcommand in subcommand_map:
            subcommand = Config.DEFAULT_ACTION
            args = arguments(1)

        command = subcommand_map[subcommand](args, self.todolist,
            lambda o: sys.stdout.write(o + "\n"),
            lambda e: sys.stderr.write(e + "\n"),
            raw_input)

        if command.execute() == False:
            exit(1)

        if self.todolist.is_dirty():
            # self.archive()
            todofile.write(str(self.todolist))

if __name__ == '__main__':
    CLIApplication().run()
