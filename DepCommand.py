import Command
import Config
import Sorter
from Utils import convert_todo_number
import View

class DepCommand(Command.Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(DepCommand, self).__init__(p_args, p_todolist, p_out, p_err, p_prompt)
        self.subsubcommand = self.argument(0)

    def _handle_add(self):
        (from_todo, to_todo) = self._get_todo_numbers()
        self.todolist.add_dependency(from_todo, to_todo)

    def _handle_rm(self):
        (from_todo, to_todo) = self._get_todo_numbers()
        self.todolist.remove_dependency(from_todo, to_todo)

    def _get_todo_numbers(self):
        from_todonumber = convert_todo_number(self.argument(1))
        to_todonumber = self.argument(2)

        if to_todonumber == 'to':
            to_todonumber = convert_todo_number(self.argument(3))
        else:
            to_todonumber = convert_todo_number(to_todonumber)

        return (from_todonumber, to_todonumber)

    def _handle_ls(self):
        """ Handles the ls subsubcommand. """
        arg1 = self.argument(1)
        arg2 = self.argument(2)

        todos = []
        if arg2 == 'to':
            # dep ls 1 to ...
            todos = self.todolist.children(convert_todo_number(arg1))
        elif arg1 == 'to':
            # dep ls ... to 1
            todos = self.todolist.parents(convert_todo_number(arg2))
        else:
            self.errors.append(self.usage())

        if todos:
            sorter = Sorter.Sorter(Config.SORT_STRING)
            view = View.View(sorter, [], todos)
            self.out(view.pretty_print())

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

