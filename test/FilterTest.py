""" Tests for the filter functionality. """

import datetime
import unittest

import Filter
from TestFacilities import load_file, todolist_to_string
import Todo

class FilterTest(unittest.TestCase):
    def setUp(self):
        # self.today = datetime.date.today()
        pass

    def test_filter1(self):
        todo = Todo.Todo("(C) Relevant")
        relevance = Filter.RelevanceFilter()
        result = relevance.filter([todo], 0)

        self.assertEquals(result, [])

    def test_filter2(self):
        todo = Todo.Todo("(C) Relevant")
        relevance = Filter.RelevanceFilter()
        result = relevance.filter([todo], 100)

        self.assertEquals(result, [todo])

    def test_filter3(self):
        todo = Todo.Todo("(C) Relevant")
        relevance = Filter.RelevanceFilter()
        result = relevance.filter([todo])

        self.assertEquals(result, [todo])

    def test_filter4(self):
        """ Test case insensitive match. """
        todos = load_file('data/FilterTest1.txt')
        grep = Filter.GrepFilter('+project')

        filtered_todos = grep.filter(todos)
        reference = load_file('data/FilterTest1a-result.txt')

        self.assertEquals(todolist_to_string(filtered_todos), \
            todolist_to_string(reference))

    def test_filter5(self):
        """ Test case sensitive match. """
        todos = load_file('data/FilterTest1.txt')
        grep = Filter.GrepFilter('+Project')

        filtered_todos = grep.filter(todos)
        reference = load_file('data/FilterTest1b-result.txt')

        self.assertEquals(todolist_to_string(filtered_todos), \
            todolist_to_string(reference))

    def test_filter6(self):
        """ Test case sensitive match (forced, with lowercase). """
        todos = load_file('data/FilterTest1.txt')
        grep = Filter.GrepFilter('+project', True)

        filtered_todos = grep.filter(todos)
        reference = load_file('data/FilterTest1c-result.txt')

        self.assertEquals(todolist_to_string(filtered_todos), \
            todolist_to_string(reference))
