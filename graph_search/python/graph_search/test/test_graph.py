import pytest
from graph_search.graph import UndirectedEdgeListGraph, GraphInvariantViolationException

def check_undirected_graph_variants(graph):
        try:
            graph.validate_undirectedness()
        except GraphInvariantViolationException:
            pytest.fail("Graph is not undirected")


class TestUndirectedEdgeListGraph:
    def test_empty_graph_is_empty(self):
        graph = UndirectedEdgeListGraph()
        assert not graph.edges
        assert not graph.vertices

    def test_can_add_a_weighted_edge(self):
        graph = UndirectedEdgeListGraph()

        vertex_from = 1
        vertex_to = 2
        weight = 3.14

        graph.add_edge(vertex_from, vertex_to, weight)

        actual_vertices = graph.vertices
        assert len(actual_vertices) == 2
        assert vertex_from in actual_vertices
        assert vertex_to in actual_vertices

        actual_edges = graph.edges
        assert len(actual_edges) == 2
        assert (vertex_from, vertex_to, weight) in actual_edges
        assert (vertex_to, vertex_from, weight) in actual_edges

        check_undirected_graph_variants(graph)
