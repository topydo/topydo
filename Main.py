#!/usr/bin/env python
""" Entry file for the Python todo.txt CLI. """

import sys

from AddCommand import AddCommand
from AppendCommand import AppendCommand
from DepCommand import DepCommand
import Config
from DoCommand import DoCommand
from ListCommand import ListCommand
from PrettyPrinter import *
from PriorityCommand import PriorityCommand
import TodoFile
import TodoList
from Utils import convert_todo_number

def print_iterable(p_iter):
    """ Prints an iterable to the standard output, one item per line. """
    for item in sorted(p_iter):
        print item

def usage():
    """ Prints the usage of the todo.txt CLI """
    exit(1)

def error(p_message, p_exit=True):
    """ Prints a message on the standard error. """
    sys.stderr.write(p_message + '\n')

    if p_exit:
        exit(1)

def argument(p_number):
    """ Retrieves a value from the argument list. """
    try:
        value = sys.argv[p_number]
    except IndexError:
        usage()

    return value

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

class Application(object): # TODO: rename to CLIApplication
    def __init__(self):
        self.todolist = TodoList.TodoList([])

    def print_todo(self, p_number):
        """ Prints a single todo item to the standard output. """
        todo = self.todolist.todo(p_number)
        printed = pretty_print([todo], [pp_number, pp_color])
        print printed[0]

    def add(self):
        command = AddCommand(arguments(), self.todolist)
        if command.execute():
            self.print_todo(self.todolist.count())

    def append(self):
        """ Appends a text to a todo item. """
        command = AppendCommand(arguments(), self.todolist)
        command.execute()

    def dep(self):
        command = DepCommand(arguments(), self.todolist)
        command.execute()

    def do(self):
        command = DoCommand(arguments(), self.todolist)
        command.execute()

    def pri(self):
        command = PriorityCommand(arguments(), self.todolist)
        command.execute()

    def list(self):
        command = ListCommand(arguments(), self.todolist)
        command.execute()

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

        if subcommand == 'add':
            self.add()
        elif subcommand == 'app' or subcommand == 'append':
            self.append()
        elif subcommand == 'dep':
            self.dep()
        elif subcommand == 'do':
            self.do()
        elif subcommand == 'ls':
            self.list()
        elif subcommand == 'lsprj' or subcommand == 'listproj':
            print_iterable(self.todolist.projects())
        elif subcommand == 'lscon' or subcommand == 'listcon':
            print_iterable(self.todolist.contexts())
        elif subcommand == 'pri':
            self.pri()
        else:
            usage()

        if self.todolist.is_dirty():
            todofile.write(str(self.todolist))

if __name__ == '__main__':
    Application().run()
