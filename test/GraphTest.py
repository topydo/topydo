import unittest

import Graph

class GraphTest(unittest.TestCase):
    def setUp(self):
        self.graph = Graph.DirectedGraph()

        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 4)
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

    def test_incoming_neighbors1(self):
        self.assertEquals(self.graph.incoming_neighbors(1), set())

    def test_incoming_neighbors2(self):
        self.assertEquals(self.graph.incoming_neighbors(2), set([1, 6]))

    def test_incoming_neighbors3(self):
        self.assertEquals(self.graph.incoming_neighbors(1, True), set())

    def test_incoming_neighbors4(self):
        self.assertEquals(self.graph.incoming_neighbors(5, True), set([1, 2, 3, 4, 6]))

    def test_outgoing_neighbors1(self):
        self.assertEquals(self.graph.outgoing_neighbors(1), set([2, 3]))

    def test_outgoing_neighbors2(self):
        self.assertEquals(self.graph.outgoing_neighbors(2), set([4]))

    def test_outgoing_neighbors3(self):
        self.assertEquals(self.graph.outgoing_neighbors(1, True), set([2, 3, 4, 5, 6]))

    def test_outgoing_neighbors4(self):
        self.assertEquals(self.graph.outgoing_neighbors(3), set([5]))

    def test_outgoing_neighbors5(self):
        self.assertEquals(self.graph.outgoing_neighbors(5), set([]))

    def test_remove_edge1(self):
        self.graph.remove_edge(1, 2)

        self.assertFalse(self.graph.has_path(1, 4))
        self.assertTrue(self.graph.has_path(2, 4))

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
