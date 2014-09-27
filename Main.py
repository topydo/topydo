#!/usr/bin/env python
""" Entry file for the Python todo.txt CLI. """

import re
import sys

from AddCommand import AddCommand
import Config
import Filter
from PrettyPrinter import pretty_print
from Recurrence import advance_recurring_todo
import Sorter
import TodoFile
import TodoList
from Utils import convert_todo_number
import View

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
        printed = pretty_print([todo], True, True)
        print printed[0]

    def add(self):
        command = AddCommand(arguments(), self.todolist)
        if command.execute():
            self.print_todo(self.todolist.count())

    def append(self):
        """ Appends a text to a todo item. """
        number = convert_todo_number(argument(2))
        text = argument(3)

        self.todolist.append(number, text)

        self.print_todo(number)

    def dep(self):
        """ Handles dependencies between todos. """
        def handle_add_rm(operation):
            """ Handles the add and rm subsubcommands. """
            from_todonumber = convert_todo_number(argument(3))
            to_todonumber = argument(4)

            if to_todonumber == 'to':
                to_todonumber = convert_todo_number(argument(5))
            else:
                to_todonumber = convert_todo_number(to_todonumber)

            if operation == 'add':
                self.todolist.add_dependency(from_todonumber, to_todonumber)
            else:
                self.todolist.remove_dependency(from_todonumber, to_todonumber)

        def handle_ls():
            """ Handles the ls subsubcommand. """
            arg1 = argument(3)
            arg2 = argument(4)

            todos = []
            if arg2 == 'to':
                # dep ls 1 to ...
                todos = self.todolist.children(convert_todo_number(arg1))
            elif arg1 == 'to':
                # dep ls ... to 1
                todos = self.todolist.parents(convert_todo_number(arg2))
            else:
                usage()

            if todos:
                sorter = Sorter.Sorter(Config.SORT_STRING)
                view = View.View(sorter, [], todos)
                print view.pretty_print()

        subsubcommand = argument(2)
        if subsubcommand == 'add' or \
            subsubcommand == 'rm' or subsubcommand == 'del':

            handle_add_rm(subsubcommand)
        elif subsubcommand == 'clean' or subsubcommand == 'gc':
            self.todolist.clean_dependencies()
        elif subsubcommand == 'ls':
            handle_ls()
        else:
            usage()

    def do(self):
        def complete_children(p_number):
            children = [t.attributes['number'] for t in self.todolist.children(p_number) if not t.is_completed()]
            if children:
                for child in children:
                    self.print_todo(child)

                confirmation = raw_input("Also mark subtasks as done? [n] ");

                if re.match('^y(es)?$', confirmation, re.I):
                    for child in children:
                        self.todolist.todo(child).set_completed()
                        self.print_todo(child)

        def handle_recurrence(todo):
            if todo.has_tag('rec'):
                new_todo = advance_recurring_todo(todo)
                self.todolist.add_todo(new_todo)
                self.print_todo(self.todolist.count())

        number = convert_todo_number(argument(2))
        todo = self.todolist.todo(number)

        if todo and not todo.is_completed():
            complete_children(number)
            handle_recurrence(todo)

            todo.set_completed()
            self.print_todo(number)

    def pri(self):
        number = convert_todo_number(argument(2))
        priority = argument(3)

        if re.match('^[A-Z]$', priority):
            todo = self.todolist.todo(number)

            if todo:
                old_priority = todo.priority()
                todo.set_priority(priority)

                print "Priority changed from %s to %s" \
                    % (old_priority, priority)
                self.print_todo(number)
        else:
            error("Invalid priority given.")

    def list(self):
        sorter = Sorter.Sorter(Config.SORT_STRING)
        filters = [Filter.DependencyFilter(self.todolist),
                   Filter.RelevanceFilter()]

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
