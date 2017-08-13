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

import unittest

from topydo.lib.Graph import DirectedGraph

from .topydo_testcase import TopydoTest


class GraphTest(TopydoTest):
    def setUp(self):
        super().setUp()

        self.graph = DirectedGraph()

        self.graph.add_edge(1, 2, 1)
        self.graph.add_edge(2, 4, "Test")
        self.graph.add_edge(4, 3)
        self.graph.add_edge(4, 6)
        self.graph.add_edge(6, 2)
        self.graph.add_edge(1, 3)
        self.graph.add_edge(3, 5)

        #         1
        #       /   \
        #      v     v
        #    />2   />3
        #   /  |  /  |
        #  /   v /   v
        # 6 <- 4     5

    def test_has_nodes(self):
        for i in range(1, 7):
            self.assertTrue(self.graph.has_node(i))

    def test_has_edge_ids(self):
        self.assertTrue(self.graph.has_edge_id(1))
        self.assertTrue(self.graph.has_edge_id("Test"))
        self.assertFalse(self.graph.has_edge_id("1"))

    def test_incoming_neighbors1(self):
        self.assertEqual(self.graph.incoming_neighbors(1), set())

    def test_edge_id_of_nonexistent_edge(self):
        self.assertFalse(self.graph.edge_id(1, 6))

    def test_incoming_neighbors2(self):
        self.assertEqual(self.graph.incoming_neighbors(2), set([1, 6]))

    def test_incoming_neighbors3(self):
        self.assertEqual(self.graph.incoming_neighbors(1, True), set())

    def test_incoming_neighbors4(self):
        self.assertEqual(self.graph.incoming_neighbors(5, True),
                         set([1, 2, 3, 4, 6]))

    def test_outgoing_neighbors1(self):
        self.assertEqual(self.graph.outgoing_neighbors(1), set([2, 3]))

    def test_outgoing_neighbors2(self):
        self.assertEqual(self.graph.outgoing_neighbors(2), set([4]))

    def test_outgoing_neighbors3(self):
        self.assertEqual(self.graph.outgoing_neighbors(1, True),
                         set([2, 3, 4, 5, 6]))

    def test_outgoing_neighbors4(self):
        self.assertEqual(self.graph.outgoing_neighbors(3), set([5]))

    def test_outgoing_neighbors5(self):
        self.assertEqual(self.graph.outgoing_neighbors(5), set([]))

    def test_remove_edge1(self):
        self.graph.remove_edge(1, 2)

        self.assertFalse(self.graph.has_path(1, 4))
        self.assertTrue(self.graph.has_path(2, 4))
        self.assertFalse(self.graph.has_edge_id(1))

    def test_remove_edge2(self):
        self.graph.remove_edge(3, 5, True)

        self.assertFalse(self.graph.has_path(1, 5))
        self.assertFalse(self.graph.has_node(5))

    def test_remove_edge3(self):
        self.graph.remove_edge(3, 5, False)

        self.assertFalse(self.graph.has_path(1, 5))
        self.assertTrue(self.graph.has_node(5))

    def test_remove_edge4(self):
        """ Remove non-existing edge. """
        self.graph.remove_edge(4, 5)

    def test_remove_edge5(self):
        self.graph.remove_edge(3, 5, True)

        self.assertFalse(self.graph.has_path(1, 5))
        self.assertFalse(self.graph.has_node(5))

    def test_remove_edge6(self):
        self.graph.remove_edge(1, 3, True)

        self.assertTrue(self.graph.has_path(1, 5))

    def test_remove_node1(self):
        self.graph.remove_node(2)

        self.assertTrue(self.graph.has_node(1))
        self.assertTrue(self.graph.has_node(4))
        self.assertTrue(self.graph.has_node(6))
        self.assertFalse(self.graph.has_node(2))

        self.assertFalse(self.graph.has_edge(2, 4))
        self.assertFalse(self.graph.has_edge(1, 2))

    def test_remove_node2(self):
        self.graph.remove_node(3, True)

        self.assertFalse(self.graph.has_node(5))
        self.assertFalse(self.graph.has_edge(1, 3))
        self.assertFalse(self.graph.has_edge(3, 5))
        self.assertFalse(self.graph.has_path(1, 5))

    def test_remove_node3(self):
        self.graph.remove_node(3, False)

        self.assertTrue(self.graph.has_node(5))
        self.assertFalse(self.graph.has_edge(1, 3))
        self.assertFalse(self.graph.has_edge(3, 5))
        self.assertFalse(self.graph.has_path(1, 5))

    def test_transitive_reduce1(self):
        self.graph.transitively_reduce()

        self.assertTrue(self.graph.has_edge(4, 3))
        self.assertFalse(self.graph.has_edge(1, 3))

    def test_add_double_edge(self):
        self.graph.add_edge(1, 3)
        self.graph.remove_edge(1, 3)

        # the one and only edge must be removed now
        self.assertFalse(self.graph.has_edge(1, 3))

    def test_add_double_edge_with_id(self):
        self.graph.add_edge(1, 3, "Dummy")
        self.assertFalse(self.graph.has_edge_id("Dummy"))

        self.graph.remove_edge(1, 3)

        # the one and only edge must be removed now
        self.assertFalse(self.graph.has_edge(1, 3))

    def test_str_output(self):
        out = 'digraph g {\n  1\n  1 -> 2 [label="1"]\n  1 -> 3\n  2\n  2 -> 4 [label="Test"]\n  3\n  3 -> 5\n  4\n  4 -> 3\n  4 -> 6\n  5\n  6\n  6 -> 2\n}\n'
        self.assertEqual(str(self.graph), out)

    def test_dot_output_without_labels(self):
        out = 'digraph g {\n  1\n  1 -> 2\n  1 -> 3\n  2\n  2 -> 4\n  3\n  3 -> 5\n  4\n  4 -> 3\n  4 -> 6\n  5\n  6\n  6 -> 2\n}\n'
        self.assertEqual(self.graph.dot(False), out)

if __name__ == '__main__':
    unittest.main()
