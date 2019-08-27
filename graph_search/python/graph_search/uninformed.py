"""
Pure python implementation of uninformed graph search algorithms
"""

from abc import ABC
import copy

from graph_search.graph import Vertex

class XFirstSearch(ABC):
    """
    Abstract base class for all algorithms that select nodes from some collection to examine next
    """

    def __init__(self, goal: Vertex):
        self._goal = copy.deepcopy(goal)
        self._path = [] : List[Vertex]

    def visit(self, vertex: Vertex):
        """
        Visits the providing vertex, and adds any children to the collection of nodes to visit next
        """
        if vertex == self._goal:
            return self._path
        self._expand_to_visit(vertex.children)

    def _expand_to_visit(self, vertices: List[Vertex]):
        self.kkkkkkkkkkk
