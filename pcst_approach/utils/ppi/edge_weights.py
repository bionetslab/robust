import networkx as nx

class CoVexEdgeWeight:
    """
    An alternative edge weight that penalizes hubs. Note that the corresponding
    steiner tree no longer minimizes the number of vertices. The solutions could
    be more path like because in especially hubs are great steiner points that are now
    no longer attractive to use.
    """
    def __init__(self, graph: nx.Graph, lambda_):
        self.graph = graph
        self.avg_degree = self._calculate_avg_degree()
        self.lambda_ = lambda_

    def _calculate_avg_degree(self):
        return 2 * self.graph.number_of_edges() / self.graph.number_of_nodes()

    def __getitem__(self, e):
        return (1 - self.lambda_) * self.avg_degree + self.lambda_ * 0.5 * (
                self.graph.degree()[e[0]] + self.graph.degree()[e[1]])


class UnitEdgeWeight:
    """
    Simple unit edge weights. Every edge has the same weight. A Steiner Tree, thus,
    minimizes just the number of vertices.
    """
    def __getitem__(self, e):
        return 1.0
