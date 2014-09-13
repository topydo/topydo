import pdb
import unittest

import Sorter
import TodoList
import View

from TestFacilities import load_file, todolist_to_string, load_file_to_todolist

class SorterTest(unittest.TestCase):
    def sort_file(self,p_filename, p_filename_ref, p_sorter):
        """
        Sorts a file and compares it with a reference result.
        Also check that the sort algorithm hasn't touched the original data.
        """
        todos = load_file(p_filename)
        text_before = todolist_to_string(todos)
        todos_sorted = todolist_to_string(p_sorter.sort(todos))
        todos_ref = todolist_to_string(load_file(p_filename_ref))

        self.assertEquals(todos_sorted, todos_ref)
        self.assertEquals(todolist_to_string(todos), text_before)

    def test_sort1(self):
        """ Alphabetically sorted """
        sorter = Sorter.Sorter('text')
        self.sort_file('data/SorterTest1.txt', 'data/SorterTest1-result.txt', sorter)

    def test_sort2a(self):
        """
        Ascendingly sorted by priority. Also checks stableness of the sort.
        """
        sorter = Sorter.Sorter('prio')
        self.sort_file('data/SorterTest2.txt', 'data/SorterTest2-result.txt', sorter)

    def test_sort2b(self):
        """
        Ascendingly sorted by priority. Also checks stableness of the sort.
        """
        sorter = Sorter.Sorter('asc:prio')
        self.sort_file('data/SorterTest2.txt', 'data/SorterTest2-result.txt', sorter)

    def test_sort3(self):
        """
        Descendingly sorted by priority. Also checks stableness of the
        sort.
        """
        sorter = Sorter.Sorter('desc:prio')
        self.sort_file('data/SorterTest3.txt', 'data/SorterTest3-result.txt', sorter)

    def test_sort4(self):
        """ Ascendingly sorted by due date """
        sorter = Sorter.Sorter('due')
        self.sort_file('data/SorterTest4.txt', 'data/SorterTest4-result.txt', sorter)

    def test_sort5(self):
        """ Descendingly sorted by due date """
        sorter = Sorter.Sorter('desc:due')
        self.sort_file('data/SorterTest5.txt', 'data/SorterTest5-result.txt', sorter)

    def test_sort6(self):
        """ Ascendingly sorted by creation date """
        sorter = Sorter.Sorter('creation')
        self.sort_file('data/SorterTest6.txt', 'data/SorterTest6-result.txt', sorter)

    def test_sort7(self):
        """ Ascendingly sorted by completion date. """
        sorter = Sorter.Sorter('completion')
        self.sort_file('data/SorterTest7.txt', 'data/SorterTest7-result.txt', sorter)

    def test_sort8(self):
        """ Descendingly sorted by importance """
        sorter = Sorter.Sorter('desc:importance')
        self.sort_file('data/SorterTest8.txt', 'data/SorterTest8-result.txt', sorter)

    def test_sort9(self):
        """
        Sort on multiple levels: first descending importance, then
        ascending priority.
        """
        sorter = Sorter.Sorter('desc:importance,priority')
        self.sort_file('data/SorterTest9.txt', 'data/SorterTest9-result.txt', sorter)

    def test_sort10(self):
        """ Deal with garbage input. """
        sorter = Sorter.Sorter('')
        self.sort_file('data/SorterTest9.txt', 'data/SorterTest9.txt', sorter)

    def test_sort11(self):
        """ Deal with garbage input. """
        sorter = Sorter.Sorter('fnord')
        self.sort_file('data/SorterTest9.txt', 'data/SorterTest9.txt', sorter)

    def test_sort12(self):
        """
        Descendingly sorted by average importance.

        Reusing input and output for normal importance test, since without
        dependencies the average importance should be equal.
        """
        sorter = Sorter.Sorter('desc:importance-avg')
        self.sort_file('data/SorterTest9.txt', 'data/SorterTest9-result.txt', sorter)

    def test_sort13(self):
        sorter = Sorter.Sorter('desc:importance-average')

        pdb.set_trace()
        todolist = load_file_to_todolist('data/SorterTest10.txt')
        view = todolist.view(sorter, [])
        result = load_file('data/SorterTest10-result.txt')

        self.assertEquals(str(view), todolist_to_string(result))

    def test_sort14(self):
        """
        Test that own importance is used when average turns out to be
        lower.
        """
        sorter = Sorter.Sorter('desc:importance-average')

        pdb.set_trace()
        todolist = load_file_to_todolist('data/SorterTest11.txt')
        view = todolist.view(sorter, [])
        result = load_file('data/SorterTest11-result.txt')

        self.assertEquals(str(view), todolist_to_string(result))

