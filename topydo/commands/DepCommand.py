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

from topydo.lib import Filter
from topydo.lib.Command import Command, InvalidCommandArgument
from topydo.lib.Config import config
from topydo.lib.printers.Dot import DotPrinter
from topydo.lib.printers.PrettyPrinter import pretty_printer_factory
from topydo.lib.Sorter import Sorter
from topydo.lib.TodoListBase import InvalidTodoException
from topydo.lib.View import View


class DepCommand(Command):
    def __init__(self, p_args, p_todolist, #pragma: no branch
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super().__init__(
            p_args, p_todolist, p_out, p_err, p_prompt)

        try:
            self.subsubcommand = self.argument(0)
        except InvalidCommandArgument:
            self.subsubcommand = None

        self.printer = pretty_printer_factory(self.todolist)

    def _handle_add(self):
        for from_todo, to_todo in self._get_todos():
            self.todolist.add_dependency(from_todo, to_todo)

    def _handle_rm(self):
        for from_todo, to_todo in self._get_todos():
            self.todolist.remove_dependency(from_todo, to_todo)

    def _get_todos(self):
        result = []

        def get_parent_dependencies():
            child_todo = first_todo
            sibling_todo = second_todo

            return [(parent, child_todo) for parent in self.todolist.parents(sibling_todo)]

        def get_child_dependencies():
            parent_todo = first_todo
            sibling_todo = second_todo

            return [(parent_todo, child) for child in self.todolist.children(sibling_todo)]

        get_before_dependency = lambda: [(second_todo, first_todo)]
        get_after_dependency = lambda: [(first_todo, second_todo)]

        operators = {
            "after": get_after_dependency,
            "before": get_before_dependency,
            "child-of": get_child_dependencies,
            "childof": get_child_dependencies,
            "children-of": get_child_dependencies,
            "childrenof": get_child_dependencies,
            "parent-of": get_parent_dependencies,
            "parentof": get_parent_dependencies,
            "parents-of": get_parent_dependencies,
            "parentsof": get_parent_dependencies,
            "partof": get_before_dependency,
            "to": get_after_dependency,
        }

        try:
            first_todo_nr = self.argument(1)
            operator = self.argument(2)

            if operator in operators:
                second_todo_nr = self.argument(3)
            else:
                second_todo_nr = self.argument(2)
                operator = "to"

            first_todo = self.todolist.todo(first_todo_nr)
            second_todo = self.todolist.todo(second_todo_nr)

            result = operators[operator]()
        except (InvalidTodoException):
            self.error("Invalid todo number given.")
        except InvalidCommandArgument:
            self.error(self.usage())

        return result

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

    def _handle_dot(self):
        """ Handles the dot subsubcommand. """
        self.printer = DotPrinter(self.todolist)

        try:
            arg = self.argument(1)
            todo = self.todolist.todo(arg)
            arg = self.argument(1)
            todos = set([self.todolist.todo(arg)])
            todos |= set(self.todolist.children(todo))
            todos |= set(self.todolist.parents(todo))
            todos = sorted(todos, key=lambda t: t.text())

            self.out(self.printer.print_list(todos))
        except InvalidTodoException:
            self.error("Invalid todo number given.")
        except InvalidCommandArgument:
            self.error(self.usage())


    def execute(self):
        if not super().execute():
            return False

        dispatch = {
            'add':   self._handle_add,
            'rm':    self._handle_rm,
            'del':   self._handle_rm,
            'ls':    self._handle_ls,
            'clean': self.todolist.clean_dependencies,
            'dot':   self._handle_dot,
            'gc':    self.todolist.clean_dependencies,
        }

        if self.subsubcommand in dispatch:
            dispatch[self.subsubcommand]()
        else:
            self.error(self.usage())

    def usage(self):
        return """Synopsis:
  dep <add|rm> <NUMBER> [to] <NUMBER>
  dep add <NUMBER> <before|partof|after|parents-of|children-of> <NUMBER>
  dep ls <NUMBER> to
  dep ls to <NUMBER>
  dep dot <NUMBER>
  dep clean"""

    def help(self):
        return """\
* add               : Adds a dependency. `dep add 1 2` denotes that todo item 1
                      is dependant on todo item 2, i.e. item 2 is a subitem of
                      item 1.
* rm (alias: del)   : Removes a dependency.
* ls                : Lists all dependencies to or from a certain todo.
* dot               : Prints a dependency tree as a Dot graph.
* clean (alias: gc) : Removes redundant id or p tags.\
"""
