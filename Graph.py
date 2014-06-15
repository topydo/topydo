""" Contains the class for a directed graph. """

class DirectedGraph(object):
    """
    Represents a simple directed graph, used for tracking todo
    dependencies. The nodes are very simple: just integers.
    """
    def __init__(self):
        self._edges = {}

    def add_node(self, p_id):
        """ Adds a node to the graph. """
        if not self.has_node(p_id):
            self._edges[p_id] = set()

    def has_node(self, p_id):
        """ Returns true iff the graph has the given node. """
        return p_id in self._edges

    def add_edge(self, p_from, p_to):
        """
        Adds an edge to the graph. The nodes will be added if they don't
        exist.
        """
        if not self.has_node(p_from):
            self.add_node(p_from)

        if not self.has_node(p_to):
            self.add_node(p_to)

        self._edges[p_from].add(p_to)

    def has_path(self, p_from, p_to):
        """
        Returns true iff there is a path from the first node to the second.
        """
        return p_to in self.reachable_nodes(p_from)

    def incoming_neighbors(self, p_id, p_recursive=False):
        """
        Returns a set of the direct neighbors that can reach the given
        node.
        """
        return self.reachable_nodes_reverse(p_id, p_recursive)

    def outgoing_neighbors(self, p_id, p_recursive=False):
        """
        Returns the set of the direct neighbors that the given node can
        reach.
        """
        return self.reachable_nodes(p_id, p_recursive)

    def reachable_nodes(self, p_id, p_recursive=True, p_reverse=False):
        """
        Returns the set of all neighbors that the given node can reach.

        If recursive, it will also return the neighbor's neighbors, etc.
        If reverse, the arrows are reversed and then the reachable neighbors
        are located.
        """
        stack = [p_id]
        visited = set()
        result = set()

        while len(stack):
            current = stack.pop()

            if current in visited or current not in self._edges:
                continue

            visited.add(current)

            if p_reverse:
                parents = [node for node, neighbors in self._edges.iteritems() \
                    if current in neighbors]

                stack = stack + parents
                result = result.union(parents)
            else:
                stack = stack + list(self._edges[current])
                result = result.union(self._edges[current])

            if not p_recursive:
                break

        return result

    def reachable_nodes_reverse(self, p_id, p_recursive=True):
        """ Find neighbors in the inverse graph. """
        return self.reachable_nodes(p_id, p_recursive, True)

    def remove_node(self, p_id, remove_unconnected_nodes=True):
        """ Removes a node from the graph. """
        if self.has_node(p_id):
            for neighbor in self.incoming_neighbors(p_id):
                self._edges[neighbor].remove(p_id)

            neighbors = set()
            if remove_unconnected_nodes:
                neighbors = self.outgoing_neighbors(p_id)

            del self._edges[p_id]

            for neighbor in neighbors:
                if self.is_isolated(neighbor):
                    self.remove_node(neighbor)

    def is_isolated(self, p_id):
        """
        Returns True iff the given node has no incoming or outgoing edges.
        """
        return len(self.incoming_neighbors(p_id)) == 0 \
           and len(self.outgoing_neighbors(p_id)) == 0

    def has_edge(self, p_from, p_to):
        """ Returns True when the graph has the given edge. """
        return p_from in self._edges and p_to in self._edges[p_from]

    def remove_edge(self, p_from, p_to, remove_unconnected_nodes=True):
        """
        Removes an edge from the graph.

        When remove_unconnected_nodes is True, then the nodes are also removed
        if they become isolated.
        """
        if self.has_edge(p_from, p_to):
            self._edges[p_from].remove(p_to)

        if remove_unconnected_nodes:
            if self.is_isolated(p_from):
                self.remove_node(p_from)

            if self.is_isolated(p_to):
                self.remove_node(p_to)

