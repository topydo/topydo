""" A view is a list of todos, sorted and filtered. """

from PrettyPrinter import *

class View(object):
    """
    A view is instantiated by a todo list, usually obtained from a todo.txt
    file. Also a sorter and a list of filters should be given that is applied
    to the list.
    """
    def __init__(self, p_sorter, p_filters, p_todos):
        self._todos = p_todos
        self._viewdata = []
        self._sorter = p_sorter
        self._filters = p_filters

        self.update()

    def update(self):
        """
        Updates the view data. Should be called when the backing todo list
        has changed.
        """
        self._viewdata = self._sorter.sort(self._todos)

        for _filter in self._filters:
            self._viewdata = _filter.filter(self._viewdata)

    def pretty_print(self):
        """ Pretty prints the view. """
        return '\n'.join(pretty_print(self._viewdata, [pp_number, pp_color]))

    def __str__(self):
        return '\n'.join(pretty_print(self._viewdata))
