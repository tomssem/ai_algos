"""
Data structures for representing graphs
"""

import abc

class AbstractGraph(abc.ABC):
    """
    Abstract base class for all graph objects.
    Nodes are represented by integers, and edges as tuples of `(vertex_from, vertex_to, weight)`,
    where weight is a float representing the weight of the edge (this will be 1 in unweighted
    graphs.

    Defines::
     vertices
     load
     save
     children_of
     parents_of
     edges_from
     edges_to
    """

    @abc.abstractproperty
    def vertices(self):
        """
        Return a list of all vertices
        :rtype: List[int]
        """

    @abc.abstractmethod
    def save(self, path):
        """
        Save a graph to the provided filepath, will overwrite any existing file. Returns concrete
        graph object
        :param path: the string path from to which to save the graph
        :rtype: concrete class extending AbstractGraph
        """

    @abc.abstractclassmethod
    def load(cls, path):
        """
        Read a graph from a file at the provided filepath. Returns concrete graph object
        :param path: the string path from which to load a graph
        :rtype: concrete class extending AbstractGraph
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
