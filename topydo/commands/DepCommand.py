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

from topydo.lib.Command import Command, InvalidCommandArgument
from topydo.lib.Config import config
from topydo.lib import Filter
from topydo.lib.PrettyPrinter import pretty_printer_factory
from topydo.lib.Sorter import Sorter
from topydo.lib.TodoListBase import InvalidTodoException
from topydo.lib.View import View

class DepCommand(Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(DepCommand, self).__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

        try:
            self.subsubcommand = self.argument(0)
        except InvalidCommandArgument:
            self.subsubcommand = None

        self.printer = pretty_printer_factory(self.todolist)

    def _handle_add(self):
        (from_todo, to_todo) = self._get_todos()

        if from_todo and to_todo:
            self.todolist.add_dependency(from_todo, to_todo)

    def _handle_rm(self):
        (from_todo, to_todo) = self._get_todos()

        if from_todo and to_todo:
            self.todolist.remove_dependency(from_todo, to_todo)

    def _get_todos(self):
        from_todo = None
        to_todo = None

        try:
            operator = self.argument(2)

            if operator == 'before' or operator == 'partof':
                from_todo_nr = self.argument(3)
                to_todo_nr = self.argument(1)
            elif operator == 'to' or operator == 'after':
                from_todo_nr = self.argument(1)
                to_todo_nr = self.argument(3)
            else:
                # the operator was omitted, assume 2nd argument is target task
                # default to 'to' behavior
                from_todo_nr = self.argument(1)
                to_todo_nr = self.argument(2)

            from_todo = self.todolist.todo(from_todo_nr)
            to_todo = self.todolist.todo(to_todo_nr)
        except (InvalidTodoException):
            self.error("Invalid todo number given.")
        except InvalidCommandArgument:
            self.error(self.usage())

        return (from_todo, to_todo)

    def _handle_ls(self):
        """ Handles the ls subsubcommand. """
        try:
            arg1 = self.argument(1)
            arg2 = self.argument(2)

            todos = []
            if arg2 == 'to':
                # dep ls 1 to ...
                number = arg1
                todo = self.todolist.todo(number)
                todos = self.todolist.children(todo)
            elif arg1 == 'to':
                # dep ls ... to 1
                number = arg2
                todo = self.todolist.todo(number)
                todos = self.todolist.parents(todo)
            else:
                self.error(self.usage())

            if todos:
                sorter = Sorter(config().sort_string())
                instance_filter = Filter.InstanceFilter(todos)
                view = View(sorter, [instance_filter], self.todolist)
                self.out(self.printer.print_list(view.todos))
        except InvalidTodoException:
            self.error("Invalid todo number given.")
        except InvalidCommandArgument:
            self.error(self.usage())

    def execute(self):
        if not super(DepCommand, self).execute():
            return False

        dispatch = {
            'add':   self._handle_add,
            'rm':    self._handle_rm,
            'del':   self._handle_rm,
            'ls':    self._handle_ls,
            'clean': self.todolist.clean_dependencies,
            'gc':    self.todolist.clean_dependencies,
        }

        if self.subsubcommand in dispatch:
            dispatch[self.subsubcommand]()
        else:
            self.error(self.usage())

    def usage(self):
        return """Synopsis:
  dep <add|rm> <NUMBER> [to] <NUMBER>
  dep add <NUMBER> <before|partof|after> <NUMBER>
  dep ls <NUMBER> to
  dep ls to <NUMBER>
  dep clean"""

    def help(self):
        return """\
* add              : Adds a dependency. Using 1 before 2 creates a dependency
                     from todo item 2 to 1.
* rm (alias: del)  : Removes a dependency.
* ls               : Lists all dependencies to or from a certain todo.
* clean (alias: gc): Removes redundant id or p tags.
"""
