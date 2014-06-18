#!/usr/bin/env python
""" Entry file for the Python todo.txt CLI. """

import re
import sys

import Config
import Filter
from PrettyPrinter import pretty_print
import Sorter
import TodoFile
import TodoList

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

class Application(object):
    def __init__(self):
        self.todolist = TodoList.TodoList([])
        self.dirty = False

    def print_todo(self, p_number):
        """ Prints a single todo item to the standard output. """
        todo = self.todolist.todo(p_number)
        printed = pretty_print([todo], True, True)
        print printed[0]

    def add(self):
        """ Adds a todo item to the list. """
        try:
            self.todolist.add(sys.argv[2])

            self.print_todo(self.todolist.count())
            self.dirty = True
        except IndexError:
            error("No todo text was given.")

    def append(self):
        """ Appends a text to a todo item. """

        try:
            number = sys.argv[2]
            text = sys.argv[3]
        except IndexError:
            usage()

        try:
            number = int(number)
            self.todolist.append(number, text)

            self.print_todo(number)
            self.dirty = True
        except ValueError:
            error("Invalid todo number given.")

    def do(self):
        try:
            number = sys.argv[2]
        except IndexError:
            usage()

        try:
            number = int(number)
            self.todolist.todo(number).set_completed()

            self.print_todo(number)
            self.dirty = True
        except IndexError:
            usage()
        except ValueError:
            error("Invalid todo number given.")

    def pri(self):
        try:
            number = sys.argv[2]
            priority = sys.argv[3]
        except IndexError:
            usage()

        if re.match('^[A-Z]$', priority):
            try:
                number = int(number)
                todo = self.todolist.todo(number)
                old_priority = todo.priority()
                todo.set_priority(priority)

                print "Priority changed from %s to %s" \
                    % (old_priority, priority)
                self.print_todo(number)
                self.dirty = True
            except AttributeError:
                error("Invalid todo number given.")
            except ValueError:
                error("Invalid todo number given.")
        else:
            error("Invalid priority given.")

    def list(self):
        sorter = Sorter.Sorter(Config.SORT_STRING)
        filters = [Filter.RelevanceFilter()]

        if len(sys.argv) > 2:
            filters.append(Filter.GrepFilter(sys.argv[2]))

        print self.todolist.view(sorter, filters).pretty_print()

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

        if self.dirty:
            todofile.write(str(self.todolist))

if __name__ == '__main__':
    Application().run()
