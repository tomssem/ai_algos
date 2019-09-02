"""
Data structures for representing graphs
"""

import abc
import collections
import copy

class AbstractGraph(abc.ABC):
    """
    Abstract base class for all graph objects. This is an immutable data structure
    Nodes are represented by integers, and edges as tuples of `(vertex_from, vertex_to, weight)`,
    where weight is a float representing the weight of the edge (this will be 1 in unweighted
    graphs.
    """

    @abc.abstractproperty
    def vertices(self):
        """
        Return a list of all vertices
        :rtype: List[int]
        """

    @abc.abstractproperty
    def edges(self):
        """
        Return a list of all edges
        :rtype: List[(int, int, weight)]
        """

    @abc.abstractmethod
    def add_edge(self, vertex_from, vertex_to, weight=1):
        """
        Add an edge from `vertex_from` to `vertex_to` with weight `weight` (default value: 1).
        Behaviour may change based on whether this is a directed graph or an undirected graph
        (see implementing subclass).
        If the vertices are not present in the graph they will be added
        Returns a new graph (since this is an immutable graph)
        :param vertex_from: the vertex this edge leaves
        :param vertex_to: the vertex this edge enters
        :param weight: the weight of this vertex
        """

    @abc.abstractmethod
    def children_of(self, vertex):
        """
        Get children that are accessible to this node, along with accompanying weights
        :param int vertex: the vertex we want to find all children of
        :returns: A list of all children [(vertex, weight)]
        :rtype: List[Tuple[int, float]]
        """

    @abc.abstractmethod
    def parents_of(self, vertex):
        """
        Get parents that can access this node laong with accompanying weights.
        :param int vertex: the vertex we want to find all parents of
        :returns: A list of all parents [(vertex, weight)]
        :rtype: List[Tuple[int, float]]
        """

    @abc.abstractmethod
    def edges_from(self, vertex):
        """
        Get all edges that lead from supplied vertex
        :param int vertex: the vertex we want to find all edges from
        :returns: A list of all edges from this node [(vertex_out, vertex_in, weight)]
        :rtype: List[Tuple[int, int, float]]
        """

    @abc.abstractmethod
    def edges_to(self, vertex):
        """
        Get all edges that lead to supplied vertex
        :param int vertex: the vertex we want to find all edges to
        :returns: A list of all edges into this node [(vertex_out, vertex_in, weight)]
        :rtype: List[Tuple[int, int, float]]
        """

class GraphInvariantViolationException(Exception):
    """
    Raised when graph is found to be in violation of its invariants
    """

class UndirectedGraph(AbstractGraph):
    """
    Class that represents an undirected graph.

    Defines::
     validate_undirectedness
    """

    @abc.abstractmethod
    def validate_undirectedness(self):
        """
        Checks that this graph is indeed undirected
        :raises GraphInvariantError
        """

    @abc.abstractmethod
    def add_edge(self, vertex_from, vertex_to, weight=1):
        """
        Add an edge from `vertex_from` to `vertex_to` with weight `weight` (default value: 1).
        This will essentially add two edges `(vertex_from, vertex_to, weight)` and
        `(vertex_to, vertex_from, weight)`
        Returns a new graph (since this is an immutable graph)
        :param vertex_from: the vertex this edge leaves
        :param vertex_to: the vertex this edge enters
        :param weight: the weight of this vertex
        """

class UndirectedEdgeListGraph(UndirectedGraph):
    """
    Undirected graph that is represented using an edge list
    """

    def __init__(self):
        self._edge_list = []
        self._vertices = []

    def validate_undirectedness(self):
        cnt = collections.Counter()
        for (vertex_in, vertex_out, _) in self.edges:
            cnt[(vertex_in, vertex_out)] += 1
            cnt[(vertex_out, vertex_in)] += 1

        if not all([v == 2 for v in cnt.values()]):
            raise GraphInvariantViolationException("Not undirected graph")

    @property
    def vertices(self):
        return copy.copy(self._vertices)

    @property
    def edges(self):
        return copy.copy(self._edge_list)

    def add_edge(self, vertex_from, vertex_to, weight=1):
        self._edge_list.append((vertex_from, vertex_to, weight))
        self._edge_list.append((vertex_to, vertex_from, weight))
        self._vertices.extend([vertex_from, vertex_to])
        self.validate_undirectedness()

    def children_of(self, vertex):
        pass

    def parents_of(self, vertex):
        pass

    def edges_from(self, vertex):
        pass

    def edges_to(self, vertex):
        pass
