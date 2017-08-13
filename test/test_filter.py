# Topydo - A todo.txt client written in Python.
# Copyright (C) 2014 - 2015 Bram Schoenmakers <bram@topydo.org>
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
from datetime import date, timedelta

from topydo.lib import Filter
from topydo.lib.Todo import Todo

from .facilities import load_file, load_file_to_todolist, todolist_to_string
from .topydo_testcase import TopydoTest


class FilterTest(TopydoTest):
    def test_filter03(self):
        todo = Todo("(C) Relevant")
        relevance = Filter.RelevanceFilter()
        result = relevance.filter([todo])

        self.assertEqual(result, [todo])

    def test_filter04(self):
        """ Test case insensitive match. """
        todos = load_file('test/data/FilterTest1.txt')
        grep = Filter.GrepFilter('+project')

        filtered_todos = grep.filter(todos)
        reference = load_file('test/data/FilterTest1a-result.txt')

        self.assertEqual(todolist_to_string(filtered_todos),
                         todolist_to_string(reference))

    def test_filter05(self):
        """ Test case sensitive match. """
        todos = load_file('test/data/FilterTest1.txt')
        grep = Filter.GrepFilter('+Project')

        filtered_todos = grep.filter(todos)
        reference = load_file('test/data/FilterTest1b-result.txt')

        self.assertEqual(todolist_to_string(filtered_todos),
                         todolist_to_string(reference))

    def test_filter06(self):
        """ Test case sensitive match (forced, with lowercase). """
        todos = load_file('test/data/FilterTest1.txt')
        grep = Filter.GrepFilter('+project', True)

        filtered_todos = grep.filter(todos)
        reference = load_file('test/data/FilterTest1c-result.txt')

        self.assertEqual(todolist_to_string(filtered_todos),
                         todolist_to_string(reference))

    def test_filter07(self):
        """ Tests the dependency filter. """
        todolist = load_file_to_todolist('test/data/FilterTest2.txt')
        depfilter = Filter.DependencyFilter(todolist)

        filtered_todos = depfilter.filter(todolist.todos())
        reference = load_file('test/data/FilterTest2-result.txt')

        self.assertEqual(todolist_to_string(filtered_todos),
                         todolist_to_string(reference))

    def test_filter08(self):
        """ Test case sensitive match (forced, with lowercase). """
        todos = load_file('test/data/FilterTest1.txt')
        grep = Filter.GrepFilter('+Project', False)

        filtered_todos = grep.filter(todos)
        reference = load_file('test/data/FilterTest1a-result.txt')

        self.assertEqual(todolist_to_string(filtered_todos),
                         todolist_to_string(reference))

    def test_filter09(self):
        """ Test instance filter. """
        todos = load_file('test/data/FilterTest1.txt')
        instance_filter = Filter.InstanceFilter(todos[2:])

        filtered_todos = instance_filter.filter(todos)

        self.assertEqual(todos[2:], filtered_todos)

    def test_filter10(self):
        """ Test instance filter. """
        todos = load_file('test/data/FilterTest1.txt')
        instance_filter = Filter.InstanceFilter([])

        filtered_todos = instance_filter.filter(todos)

        self.assertEqual([], filtered_todos)

    def test_filter11(self):
        """ Test instance filter. """
        todos = load_file('test/data/FilterTest1.txt')
        instance_filter = Filter.InstanceFilter(todos[2:])

        filtered_todos = instance_filter.filter([])

        self.assertEqual([], filtered_todos)

    def test_filter12(self):
        """ Test limit filter. """
        todos = load_file('test/data/FilterTest1.txt')
        limit_filter = Filter.LimitFilter(0)

        filtered_todos = limit_filter.filter(todos)

        self.assertEqual([], filtered_todos)

    def test_filter13(self):
        """ Test limit filter. """
        todos = load_file('test/data/FilterTest1.txt')
        limit_filter = Filter.LimitFilter(1)

        filtered_todos = limit_filter.filter(todos)

        self.assertEqual(len(filtered_todos), 1)
        self.assertEqual(filtered_todos[0].source(),
                         '(C) This is part of some +Project')

    def test_filter14(self):
        """ Test limit filter. """
        todos = load_file('test/data/FilterTest1.txt')
        limit_filter = Filter.LimitFilter(-1)

        filtered_todos = limit_filter.filter(todos)

        self.assertEqual(todos, filtered_todos)

    def test_filter15(self):
        """ Test limit filter. """
        todos = load_file('test/data/FilterTest1.txt')
        limit_filter = Filter.LimitFilter(100)

        filtered_todos = limit_filter.filter(todos)

        self.assertEqual(len(filtered_todos), 4)

    def test_filter16(self):
        todos = load_file('test/data/FilterTest1.txt')
        grep = Filter.NegationFilter(Filter.GrepFilter('+project'))

        filtered_todos = grep.filter(todos)
        reference = load_file('test/data/FilterTest3-result.txt')

        self.assertEqual(todolist_to_string(filtered_todos),
                         todolist_to_string(reference))

    def test_filter17(self):
        todos = load_file('test/data/FilterTest1.txt')
        grep1 = Filter.GrepFilter('task')
        grep2 = Filter.GrepFilter('project')
        andfilter = Filter.AndFilter(grep1, grep2)

        filtered_todos = andfilter.filter(todos)
        reference = load_file('test/data/FilterTest4-result.txt')

        self.assertEqual(todolist_to_string(filtered_todos),
                         todolist_to_string(reference))

    def test_filter18(self):
        todos = load_file('test/data/FilterTest1.txt')
        grep1 = Filter.GrepFilter('part')
        grep2 = Filter.GrepFilter('important')
        grep = Filter.OrFilter(grep1, grep2)

        filtered_todos = grep.filter(todos)
        reference = load_file('test/data/FilterTest5-result.txt')

        self.assertEqual(todolist_to_string(filtered_todos),
                         todolist_to_string(reference))

    def test_filter20(self):
        todos = load_file('test/data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('due:<2014-11-10')

        filtered_todos = otf.filter(todos)
        reference = load_file('test/data/FilterTest6-result.txt')

        self.assertEqual(todolist_to_string(filtered_todos),
                         todolist_to_string(reference))

    def test_filter21(self):
        todos = load_file('test/data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('due:=2014-11-10')

        filtered_todos = otf.filter(todos)

        self.assertEqual(todolist_to_string(filtered_todos), "")

    def test_filter22(self):
        todos = load_file('test/data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('due:=2014-11-10')

        filtered_todos = otf.filter(todos)

        self.assertEqual(todolist_to_string(filtered_todos), "")

    def test_filter23(self):
        todos = load_file('test/data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('due:=2014-11-99')

        filtered_todos = otf.filter(todos)

        self.assertEqual(todolist_to_string(filtered_todos), "")

    def test_filter24(self):
        todos = load_file('test/data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('due:=garbage')

        filtered_todos = otf.filter(todos)

        self.assertEqual(todolist_to_string(filtered_todos), "")

    def test_filter25(self):
        todos = load_file('test/data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('value:<10')

        filtered_todos = otf.filter(todos)
        reference = load_file('test/data/FilterTest8-result.txt')

        self.assertEqual(todolist_to_string(filtered_todos),
                         todolist_to_string(reference))

    def test_filter26(self):
        todos = load_file('test/data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('value:<=16')

        filtered_todos = otf.filter(todos)
        reference = load_file('test/data/FilterTest9-result.txt')

        self.assertEqual(todolist_to_string(filtered_todos),
                         todolist_to_string(reference))

    def test_filter27(self):
        todos = load_file('test/data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('value:<16')

        filtered_todos = otf.filter(todos)
        reference = load_file('test/data/FilterTest10-result.txt')

        self.assertEqual(todolist_to_string(filtered_todos),
                         todolist_to_string(reference))

    def test_filter28(self):
        todos = load_file('test/data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('value:<16a')

        filtered_todos = otf.filter(todos)

        self.assertEqual(todolist_to_string(filtered_todos), "")

    def test_filter29(self):
        todos = load_file('test/data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('value:>8')

        filtered_todos = otf.filter(todos)
        reference = load_file('test/data/FilterTest11-result.txt')

        self.assertEqual(todolist_to_string(filtered_todos),
                         todolist_to_string(reference))

    def test_filter30(self):
        todos = load_file('test/data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('value:>=8')

        filtered_todos = otf.filter(todos)
        reference = load_file('test/data/FilterTest12-result.txt')

        self.assertEqual(todolist_to_string(filtered_todos),
                         todolist_to_string(reference))

    def test_filter31(self):
        todos = load_file('test/data/FilterTest3.txt')
        otf = Filter.OrdinalTagFilter('value:>-8')

        filtered_todos = otf.filter(todos)
        reference = load_file('test/data/FilterTest13-result.txt')

        self.assertEqual(todolist_to_string(filtered_todos),
                         todolist_to_string(reference))


class OrdinalTagFilterTest(TopydoTest):
    def setUp(self):
        super().setUp()

        today = date.today()
        tomorrow = today + timedelta(1)

        self.today = today.isoformat()
        self.tomorrow = tomorrow.isoformat()

        self.todo1 = "Foo due:{}".format(self.today)
        self.todo2 = "Bar due:{}".format(self.tomorrow)
        self.todo3 = "Baz due:Nonsense"
        self.todo4 = "Fnord due:2014-10-32"
        self.todo5 = "Double tags key:value1 key:value2"

        self.todos = [
            Todo(self.todo1),
            Todo(self.todo2),
            Todo(self.todo3),
            Todo(self.todo4),
            Todo(self.todo5),
        ]

    def test_filter1(self):
        otf = Filter.OrdinalTagFilter('due:today')

        result = otf.filter(self.todos)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source(), self.todo1)

    def test_filter2(self):
        otf = Filter.OrdinalTagFilter('due:=today')

        result = otf.filter(self.todos)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source(), self.todo1)

    def test_filter3(self):
        otf = Filter.OrdinalTagFilter('due:>today')

        result = otf.filter(self.todos)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source(), self.todo2)

    def test_filter4(self):
        otf = Filter.OrdinalTagFilter('due:<1w')

        result = otf.filter(self.todos)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].source(), self.todo1)
        self.assertEqual(result[1].source(), self.todo2)

    def test_filter5(self):
        otf = Filter.OrdinalTagFilter('due:!today')

        result = otf.filter(self.todos)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source(), self.todo2)

    def test_filter6(self):
        otf = Filter.OrdinalTagFilter('due:non')

        result = otf.filter(self.todos)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source(), self.todo3)

    def test_filter7(self):
        otf = Filter.OrdinalTagFilter('due:Non')

        result = otf.filter(self.todos)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source(), self.todo3)

    def test_filter8(self):
        """
        OrdinalTagFilter should resort to a simple GrepFilter when a tag
        appears more than once.
        """
        otf = Filter.OrdinalTagFilter('key:value2')

        result = otf.filter(self.todos)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source(), self.todo5)


class CreationFilterTest(TopydoTest):
    def setUp(self):
        super().setUp()

        self.todo1 = "2015-12-19 With creation date."
        self.todo2 = "Without creation date."

        self.todos = [Todo(self.todo1), Todo(self.todo2)]

    def test_filter1(self):
        cf = Filter.CreationFilter('create:2015-12-19')

        result = cf.filter(self.todos)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source(), self.todo1)

    def test_filter2(self):
        cf = Filter.CreationFilter('creation:2015-12-19')

        result = cf.filter(self.todos)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source(), self.todo1)

    def test_filter3(self):
        cf = Filter.CreationFilter('created:2015-12-19')

        result = cf.filter(self.todos)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source(), self.todo1)


class CompletionFilterTest(TopydoTest):
    def setUp(self):
        super().setUp()

        self.todo1 = "2015-12-19 With creation date."
        self.todo2 = "x 2015-12-19 2015-12-18 Without creation date."
        self.todo3 = "x 2015-12-18 Without creation date."

        self.todos = [Todo(self.todo1), Todo(self.todo2), Todo(self.todo3)]

    def test_filter1(self):
        cf = Filter.CompletionFilter('complete:2015-12-19')

        result = cf.filter(self.todos)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source(), self.todo2)

    def test_filter2(self):
        cf = Filter.CompletionFilter('completed:2015-12-19')

        result = cf.filter(self.todos)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source(), self.todo2)

    def test_filter3(self):
        cf = Filter.CompletionFilter('completion:2015-12-19')

        result = cf.filter(self.todos)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source(), self.todo2)

    def test_filter4(self):
        cf = Filter.CompletionFilter('completion:<=2015-12-19')

        result = cf.filter(self.todos)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].source(), self.todo2)
        self.assertEqual(result[1].source(), self.todo3)


class PriorityFilterTest(TopydoTest):
    def setUp(self):
        super().setUp()

        self.todo1 = "(A) Foo"
        self.todo2 = "(B) Bar"
        self.todo3 = "(C) Baz"
        self.todo4 = "(Z) FooBar"
        self.todo5 = "FooBaz"

        self.todos = [
            Todo(self.todo1),
            Todo(self.todo2),
            Todo(self.todo3),
            Todo(self.todo4),
            Todo(self.todo5),
        ]

    def test_filter1(self):
        pf = Filter.PriorityFilter('(A)')

        result = pf.filter(self.todos)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source(), self.todo1)

    def test_filter1a(self):
        pf = Filter.PriorityFilter('(=A)')

        result = pf.filter(self.todos)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source(), self.todo1)

    def test_filter2(self):
        pf = Filter.PriorityFilter('(>B)')

        result = pf.filter(self.todos)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source(), self.todo1)

    def test_filter3(self):
        pf = Filter.PriorityFilter('(>=C)')

        result = pf.filter(self.todos)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].source(), self.todo1)
        self.assertEqual(result[1].source(), self.todo2)
        self.assertEqual(result[2].source(), self.todo3)

    def test_filter4(self):
        pf = Filter.PriorityFilter('(<A)')

        result = pf.filter(self.todos)

        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].source(), self.todo2)
        self.assertEqual(result[1].source(), self.todo3)
        self.assertEqual(result[2].source(), self.todo4)
        self.assertEqual(result[3].source(), self.todo5)

    def test_filter5(self):
        pf = Filter.PriorityFilter('(<=C)')

        result = pf.filter(self.todos)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].source(), self.todo3)
        self.assertEqual(result[1].source(), self.todo4)
        self.assertEqual(result[2].source(), self.todo5)

    def test_filter6(self):
        pf = Filter.PriorityFilter('(!B)')

        result = pf.filter(self.todos)

        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].source(), self.todo1)
        self.assertEqual(result[1].source(), self.todo3)
        self.assertEqual(result[2].source(), self.todo4)
        self.assertEqual(result[3].source(), self.todo5)

    def test_filter7(self):
        pf = Filter.PriorityFilter('(>A)')

        result = pf.filter(self.todos)

        self.assertEqual(len(result), 0)

    def test_filter8(self):
        pf = Filter.PriorityFilter('(<Z)')

        result = pf.filter(self.todos)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source(), self.todo5)

if __name__ == '__main__':
    unittest.main()
