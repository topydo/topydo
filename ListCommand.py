import Command
import Config
import Filter
import Sorter

class ListCommand(Command.Command):
    def __init__(self, p_args, p_todolist):
        super(ListCommand, self).__init__(p_args, p_todolist)

    def execute(self):
        sorter = Sorter.Sorter(Config.SORT_STRING)
        filters = [Filter.DependencyFilter(self.todolist),
                   Filter.RelevanceFilter()]

        if len(self.args) > 0:
            filters.append(Filter.GrepFilter(self.argument(0)))

        print self.todolist.view(sorter, filters).pretty_print() # FIXME

        return True
