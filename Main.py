#!/usr/bin/env python
""" Entry file for the Python todo.txt CLI. """

import sys

from AddCommand import AddCommand
from AppendCommand import AppendCommand
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

def arguments():
    """
    Retrieves all values from the argument list starting from the given
    position.
    """
    try:
        values = sys.argv[2:] # strip off subcommand at position 1
    except IndexError:
        usage()

    return values

class CLIApplication(object):
    def __init__(self):
        self.todolist = TodoList.TodoList([])

    def run(self):
        """ Main entry function. """
        todofile = TodoFile.TodoFile(Config.FILENAME)

        try:
            self.todolist = TodoList.TodoList(todofile.read())
        except Exception:
            pass # TODO

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

        if subcommand in subcommand_map:
          command = subcommand_map[subcommand](arguments(), self.todolist,
              lambda o: sys.stdout.write(o + "\n"),
              lambda e: sys.stderr.write(e + "\n"),
              raw_input)

          if not command.execute():
              exit(1)
        else:
            usage()

        if self.todolist.is_dirty():
            todofile.write(str(self.todolist))

if __name__ == '__main__':
    CLIApplication().run()
