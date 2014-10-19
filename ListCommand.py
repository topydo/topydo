import Command
import Config
import Filter
import Sorter

class ListCommand(Command.Command):
    def __init__(self, p_args, p_todolist,
                 p_out=lambda a: None,
                 p_err=lambda a: None,
                 p_prompt=lambda a: None):
        super(ListCommand, self).__init__(p_args, p_todolist, p_out, p_err, p_prompt)

    def execute(self):
        show_all = self.argumentShift("-x")

        sorter = Sorter.Sorter(Config.SORT_STRING)
        filters = [] if show_all else [Filter.DependencyFilter(self.todolist), Filter.RelevanceFilter()]

        if len(self.args) > 0:
            filters.append(Filter.GrepFilter(self.argument(0)))

        self.out(self.todolist.view(sorter, filters).pretty_print())
