# Graph search for AI
## Introduction
Many domains in the real world can be expressed as graphs, for example maps, computer networks, and discrete state transitions can all be represented by graphs. We can then ask questions about how to perform certain tasks in this domain, such as: "How far is Winnipeg from Montreal?", "How quickly can I send a packet of information from computer A to computer B?", and "How do I cook an egg?". All the above questions boil down to finding paths through the graphs that represent the problem. In maps a path represents a sequence of roads between junctions, in computer networks it represents a step of hops between routers, and for discrete transitions, it represents a sequence of actions that effect a change in state.

The problem of searching for paths on graphs will form the basis for this XXX. We will look at how to represent graphs, how to measure the goodness of paths through them, and then how to search for (possibly optimal) paths through them.

## Definitions
A graph, $$G$$ is represented as a set of vertices:

$$V\$$

and edges between the vertices:

$$E \subseteq \{(v_\text{i}, v_\text{j}, w), v_\text{i} \in V, v_\text{j} \in V, \w \in \mathbbm{R}\}$$

where each edge joins $$v_i$$ to $$v_j$$, and (potentially) has a weight, $$w$$ associated with it.

A graph can be undirected in that if $$(v_i, v_j, w^i)$$ is an edge on a graph, then an edge in the opposite direction $$(v_o, v_i, w^i)$$ is also present. In a directed graph, edges in one direction can be present.

A path on a graph path connects two nodes by following edge: a path $$p$$ from $$v_1$$ to $$v_n$$, in graph $$G$$ denoted $$v_1\leadsto_G v_n$$, is a sequence of edges $$[(v_1, v_2, w_1), .., (v_{n-1}, v_n, w_{n-1})]$$ where $$(v_i, v_{i+1}, w_i) \in E$$ for $$i=1, ..., n-1$$. There may be multiple paths that lead from $$v_1$$ to $$v_2$$, in which case we index paths as $$v_1 \leadsto_G^i v_n$$ The cost of a path is $$c{p} = \sum_{i=1}^{n-1} w_i$$, the sum of edge weights along the path. The length of a path $$l{l} = {n-1}$$ is simply equal to the number of edges.

## The graph search problem
In graph search we seek to find a path from some source node, to some target node that has a minimum cost among all satisfying paths (we can find a maximum cost path by simply negating all the edge weights and preceding as below). If all the edge weights are constant across the graph, then finding a minimum cost path amounts to finding a minimum length path.

Expressed formally we have: Given $$G = (V, E)$$, a source node $$v_{a}$$, and a target node $$v_{b}$$, find a path $$p^* = v_a\leadsto_G^{i} v_b$$ s.t. $$c(v_a\leadsto_G^{i} v_b) \leq c(v_a\leadsto_G^{j} v_b) \ \forall \ j$$


## Graph search solutions
There are two broad categories of graph search alogorithms, *uninformed* and *informed*.

### Uninformed search algorithms
Uninformed s
