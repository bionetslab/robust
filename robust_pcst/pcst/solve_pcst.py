from timeit import default_timer as timer

import pcst_fast
import networkx as nx

from .pcst_instance import PcstInstance


def solve_pcst(pcst_graph: PcstInstance) -> nx.Graph:
    """
    Solves the PCST instance. Should run in 0.3-1.0 seconds.
    It returns the selected subgraph without any labels, i.e. only vertices and edges, no
     weights or costs.
    """
    root = -1
    num_clusters = 1
    pruning = 'strong'
    vertices_, edges_ = pcst_fast.pcst_fast(pcst_graph.edges, pcst_graph.prizes,
                                            pcst_graph.costs, root, num_clusters, pruning,
                                            0)
    G_ = nx.Graph()
    vertex_ids = pcst_graph.vertex_ids
    G_.add_nodes_from([vertex_ids.get_label(i) for i in vertices_])
    G_.add_edges_from([(vertex_ids.get_label(pcst_graph.edges[i][0]),
                        vertex_ids.get_label(pcst_graph.edges[i][1])) for i in edges_])
    assert nx.is_tree(G_), "Result should be a tree"
    return G_
