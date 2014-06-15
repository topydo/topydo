import unittest

import Filter
import Sorter
from TestFacilities import load_file, todolist_to_string
import TodoFile
import TodoList

class ViewTest(unittest.TestCase):
    def test_view(self):
        """ Check filters and printer for views. """
        todofile = TodoFile.TodoFile('data/FilterTest1.txt')
        ref = load_file('data/ViewTest1-result.txt')

        todolist = TodoList.TodoList(todofile.read())
        sorter = Sorter.Sorter('text')
        todofilter = Filter.GrepFilter('+Project')
        view = todolist.view(sorter, [todofilter])

        self.assertEquals(str(view), todolist_to_string(ref))

