import networkx as nx

from .edge_weights import UnitEdgeWeight


class PpiInstance:
    """
    Describes an instance for which we want to find multiple diverse steiner trees.
    It consists of a graph (more or less static PPI), terminals (different for each
    disease), and edge weights (probably constant but there are multiple options).
    One could actually encode it directly the the networkx-graph but the PPI graph is
    rather big. We don't want you to reload it for every new set of terminals, etc.
    All the values should be constant.
    """

    def __init__(self, ppi_graph: nx.Graph, terminals: list,
                 edge_weights=UnitEdgeWeight(), meta=None):
        self.ppi_graph = ppi_graph
        self.terminals = terminals
        self.edge_weights = edge_weights
        if not meta:
            self.meta = {"graph_diameter": 8}  # Precomputed.
            print("Setting the graph_diameter to the precomputed value of 8. "
                  "Directly specify meta to overwrite this.")
        else:
            self.meta = meta

    def compute_cost(self, subgraph: nx.Graph):
        return sum(self.edge_weights[e] for e in subgraph.edges)

    def is_feasible_solution(self, steiner_tree: nx.Graph, percentage_terminals_req_in_solution: int):
        """
        Checks if the solution covers all terminals and is connected.
        """
        #for v in self.terminals:
        #    if v not in steiner_tree.nodes:
        #        return False
        intersection_length = len(set(self.terminals).intersection(set(steiner_tree.nodes)))
        if intersection_length / len(self.terminals) < percentage_terminals_req_in_solution:
            return False
        return nx.is_connected(steiner_tree)
