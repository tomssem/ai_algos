"""
Data structures for representing graphs
"""

import copy
from typing import List

class Vertex:
    """
    Represents a vertex in an immutable graph
    """
    def __init__(self, children: List[Vertex]):
        self._children = children

    @property
    def children(self):
        """
        Get the children of this node
        """
        return copy.deepcopy(self._children)
