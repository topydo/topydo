from PrettyPrinter import pretty_print

class View:
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
        return '\n'.join(pretty_print(self._todos, True, True))

    def __str__(self):
        return '\n'.join(pretty_print(self._todos))
