"""
This module ptovides topological sort of graph.

In the directed graph we progressively pick one leaf node,
remove all adges to it and add it at the head of the (ini-
tially empty) result list. If there is no more such leaf
node, we have either a cycle (if there are still edges/
nodes left) or we're done. Isolated nodes (with neither in-
nor outcoming edges) are inserted at the head of the result
list.


:Version: 0.0.1
:Authors: Dinu Gherman, Loic Calvino, Szymon Stoma
"""

import sys


def all_edges_from(v0, E):
    "Return a list of all edges (v0, w) in E starting at v0."

    res_edges = []
    for v, w in E:
        if v0 == v:
            res_edges.append((v, w))
    return res_edges


def _top_sort(v, E, visited, sorted, sorted_indices):
    "Recursive topsort function."

    visited[v] = 1
    for v, w in all_edges_from(v, E):
        if not visited[w]:
            _top_sort(w, E, visited, sorted, sorted_indices)
        else:
            if not sorted[w]:
                # TODO drop it..
                sys.exit(0)
    sorted[v] = 1
    sorted_indices.insert(0, v)


def top_sort(V, E):
    "Top-level sorting function."
    #print V, E
    n = len(V)
    visited = [0] * n   # Flags for (un-)visited elements.
    sorted = [0] * n    # Flags for (un-)sorted elements.
    sorted_indices = []  # The list of sorted element indices.

    for v in range(n):
        if not visited[v]:
            _top_sort(v, E, visited, sorted, sorted_indices)

    # Build and return a list of elements from the sort indices.
    sorted_elements = []
    for i in sorted_indices:
        sorted_elements.append(V[i])
    return sorted_elements


def wrap(pairs):
    """Convert an element pairs list into (verticesList, edgeIndexList).

    This might be useful for those who prefer topsort(edgeList)
    instead of topsort(verticesList, edgeIndexList)...
    E.g. wrap( [('a','b'), ('b','c'), ('c','a')] )
         -> (['a','b','c'], [(0,1), (1,2), (2,0)])
    """

    e = []
    v = []

    # Make a list of unique vertices.
    for x, y in pairs:
        if x not in v:
            v.append(x)
        if y not in v:
            v.append(y)

    # Convert original element pairs into index pairs.
    for x, y in pairs:
        e.append((v.index(x), v.index(y)))

    return v, e


