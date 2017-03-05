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

from itertools import product

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

    def _preprocess(self):
        operators = {
            'after': 'get_after_deps',
            'before': 'get_before_deps',
            'child-of': 'get_child_deps',
            'childof': 'get_child_deps',
            'children-of': 'get_child_deps',
            'childrenof': 'get_child_deps',
            'parent-of': 'get_parent_deps',
            'parentof': 'get_parent_deps',
            'parents-of': 'get_parent_deps',
            'parentsof': 'get_parent_deps',
            'partof': 'get_before_deps',
            'to': 'get_to',  # 'to' is special so don't be definitive here
        }

        try:
            matching_operators = set(self.args[1:]).intersection(set(operators))
            if len(matching_operators) == 1:
                operator = matching_operators.pop()
            else:
                raise InvalidCommandArgument

            operator_pos = self.args.index(operator)
            first_todo_nrs = self.args[1:operator_pos]
            second_todo_nrs = self.args[operator_pos + 1:]

            if not first_todo_nrs and not second_todo_nrs:
                raise InvalidCommandArgument

            return (first_todo_nrs, second_todo_nrs, operators[operator])
        except (KeyError, IndexError):
            raise InvalidCommandArgument

    def _handle_add(self):
        from_todos = set()
        to_todos = set()

        for from_todo, to_todo in self._get_todos():
            self.todolist.add_dependency(from_todo, to_todo)

            from_todos.add(from_todo)
            to_todos.add(to_todo)

        if from_todos and to_todos:
            if len(from_todos) == 1:
                following = 'item'
                depend = 'depends'
            else:
                following = 'items'
                depend = 'depend'

            item = 'item' if len(to_todos) == 1 else 'items'

            self.out('Following todo ' + following + ':')
            self.out(self.printer.print_list(from_todos))
            self.out(depend + ' now on todo ' + item + ' below:')
            self.out(self.printer.print_list(to_todos))
        else:
            self.out('')

    def _handle_rm(self):
        from_todos = set()
        to_todos = set()

        for from_todo, to_todo in self._get_todos():
            self.todolist.remove_dependency(from_todo, to_todo)

            from_todos.add(from_todo)
            to_todos.add(to_todo)

        if from_todos and to_todos:
            if len(from_todos) == 1:
                following = 'item'
                depend = 'no longer depends'
            else:
                following = 'items'
                depend = 'no longer depend'

            item = 'item' if len(to_todos) == 1 else 'items'

            self.out('Following todo ' + following + ':')
            self.out(self.printer.print_list(from_todos))
            self.out(depend + ' on todo ' + item + ' below:')
            self.out(self.printer.print_list(to_todos))
        else:
            self.out('')

    def _get_todos(self):
        result = []

        def get_parent_dependencies():
            result = set()
            child_todos = first_todos
            sibling_todos = second_todos

            combinations = list(product(child_todos, sibling_todos))
            for child, sibling in combinations:
                result.update([(parent, child) for parent in self.todolist.parents(sibling)])

            return list(result)

        def get_child_dependencies():
            result = set()
            parent_todos = first_todos
            sibling_todos = second_todos

            combinations = list(product(parent_todos, sibling_todos))
            for parent, sibling in combinations:
                result.update([(parent, child) for child in self.todolist.children(sibling)])

            return list(result)

        def get_before_dependencies():
            return list(product(second_todos, first_todos))

        def get_after_dependencies():
            return list(product(first_todos, second_todos))

        actions = {
            'get_after_deps': get_after_dependencies,
            'get_before_deps': get_before_dependencies,
            'get_child_deps': get_child_dependencies,
            'get_parent_deps': get_parent_dependencies,
            'get_to': get_after_dependencies,
        }

        try:
            if len(self.args) == 3:
                first_todo_nrs = [self.argument(1)]
                action = "get_to"
                second_todo_nrs = [self.argument(2)]
            else:
                first_todo_nrs, second_todo_nrs, action = self._preprocess()

            first_todos = [self.todolist.todo(todo_nr) for todo_nr in first_todo_nrs]
            second_todos = [self.todolist.todo(todo_nr) for todo_nr in second_todo_nrs]

            result = actions[action]()
        except (InvalidTodoException):
            self.error("Invalid todo number given.")
        except InvalidCommandArgument:
            self.error(self.usage())

        return result

    def _handle_ls(self):
        """ Handles the ls subsubcommand. """

        def get_parents():
            parents = []
            for todo in todos:
                parents.append(self.todolist.parents(todo))

            intersection = set(parents[0]).intersection(*parents)
            return list(intersection)

        def get_children():
            children = []
            for todo in todos:
                children.append(self.todolist.children(todo))

            intersection = set(children[0]).intersection(*children)
            return list(intersection)

        def handle_to_operator():
            if self.argument(-1) == 'to':
                return get_children()
            else:
                return get_parents()

        actions = {
            'get_after_deps': get_parents,
            'get_before_deps': get_children,
            'get_child_deps': get_children,
            'get_parent_deps': get_parents,
            'get_to': handle_to_operator,
        }

        try:
            first_todo_nrs, second_todo_nrs, action = self._preprocess()

            if first_todo_nrs and second_todo_nrs:
                raise InvalidCommandArgument

            todo_nrs = second_todo_nrs or first_todo_nrs
            todos = [self.todolist.todo(todo_nr) for todo_nr in todo_nrs]

            result = actions[action]()

            sorter = Sorter(config().sort_string())
            instance_filter = Filter.InstanceFilter(result)
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
            todos = set()

            for todo_nr in self.args[1:]:
                todo = self.todolist.todo(todo_nr)

                todos |= {todo}
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
  dep ls <before|after> <NUMBER>
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
