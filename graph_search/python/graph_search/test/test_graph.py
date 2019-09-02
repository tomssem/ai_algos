import pytest
from graph_search.graph import UndirectedEdgeListGraph


class TestUndirectedEdgeListGraph:
    def test_empty_graph_is_empty(self):
        graph = UndirectedEdgeListGraph()
        assert not graph.edges
        assert not graph.vertices
