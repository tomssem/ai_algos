import itertools
import random

import pytest

from graph_search.graph import UndirectedEdgeListGraph, GraphInvariantViolationException, MultipleEdgesException

def check_undirected_graph_variants(graph):
    try:
        graph.validate_undirectedness()
    except GraphInvariantViolationException:
        pytest.fail("Graph is not undirected")

def create_unique_edges(num_vertices, num_edges, min_weight, max_weight):
    """
    Creates a set of unique edges
    """
    all_edges = set(map(tuple, map(sorted, itertools.product(range(num_vertices), range(num_vertices)))))
    edges_no_weight = random.sample(all_edges, num_edges)
    return [(v_in, v_out, random.uniform(min_weight, max_weight)) for v_in, v_out in edges_no_weight]


def add_edges_test(edges, graph):
    expected_edges = set()
    expected_vertices = set()

    for vertex_from, vertex_to, weight in edges:
        graph.add_edge(vertex_from, vertex_to, weight)
        expected_vertices.add(vertex_from)
        expected_vertices.add(vertex_to)
        expected_edges.add((vertex_from, vertex_to, weight))
        expected_edges.add((vertex_to, vertex_from, weight))


    assert len(expected_edges) == len(graph.edges)
    assert expected_edges == set(graph.edges)

    assert len(expected_vertices) == len(graph.vertices)
    assert expected_vertices == set(graph.vertices)

    check_undirected_graph_variants(graph)


class TestUndirectedEdgeListGraph:
    def setup_method(self, method):
        random.seed(1000003)
        self.graph = UndirectedEdgeListGraph()

    def test_empty_graph_is_empty(self):
        assert not self.graph.edges
        assert not self.graph.vertices

    def test_can_add_a_weighted_edge(self):
        vertex_from = 1
        vertex_to = 2
        weight = 3.14

        self.graph.add_edge(vertex_from, vertex_to, weight)

        actual_vertices = self.graph.vertices
        assert len(actual_vertices) == 2
        assert vertex_from in actual_vertices
        assert vertex_to in actual_vertices

        actual_edges = self.graph.edges
        assert len(actual_edges) == 2
        assert (vertex_from, vertex_to, weight) in actual_edges
        assert (vertex_to, vertex_from, weight) in actual_edges

        check_undirected_graph_variants(self.graph)

    def test_can_add_an_unweighted_edge(self):
        vertex_from = 1
        vertex_to = 2

        self.graph.add_edge(vertex_from, vertex_to)

        actual_vertices = self.graph.vertices
        assert len(actual_vertices) == 2
        assert vertex_from in actual_vertices
        assert vertex_to in actual_vertices

        actual_edges = self.graph.edges
        assert len(actual_edges) == 2
        assert (vertex_from, vertex_to, 1) in actual_edges
        assert (vertex_to, vertex_from, 1) in actual_edges

        check_undirected_graph_variants(self.graph)

    def test_cant_add_same_edge_twice(self):
        self.graph.add_edge(1, 2, 3)

        with pytest.raises(MultipleEdgesException) as excinfo:
            self.graph.add_edge(1, 2, 3)

        assert "already" in str(excinfo.value)

    def test_catch_undirectedness_violations(self):
        self.graph._edge_list.add((1, 2, 3))

        with pytest.raises(GraphInvariantViolationException) as excinfo:
            self.graph.validate_undirectedness()

        assert "undirected" in str(excinfo.value)

    def test_can_add_multiple_weighted_edges(self):
        edges = [(1, 2, 4.6), (4, 3, 8.8)]

        add_edges_test(edges, self.graph)

    def test_vertices_unique(self):
        edges = [(1, 2, 4.6), (4, 2, 8.8)]

        add_edges_test(edges, self.graph)

    def test_add_many_edges(self):
        edges = create_unique_edges(1000, 10000, 0, 10000)
        add_edges_test(edges, self.graph)

    def test_children_of_simple(self):
        vertex_from = 1
        vertex_to = 2
        weight = 3.14
        self.graph.add_edge(vertex_from, vertex_to, weight)

        assert [(vertex_to, weight)] == self.graph.children_of(vertex_from)
        assert [(vertex_from, weight)] == self.graph.children_of(vertex_to)

    def test_children_of_complex(self):
        edges = create_unique_edges(100, 1000, 0, 1000)

        for edge in edges:
            self.graph.add_edge(*edge)

        for v_from, _, _  in edges:
            expected_parents = [(v_to, weight) for (_v_from, v_to, weight) in self.graph.edges if v_from == _v_from]

            assert sorted(self.graph.children_of(v_from)) == sorted(expected_parents)

    def test_parents_of_simple(self):
        vertex_from = 1
        vertex_to = 2
        weight = 3.14
        self.graph.add_edge(vertex_from, vertex_to, weight)

        assert [(vertex_to, weight)] == self.graph.parents_of(vertex_from)
        assert [(vertex_from, weight)] == self.graph.parents_of(vertex_to)

    def test_parents_of_complex(self):
        edges = create_unique_edges(100, 1000, 0, 1000)

        for edge in edges:
            self.graph.add_edge(*edge)

        for _, v_to, _  in edges:
            expected_parents = [(v_from, weight) for (v_from, _v_to, weight) in self.graph.edges if v_to == _v_to]

            assert sorted(self.graph.parents_of(v_to)) == sorted(expected_parents)
