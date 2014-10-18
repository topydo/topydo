from Command import *
import Config
import Filter
import Sorter
import TodoList
from Utils import convert_todo_number, InvalidTodoNumberException
import View

class DepCommand(Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(DepCommand, self).__init__(p_args, p_todolist, p_out, p_err, p_prompt)
        self.subsubcommand = self.argument(0)

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
            from_todo_nr = convert_todo_number(self.argument(1))
            to_todo_nr = self.argument(2)

            if to_todo_nr == 'to':
                to_todo_nr = convert_todo_number(self.argument(3))
            else:
                to_todo_nr = convert_todo_number(to_todo_nr)

            from_todo = self.todolist.todo(from_todo_nr)
            to_todo = self.todolist.todo(to_todo_nr)
        except (InvalidTodoNumberException, TodoList.InvalidTodoException):
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
                number = convert_todo_number(arg1)
                todo = self.todolist.todo(number)
                todos = self.todolist.children(todo)
            elif arg1 == 'to':
                # dep ls ... to 1
                number = convert_todo_number(arg2)
                todo = self.todolist.todo(number)
                todos = self.todolist.parents(todo)
            else:
                self.error(self.usage())

            if todos:
                sorter = Sorter.Sorter(Config.SORT_STRING)
                instance_filter = Filter.InstanceFilter(todos)
                view = View.View(sorter, [instance_filter], self.todolist)
                self.out(view.pretty_print())
        except (TodoList.InvalidTodoException, InvalidTodoNumberException):
            self.error("Invalid todo number given.")
        except InvalidCommandArgument:
            self.error(self.usage())

    def execute(self):
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

