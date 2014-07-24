#!/usr/bin/env python
""" Entry file for the Python todo.txt CLI. """

import datetime
import re
import sys

import Config
import Filter
from PrettyPrinter import pretty_print
from RelativeDate import relative_date_to_date
import Sorter
import TodoFile
import TodoList
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

def convert_number(p_number):
    """ Converts a string number to an integer. """
    try:
        p_number = int(p_number)
    except ValueError:
        error("Invalid todo number given.")

    return p_number

def preprocess_input_todo(p_text):
    """
    Preprocesses user input when adding a task.

    It does:

    * Detect a priority mid-sentence and puts it at the start.
    """
    p_text = re.sub(r'^(.+) (\([A-Z]\))(.*)$', r'\2 \1\3', p_text)

    return p_text

def postprocess_input_todo(p_todo):
    """
    Post-processes a parsed todo when adding it to the list.

    * It converts relative dates to absolute ones.
    * Automatically inserts a creation date if not present.
    """
    for tag in [Config.TAG_START, Config.TAG_DUE]:
        value = p_todo.tag_value(tag)

        if value:
            date = relative_date_to_date(value)
            if date:
                p_todo.set_tag(tag, date.isoformat())

    p_todo.set_creation_date(datetime.date.today())

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
        text = preprocess_input_todo(argument(2))
        todo = self.todolist.add(text)
        postprocess_input_todo(todo)
        self.print_todo(self.todolist.count())
        self.dirty = True

    def append(self):
        """ Appends a text to a todo item. """
        number = convert_number(argument(2))
        text = argument(3)

        self.todolist.append(number, text)

        self.print_todo(number)
        self.dirty = True

        self.dirty = True

    def dep(self):
        """ Handles dependencies between todos. """
        def handle_add_rm(operation):
            """ Handles the add and rm subsubcommands. """
            from_todonumber = convert_number(argument(3))
            to_todonumber = argument(4)

            if to_todonumber == 'to':
                to_todonumber = convert_number(argument(5))
            else:
                to_todonumber = convert_number(to_todonumber)

            if operation == 'add':
                self.todolist.add_dependency(from_todonumber, to_todonumber)
            else:
                self.todolist.remove_dependency(from_todonumber, to_todonumber)

            self.dirty = True

        def handle_ls():
            """ Handles the ls subsubcommand. """
            arg1 = argument(3)
            arg2 = argument(4)

            todos = []
            if arg2 == 'to':
                # dep ls 1 to ...
                todos = self.todolist.children(convert_number(arg1))
            elif arg1 == 'to':
                # dep ls ... to 1
                todos = self.todolist.parents(convert_number(arg2))
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
            self.dirty = True
        elif subsubcommand == 'ls':
            handle_ls()
        else:
            usage()

    def do(self):
        number = convert_number(argument(2))
        todo = self.todolist.todo(number)

        if todo:
            todo.set_completed()
            self.print_todo(number)
            self.dirty = True

    def pri(self):
        number = convert_number(argument(2))
        priority = argument(3)

        if re.match('^[A-Z]$', priority):
            todo = self.todolist.todo(number)

            if todo:
                old_priority = todo.priority()
                todo.set_priority(priority)

                print "Priority changed from %s to %s" \
                    % (old_priority, priority)
                self.print_todo(number)
                self.dirty = True
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

        if self.dirty:
            todofile.write(str(self.todolist))

if __name__ == '__main__':
    Application().run()
