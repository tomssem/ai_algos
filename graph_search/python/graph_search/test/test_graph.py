import itertools
import random

import pytest

from graph_search.graph import (UndirectedEdgeListGraph, GraphInvariantViolationException,
                                MultipleEdgesException, DirectedEdgeListGraph,
                                UndirectedAdjacencyMatrixGraph)

UNDIRECTED_TYPE=[UndirectedEdgeListGraph, UndirectedAdjacencyMatrixGraph]

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


def undirected_add_edges_test(edges, graph):
    # check that when we edge an edge to a graph, it and the edge in the opposite direction is
    # added.
    expected_edges = set()
    expected_vertices = set()

    for vertex_from, vertex_to, weight in edges:
        graph.add_edge(vertex_from, vertex_to, weight)
        expected_vertices.add(vertex_from)
        expected_vertices.add(vertex_to)
        expected_edges.add((vertex_from, vertex_to, weight))
        expected_edges.add((vertex_to, vertex_from, weight))

    actual_edges = graph.edges
    actual_edges_dict = edge_list_to_dict(actual_edges)
    assert len(expected_edges) == len(actual_edges)

    for v_in, v_out, w in expected_edges:
        assert pytest.approx(actual_edges_dict[(v_in, v_out)], w)

    assert len(expected_vertices) == len(graph.vertices)
    assert expected_vertices == set(graph.vertices)

    check_undirected_graph_variants(graph)

def directed_add_edges_test(edges, graph):
    # check that when an edge is added to the graph, only that edge is added
    expected_edges = set()
    expected_vertices = set()

    for vertex_from, vertex_to, weight in edges:
        graph.add_edge(vertex_from, vertex_to, weight)
        expected_vertices.add(vertex_from)
        expected_vertices.add(vertex_to)
        expected_edges.add((vertex_from, vertex_to, weight))

    assert len(expected_edges) == len(graph.edges)
    assert expected_edges == set(graph.edges)

    assert len(expected_vertices) == len(graph.vertices)
    assert expected_vertices == set(graph.vertices)

@pytest.fixture(params=[(UndirectedEdgeListGraph, undirected_add_edges_test),
                        (DirectedEdgeListGraph, directed_add_edges_test),
                         (UndirectedAdjacencyMatrixGraph, undirected_add_edges_test)])
def construct_graph(request):
    GraphType, test_function = request.param
    return GraphType(), test_function

@pytest.fixture
def set_random_seed():
    random.seed(1000003)
    yield


def test_empty_graph_is_empty(construct_graph):
    graph, _ = construct_graph
    assert not graph.edges
    assert not graph.vertices

def edge_list_to_dict(edges):
    # convert an edge list to a dict of vertices to weights to make it easier to compare
    # numpy and native python floats
    return {(v1, v2): w for (v1, v2, w) in edges}

@pytest.mark.parametrize("GraphType", UNDIRECTED_TYPE)
def test_can_add_a_weighted_edge_undirected_graph(GraphType):
    graph = GraphType()
    vertex_from = 1
    vertex_to = 2
    weight = 3.14

    graph.add_edge(vertex_from, vertex_to, weight)

    actual_vertices = graph.vertices
    assert len(actual_vertices) == 2
    assert vertex_from in actual_vertices
    assert vertex_to in actual_vertices

    actual_edges = graph.edges
    actual_edges_dict = edge_list_to_dict(actual_edges)

    assert len(actual_edges) == 2
    assert pytest.approx(actual_edges_dict[(vertex_from, vertex_to)], weight)
    assert pytest.approx(actual_edges_dict[(vertex_to, vertex_from)], weight)

    check_undirected_graph_variants(graph)

def test_can_add_a_weighted_edge_directed_graph():
    graph = DirectedEdgeListGraph()
    vertex_from = 1
    vertex_to = 2
    weight = 3.14

    graph.add_edge(vertex_from, vertex_to, weight)

    actual_vertices = graph.vertices
    assert len(actual_vertices) == 2
    assert vertex_from in actual_vertices
    assert vertex_to in actual_vertices

    actual_edges = graph.edges
    assert len(actual_edges) == 1
    assert (vertex_from, vertex_to, weight) in actual_edges

@pytest.mark.parametrize("GraphType", UNDIRECTED_TYPE)
def test_can_add_an_unweighted_edge_undirected_graph(GraphType):
    graph = GraphType()
    vertex_from = 1
    vertex_to = 2

    graph.add_edge(vertex_from, vertex_to)

    actual_vertices = graph.vertices
    assert len(actual_vertices) == 2
    assert vertex_from in actual_vertices
    assert vertex_to in actual_vertices

    actual_edges = graph.edges
    assert len(actual_edges) == 2
    assert (vertex_from, vertex_to, 1) in actual_edges
    assert (vertex_to, vertex_from, 1) in actual_edges

    check_undirected_graph_variants(graph)

def test_can_add_an_unweighted_edge_directed_graph():
    graph = DirectedEdgeListGraph()
    vertex_from = 1
    vertex_to = 2

    graph.add_edge(vertex_from, vertex_to)

    actual_vertices = graph.vertices
    assert len(actual_vertices) == 2
    assert vertex_from in actual_vertices
    assert vertex_to in actual_vertices

    actual_edges = graph.edges
    assert len(actual_edges) == 1
    assert (vertex_from, vertex_to, 1) in actual_edges

def test_cant_add_same_edge_twice(construct_graph):
    graph, test_function = construct_graph
    graph.add_edge(1, 2, 3)

    with pytest.raises(MultipleEdgesException) as excinfo:
        graph.add_edge(1, 2, 3)

    assert "already" in str(excinfo.value)

def test_can_add_multiple_weighted_edges(construct_graph):
    graph, test_function = construct_graph
    edges = [(1, 2, 4.6), (4, 3, 8.8)]

    test_function(edges, graph)

def test_vertices_unique(construct_graph):
    graph, test_function = construct_graph
    edges = [(1, 2, 4.6), (4, 2, 8.8)]

    test_function(edges, graph)

def test_add_many_edges(construct_graph):
    graph, test_function = construct_graph
    edges = create_unique_edges(1000, 10000, 0, 10000)
    test_function(edges, graph)

@pytest.mark.parametrize("GraphType", UNDIRECTED_TYPE)
def test_edges_from_simple_undirected(GraphType):
    graph = GraphType()
    vertex_from = 1
    vertex_to = 2
    weight = 3.14
    graph.add_edge(vertex_from, vertex_to, weight)

    from_vertex_from_edges = graph.edges_from(vertex_from)
    assert len(from_vertex_from_edges) == 1
    assert from_vertex_from_edges[0][0] == vertex_from
    assert from_vertex_from_edges[0][1] == vertex_to
    assert pytest.approx(from_vertex_from_edges[0][2], weight)

    to_vertex_from_edges = graph.edges_from(vertex_to)
    assert len(to_vertex_from_edges) == 1
    assert to_vertex_from_edges[0][0] == vertex_to
    assert to_vertex_from_edges[0][1] == vertex_from
    assert pytest.approx(to_vertex_from_edges[0][2], weight)

def test_edges_from_simple_directed():
    graph = DirectedEdgeListGraph()
    vertex_from = 1
    vertex_to = 2
    weight = 3.14
    graph.add_edge(vertex_from, vertex_to, weight)

    from_vertex_from_edges = graph.edges_from(vertex_from)
    assert len(from_vertex_from_edges) == 1
    assert from_vertex_from_edges[0][0] == vertex_from
    assert from_vertex_from_edges[0][1] == vertex_to
    assert pytest.approx(from_vertex_from_edges[0][2], weight)

def test_edges_from_complex(construct_graph):
    graph, test_function = construct_graph
    edges = create_unique_edges(100, 1000, 0, 1000)

    for edge in edges:
        graph.add_edge(*edge)

    edges = graph.edges
    for v_from, _, _  in edges:
        expected_children = [(v_from, v_to, weight) for (_v_from, v_to, weight) in edges if v_from == _v_from]
        actual_children = edge_list_to_dict(graph.edges_from(v_from))

        assert len(expected_children) == len(actual_children)
        for v1, v2, w in expected_children:
            assert pytest.approx(actual_children[(v1, v2)], w)

@pytest.mark.parametrize("GraphType", UNDIRECTED_TYPE)
def test_edges_to_simple_undirected(GraphType):
    graph = GraphType()
    vertex_from = 1
    vertex_to = 2
    weight = 3.14
    graph.add_edge(vertex_from, vertex_to, weight)

    from_vertex_from_edges = graph.edges_from(vertex_from)
    assert len(from_vertex_from_edges) == 1
    assert from_vertex_from_edges[0][0] == vertex_from
    assert from_vertex_from_edges[0][1] == vertex_to
    assert pytest.approx(from_vertex_from_edges[0][2], weight)

    to_vertex_from_edges = graph.edges_from(vertex_to)
    assert len(to_vertex_from_edges) == 1
    assert to_vertex_from_edges[0][0] == vertex_to
    assert to_vertex_from_edges[0][1] == vertex_from
    assert pytest.approx(to_vertex_from_edges[0][2], weight)

def test_edges_to_simple_directed():
    graph = DirectedEdgeListGraph()
    vertex_from = 1
    vertex_to = 2
    weight = 3.14
    graph.add_edge(vertex_from, vertex_to, weight)

    assert [(vertex_from, vertex_to, weight)] == graph.edges_to(vertex_to)

def test_edges_to_complex(construct_graph):
    graph, test_function = construct_graph
    edges = create_unique_edges(100, 1000, 0, 1000)

    for edge in edges:
        graph.add_edge(*edge)

    edges = graph.edges
    for _, v_to, _  in edges:
        expected_parents = [(v_from, _v_to, weight) for (v_from, _v_to, weight) in edges if v_to == _v_to]

        assert sorted(graph.edges_to(v_to)) == sorted(expected_parents)

def test_catch_undirectedness_violations_edge_list():
    graph = UndirectedEdgeListGraph()
    graph._edge_list.add((1, 2, 3))

    with pytest.raises(GraphInvariantViolationException) as excinfo:
        graph.validate_undirectedness()

    assert "undirected" in str(excinfo.value)

def test_catch_undirectedness_violations_adjacency_list():
    graph = UndirectedAdjacencyMatrixGraph()
    graph._resize(10)
    graph._adjacency_matrix[0][1] = 2

    with pytest.raises(GraphInvariantViolationException) as excinfo:
        graph.validate_undirectedness()

    assert "undirected" in str(excinfo.value)
