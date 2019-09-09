"""
Data structures for representing graphs
"""

import abc
import collections
import copy
import functools

import numpy as np

DTYPE = np.dtype("float32")
"""
types we use for numpy arrays
"""

class AbstractGraph(abc.ABC):
    """
    Abstract base class for all graph objects. This is an mutable data structure
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
        :param vertex_from: the vertex this edge leaves
        :param vertex_to: the vertex this edge enters
        :param weight: the weight of this vertex
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


class VertexNotFoundException(Exception):
    """
    Raised when a requested vertex is not on the graph
    """


class MultipleEdgesException(Exception):
    """
    Raised when the same edge added to the graph again
    """


class UndirectedGraph:
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

class DirectedGraph(AbstractGraph):
    """
    Class that represents an undirected graph
    """
    @abc.abstractmethod
    def add_edge(self, vertex_from, vertex_to, weight=1):
        """
        Add an edge from `vertex_from` to `vertex_to` with weight `weight` (default value: 1).
        Only the edge will be added, and the edge in the opposite direction will not be added (as
        in UndirectedGraph
        Returns a new graph (since this is an immutable graph)
        :param vertex_from: the vertex this edge leaves
        :param vertex_to: the vertex this edge enters
        :param weight: the weight of this vertex
        """

class AbstractEdgeListGraph(AbstractGraph):
    """
    All edge list graphs inherit from this
    """
    def __init__(self):
        self._vertices = set()
        self._edge_list = set()
        self._edge_set = set()

    @property
    def vertices(self):
        return list(self._vertices)

    @property
    def edges(self):
        return list(self._edge_list)

    def _get_matching_edges(self, predicate):
        # gets all edges that match the provided predicate
        # predicate is of type Func[(int, int, float), Bool]

        results = []
        for edge in self._edge_list:
            if predicate(*edge):
                results.append(edge)

        return results

    def edges_from(self, vertex):
        if vertex not in self._vertices:
            raise VertexNotFoundException("No such vertex {}".format(vertex))

        results = []
        for vertex_from, vertex_to, weight in self._edge_list:
            if vertex_from == vertex:
                results.append((vertex_to, weight))

        return self._get_matching_edges(lambda v, _v, _w: v == vertex)

    def edges_to(self, vertex):
        if vertex not in self._vertices:
            raise VertexNotFoundException("No such vertex {}".format(vertex))

        results = []
        for vertex_from, vertex_to, weight in self._edge_list:
            if vertex_to == vertex:
                results.append((vertex_from, weight))

        return self._get_matching_edges(lambda _v, v, _w: v == vertex)

    @abc.abstractmethod
    def add_edge(self, vertex_from, vertex_to, weight=1):
        pass

class DirectedEdgeListGraph(AbstractEdgeListGraph, DirectedGraph):
    """
    A directed graph that is represented by and edge list
    """

    def add_edge(self, vertex_from, vertex_to, weight=1):
        if (vertex_from, vertex_to) in self._edge_set:
            raise MultipleEdgesException("Vertex ({}, {}) already exists".format(vertex_from,
                                                                                 vertex_to))
        self._edge_set.add((vertex_from, vertex_to))
        self._edge_list.add((vertex_from, vertex_to, weight))
        self._vertices.update([vertex_from, vertex_to])


class UndirectedEdgeListGraph(AbstractEdgeListGraph, UndirectedGraph):
    """
    Undirected graph that is represented using an edge list
    """

    def validate_undirectedness(self):
        cnt = collections.Counter()
        for (vertex_in, vertex_out, _) in self._edge_list:
            cnt[(vertex_in, vertex_out)] += 1
            cnt[(vertex_out, vertex_in)] += 1

        if not all([v == 2 for v in cnt.values()]):
            raise GraphInvariantViolationException("Not undirected graph")

    def add_edge(self, vertex_from, vertex_to, weight=1):
        if (vertex_from, vertex_to) in self._edge_set or (vertex_to, vertex_from) in self._edge_set:
            raise MultipleEdgesException("Vertex ({}, {}) already exists".format(vertex_from,
                                                                                 vertex_to))
        self._edge_set.add((vertex_from, vertex_to))
        self._edge_list.add((vertex_from, vertex_to, weight))
        self._edge_list.add((vertex_to, vertex_from, weight))
        self._vertices.update([vertex_from, vertex_to])

class AbstractAdjacencyMatrixGraph(AbstractGraph):
    """
    Abstract adjacency matrix class
    """
    def __init__(self):
        self._adjacency_matrix = np.empty((0, 0), dtype=DTYPE)

    def _resize(self, size):
        # resize the adjacency matrix to the specified square size, copying over previous elements
        # into the same positions and padding with zeros
        tmp = np.zeros((size, size), dtype=DTYPE)
        tmp[:len(self._adjacency_matrix), :len(self._adjacency_matrix)] = self._adjacency_matrix
        self._adjacency_matrix = tmp

    @property
    def vertices(self):
        return np.where(self._adjacency_matrix.any(axis=0))[0].tolist()

    @property
    def edges(self):
        return [(i, j, self._adjacency_matrix[i, j].item())
                for i, j
                in zip(*np.where(self._adjacency_matrix))]

    def edges_from(self, vertex):
        return [(vertex, i, float(self._adjacency_matrix[vertex, i]))
                for i
                in np.where(self._adjacency_matrix[vertex])[0]]

    def edges_to(self, vertex):
        return [(i, vertex, float(self._adjacency_matrix[i, vertex]))
                for i
                in np.where(self._adjacency_matrix[:, vertex])[0]]
    @abc.abstractmethod
    def add_edge(self, vertex_from, vertex_to, weight=1):
        pass

class UndirectedAdjacencyMatrixGraph(AbstractAdjacencyMatrixGraph, UndirectedGraph):
    """
    Adjacency matrix implementation of an undirected graph
    """
    @property
    def vertices(self):
        return np.where(self._adjacency_matrix.any(axis=0))[0].tolist()

    def validate_undirectedness(self):
        if not np.array_equiv(self._adjacency_matrix, self._adjacency_matrix.T):
            raise GraphInvariantViolationException("Not undirected graph")

    def add_edge(self, vertex_from, vertex_to, weight=1):
        greatest_vertex = max(vertex_from, vertex_to)
        if len(self._adjacency_matrix) > greatest_vertex:
            # already space for this vertex
            if (self._adjacency_matrix[vertex_from][vertex_to] or
                    self._adjacency_matrix[vertex_to][vertex_from]):
                # we already have an entry for this edge
                raise MultipleEdgesException("Vertex ({}, {}) already exists".format(vertex_from,
                                                                                     vertex_to))
        else:
            # need to grow adjacency matrix
            self._resize(greatest_vertex + 1)

        self._adjacency_matrix[vertex_from, vertex_to] = weight
        self._adjacency_matrix[vertex_to, vertex_from] = weight

class DirectedAdjacencyMatrixGraph(AbstractAdjacencyMatrixGraph, DirectedGraph):
    """
    Directed graph implemented as an adjacency matrix
    """
    @property
    def vertices(self):
        return list(set(np.where(self._adjacency_matrix.any(axis=0))[0].tolist() +
                        np.where(self._adjacency_matrix.any(axis=1))[0].tolist()))

    def add_edge(self, vertex_from, vertex_to, weight=1):
        greatest_vertex = max(vertex_from, vertex_to)
        if len(self._adjacency_matrix) > greatest_vertex:
            # already space for this vertex
            if self._adjacency_matrix[vertex_from][vertex_to]:
                # we already have an entry for this edge
                raise MultipleEdgesException("Vertex ({}, {}) already exists".format(vertex_from,
                                                                                     vertex_to))
        else:
            # need to grow adjacency matrix
            self._resize(greatest_vertex + 1)

        self._adjacency_matrix[vertex_from, vertex_to] = weight

class AbstractAdjacencyListGraph(AbstractGraph):
    """
    Base class for all adjacency list graphs
    """
    def __init__(self):
        # maps from a vertex, to all vertices reachable to it along with the respective weights
        self._adjacency_list = collections.defaultdict(list) # type: Dict[Int, Tuple[int, float]]
        self._edge_set = set()

    @property
    def vertices(self):
        def _accum(a, b):
            a.add(b)
            return a
        from_vertices = functools.reduce(_accum, self._adjacency_list.keys(), set())
        to_vertices = [e for edges in self._adjacency_list.values() for (e, w) in edges]
        return list(from_vertices.union(to_vertices))

    @property
    def edges(self):
        return list([(v1, v2, w)
                     for v1 in self._adjacency_list
                     for (v2, w)
                     in self._adjacency_list[v1]])

    def edges_from(self, vertex):
        return list([(vertex, v1, w) for (v1, w) in self._adjacency_list[vertex]])

    def edges_to(self, vertex):
        return list(set([(v1, vertex, w)
                         for v1 in self._adjacency_list
                         for (v2, w) in self._adjacency_list[v1]
                         if v2 == vertex]))

    @abc.abstractmethod
    def add_edge(self, vertex_from, vertex_to, weight=1):
        pass

class UndirectedAdjacencyListGraph(AbstractAdjacencyListGraph, UndirectedGraph):
    """
    Adjacency list implementation of undirected graph
    """
    def add_edge(self, vertex_from, vertex_to, weight=1):
        if (vertex_from, vertex_to) in self._edge_set or (vertex_to, vertex_from) in self._edge_set:
            raise MultipleEdgesException("Vertex ({}, {}) already exists".format(vertex_from,
                                                                                 vertex_to))
        self._adjacency_list[vertex_from].append((vertex_to, weight))
        self._adjacency_list[vertex_to].append((vertex_from, weight))

        self._edge_set.add((vertex_from, vertex_to))
        self._edge_set.add((vertex_to, vertex_from))
