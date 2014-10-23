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

from Command import *
import TodoList
from PrettyPrinter import pretty_print
from Utils import convert_todo_number, InvalidTodoNumberException

class TagCommand(Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(TagCommand, self).__init__(p_args, p_todolist, p_out, p_err, p_prompt)

        self.subsubcommand = None
        self.todo = None
        self.tag = None
        self.value = None
        self.values = []

        try:
            self.subsubcommand = self.argument(0)
            number = convert_todo_number(self.argument(1))
            self.todo = self.todolist.todo(number)
            self.tag = self.argument(2)
            self.current_values = self.todo.tag_values(self.tag)
            self.value = self.argument(3)
        except (InvalidCommandArgument, InvalidTodoNumberException, TodoList.InvalidTodoException):
            pass

    def _print(self):
        self.out(pretty_print(self.todo, [self.todolist.pp_number()]))

    def _choose(self):
        """
        Returns the chosen number of the tag value to process (or "all")
        """
        for i, value in enumerate(self.current_values):
            self.out("%2d. %s" % (i + 1, value))

        answer = self.prompt('Which value to remove? Enter number or "all": ')

        if answer != "all":
            try:
                answer = int(answer) - 1
                
                if answer < 0 or answer >= len(self.current_values):
                    answer = None
            except ValueError:
                answer = None

        return answer

    def _add(self):
        self._set(True)

    def _set_helper(self, p_force, p_old_value=""):
        old_src = self.todo.source()
        self.todo.set_tag(self.tag, self.value, p_force, p_old_value)

        if old_src != self.todo.source():
            self.todolist.set_dirty()

    def _set(self, p_force_add=False):
        if self.value == None:
            self.error("Missing value for tag.")
            self.error(self.usage())
        else:
            if len(self.current_values) > 1:
                answer = self._choose()

                if answer == "all":
                    for value in self.current_values:
                        self._set_helper(False, value)
                elif answer != None and self.value != self.current_values[answer]:
                    self._set_helper(False, self.current_values[answer])

            else: # if not self.todo.has_tag(self.tag, self.value):
                self._set_helper(p_force_add)

            self._print()

    def _rm(self):
        self.value = ""
        self._set()

    def execute(self):
        if not super(TagCommand, self).execute():
            return False

        dispatch = {
            "add": self._add,
            "set": self._set,
            "del": self._rm,
            "rm":  self._rm,
        }

        if self.subsubcommand in dispatch and self.todo and self.tag:
            dispatch[self.subsubcommand]()
        elif self.subsubcommand not in dispatch:
            self.error(self.usage())
        elif not self.todo:
            self.error("Invalid todo number.")

    def usage(self):
        return """Synopsis: 
  tag (add|set) <NUMBER> <tag> <value>
  tag rm <NUMBER> <tag> [value]"""

    def help(self):
        return """* add: Add a tag to the given todo.
* set: Changes a tag of the given todo.
* rm: Removes a tag from the given todo."""
