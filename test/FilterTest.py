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

""" Tests for the filter functionality. """

import unittest

import Filter
from TestFacilities import *
import Todo
import TodoList

class FilterTest(unittest.TestCase):
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

    def test_filter7(self):
        """ Tests the dependency filter. """
        todolist = load_file_to_todolist('data/FilterTest2.txt')
        depfilter = Filter.DependencyFilter(todolist)

        filtered_todos = depfilter.filter(todolist.todos())
        reference = load_file('data/FilterTest2-result.txt')

        self.assertEquals(todolist_to_string(filtered_todos), \
            todolist_to_string(reference))

    def test_filter8(self):
        """ Test case sensitive match (forced, with lowercase). """
        todos = load_file('data/FilterTest1.txt')
        grep = Filter.GrepFilter('+Project', False)

        filtered_todos = grep.filter(todos)
        reference = load_file('data/FilterTest1a-result.txt')

        self.assertEquals(todolist_to_string(filtered_todos), \
            todolist_to_string(reference))

    def test_filter9(self):
        """ Test instance filter """
        todos = load_file('data/FilterTest1.txt')
        instance_filter = Filter.InstanceFilter(todos[2:])

        filtered_todos = instance_filter.filter(todos)

        self.assertEquals(todos[2:], filtered_todos)

    def test_filter10(self):
        """ Test instance filter """
        todos = load_file('data/FilterTest1.txt')
        instance_filter = Filter.InstanceFilter([])

        filtered_todos = instance_filter.filter(todos)

        self.assertEquals([], filtered_todos)

    def test_filter11(self):
        """ Test instance filter """
        todos = load_file('data/FilterTest1.txt')
        instance_filter = Filter.InstanceFilter(todos[2:])

        filtered_todos = instance_filter.filter([])

        self.assertEquals([], filtered_todos)

    def test_filter12(self):
        """ Test limit filter. """
        todos = load_file('data/FilterTest1.txt')
        limit_filter = Filter.LimitFilter(0)

        filtered_todos = limit_filter.filter(todos)

        self.assertEquals([], filtered_todos)

    def test_filter13(self):
        """ Test limit filter. """
        todos = load_file('data/FilterTest1.txt')
        limit_filter = Filter.LimitFilter(1)

        filtered_todos = limit_filter.filter(todos)

        self.assertEquals(len(filtered_todos), 1)
        self.assertEquals(filtered_todos[0].source(), '(C) This is part of some +Project')

    def test_filter14(self):
        """ Test limit filter. """
        todos = load_file('data/FilterTest1.txt')
        limit_filter = Filter.LimitFilter(-1)

        filtered_todos = limit_filter.filter(todos)

        self.assertEquals(todos, filtered_todos)

    def test_filter15(self):
        """ Test limit filter. """
        todos = load_file('data/FilterTest1.txt')
        limit_filter = Filter.LimitFilter(100)

        filtered_todos = limit_filter.filter(todos)

        self.assertEquals(len(filtered_todos), 4)

    def test_filter16(self):
        todos = load_file('data/FilterTest1.txt')
        grep = Filter.NegationFilter(Filter.GrepFilter('+project'))

        filtered_todos = grep.filter(todos)
        reference = load_file('data/FilterTest3-result.txt')

        self.assertEquals(todolist_to_string(filtered_todos), \
            todolist_to_string(reference))

    def test_filter17(self):
        todos = load_file('data/FilterTest1.txt')
        grep1 = Filter.GrepFilter('task')
        grep2 = Filter.GrepFilter('project')
        andfilter = Filter.AndFilter(grep1, grep2)

        filtered_todos = andfilter.filter(todos)
        reference = load_file('data/FilterTest4-result.txt')

        self.assertEquals(todolist_to_string(filtered_todos), \
            todolist_to_string(reference))

    def test_filter18(self):
        todos = load_file('data/FilterTest1.txt')
        grep1 = Filter.GrepFilter('part')
        grep2 = Filter.GrepFilter('important')
        grep = Filter.OrFilter(grep1, grep2)

        filtered_todos = grep.filter(todos)
        reference = load_file('data/FilterTest5-result.txt')

        self.assertEquals(todolist_to_string(filtered_todos), \
            todolist_to_string(reference))

    def test_filter19(self):
        todos = load_file('data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('due:<2014-11-10')

        filtered_todos = otf.filter(todos)
        reference = load_file('data/FilterTest6-result.txt')

        self.assertEquals(todolist_to_string(filtered_todos), \
            todolist_to_string(reference))
        
    def test_filter20(self):
        todos = load_file('data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('due:=2014-11-10')

        filtered_todos = otf.filter(todos)
        reference = load_file('data/FilterTest6-result.txt')

        self.assertEquals(todolist_to_string(filtered_todos), "")
        
    def test_filter21(self):
        todos = load_file('data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('due:=2014-11-10')

        filtered_todos = otf.filter(todos)

        self.assertEquals(todolist_to_string(filtered_todos), "")
        
    def test_filter22(self):
        todos = load_file('data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('due:=2014-11-99')

        filtered_todos = otf.filter(todos)

        self.assertEquals(todolist_to_string(filtered_todos), "")

    def test_filter23(self):
        todos = load_file('data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('due:=garbage')

        filtered_todos = otf.filter(todos)

        self.assertEquals(todolist_to_string(filtered_todos), "")

    def test_filter24(self):
        todos = load_file('data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('value:<10')

        filtered_todos = otf.filter(todos)
        reference = load_file('data/FilterTest8-result.txt')

        self.assertEquals(todolist_to_string(filtered_todos),
            todolist_to_string(reference))

    def test_filter25(self):
        todos = load_file('data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('value:<=16')

        filtered_todos = otf.filter(todos)
        reference = load_file('data/FilterTest9-result.txt')

        self.assertEquals(todolist_to_string(filtered_todos),
            todolist_to_string(reference))

    def test_filter26(self):
        todos = load_file('data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('value:<16')

        filtered_todos = otf.filter(todos)
        reference = load_file('data/FilterTest10-result.txt')

        self.assertEquals(todolist_to_string(filtered_todos),
            todolist_to_string(reference))

    def test_filter27(self):
        todos = load_file('data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('value:<16a')

        filtered_todos = otf.filter(todos)

        self.assertEquals(todolist_to_string(filtered_todos), "")

    def test_filter28(self):
        todos = load_file('data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('value:>8')

        filtered_todos = otf.filter(todos)
        reference = load_file('data/FilterTest11-result.txt')

        self.assertEquals(todolist_to_string(filtered_todos),
            todolist_to_string(reference))

    def test_filter29(self):
        todos = load_file('data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('value:>=8')

        filtered_todos = otf.filter(todos)
        reference = load_file('data/FilterTest12-result.txt')

        self.assertEquals(todolist_to_string(filtered_todos),
            todolist_to_string(reference))
