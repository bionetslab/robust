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




class BiasAwareEdgeWeight_Additive:
    """
    An alternative edge weight that penalizes hubs. Note that the corresponding
    steiner tree no longer minimizes the number of vertices. The solutions could
    be more path like because in especially hubs are great steiner points that are now
    no longer attractive to use.
    """
    def __init__(self, graph: nx.Graph, lambda_):
        self.graph = graph
        self.lambda_=lambda_
        self.average_bait_usage=self._calculate_average_bait_usage()
        
    def _calculate_average_bait_usage(self):
        bait_usages = nx.get_node_attributes(self.graph, 'bias_data')
        sum_=0
        for a in self.graph.nodes:
            sum_ = sum_ + bait_usages[a]
        return sum_ / self.graph.number_of_nodes()
    
    def __getitem__(self, e):
        # weight=(1-lambda_) * average[graph.nodes[sourceNODES[i]]["bait_usage"]] + 0.5*lambda_*(graph.nodes[sourceNODES[i]]["bait_usage"]+graph.nodes[targetNODES[i]]["bait_usage"])
        # return self.graph.edges[e[0], e[1]]["bait_edgeweights"]
        if (1-self.lambda_*self.average_bait_usage)+0.5*self.lambda_*(self.graph.nodes[e[0]]['bias_data']+self.graph.nodes[e[1]]['bias_data']) >= 0:
            return (1-self.lambda_*self.average_bait_usage)+0.5*self.lambda_*(self.graph.nodes[e[0]]['bias_data']+self.graph.nodes[e[1]]['bias_data'])
        else:
            return 0


class BiasAwareEdgeWeight_Exponential:
    """
    An alternative edge weight that penalizes hubs. Note that the corresponding
    steiner tree no longer minimizes the number of vertices. The solutions could
    be more path like because in especially hubs are great steiner points that are now
    no longer attractive to use.
    """
    def __init__(self, graph: nx.Graph, lambda_):
        self.graph = graph
        self.lambda_=lambda_
        
    def __getitem__(self, e):
        if (self.graph.nodes[e[0]]['bias_data']+self.graph.nodes[e[1]]['bias_data'])**self.lambda_ >= 0:
            return (self.graph.nodes[e[0]]['bias_data']+self.graph.nodes[e[1]]['bias_data'])**self.lambda_
        else:
            return 0



















