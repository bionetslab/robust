import networkx as nx
import numpy as np
import typing

from .edge_ids import EdgeIds
from .vertex_ids import VertexIds
from ..ppi import PpiInstance


def unit_cost(e):
    """
    Simple initialization function for the edge prizes.
    """
    return 1.0

def zero_prize(v):
    """
    Simple initialization function for the vertex prizes.
    """
    return 0.0


class PcstInstance:
    """
    This class represents an instance (i.e., a graph with weighted edges and vertices) for
    the PCST solver. It primarily saves the graph in a compatible and efficient
    data structure. You can use update functions to efficiently update a subpart
    of the weights.
    Creating the instance for the PPI-graph is quite slow so you do not want to create
    a new instance for every round but simply update the weights.
    """
    def __init__(self, ppi_instance: PpiInstance,
                 initial_costs_fn: typing.Optional[typing.Callable[[object], float]] = None,
                 initial_prize_fn: typing.Callable[[object], float] = zero_prize):
        """
        ppi_instance: The Protein-Protein-Interaction instance with PPI-graph, terminals
        for a disease and the edge costs.
        initial_costs_fn: A function to determine the initial edge costs. If none, the
        edge costs of the instance are used. Note that you can change them any time with
        update_edge_costs.
        initial_prize_fn: A function to define the initial prizes of the vertices. By
        default zero. Note that you can change them any time with update_vertex_prizes.
        """
        self._vertex_ids = VertexIds(ppi_instance.ppi_graph.nodes)
        self._edge_ids = EdgeIds(ppi_instance.ppi_graph, self._vertex_ids)
        if not initial_costs_fn:
            initial_costs_fn = lambda e: ppi_instance.edge_weights[e]
        edges = [(self._vertex_ids.get_id(e[0]), self._vertex_ids.get_id(e[1])) for e in
                 ppi_instance.ppi_graph.edges]
        self._edges = np.array(sorted(edges), dtype=np.int64)
        self._prizes = np.array([initial_prize_fn(self._vertex_ids.get_label(i)) for i in
                                 range(ppi_instance.ppi_graph.number_of_nodes())], dtype=np.float64)

        def f(e):
            e_v = self._vertex_ids.get_label(e[0])
            e_w = self._vertex_ids.get_label(e[1])
            return initial_costs_fn((e_v, e_w))

        self._costs = np.array(np.apply_along_axis(f, axis=1, arr=self._edges),
                               dtype=np.float64)

    @property
    def vertex_ids(self) -> VertexIds:
        """
        A two-way map to convert networkx vertices to ids and ids to nx vertices.
        Internally, we work with ids which are simply their position in the array.
        self.vertex_ids.get_id(v_0) -> 0
        self.vertex_ids.get_label(0) -> v_0
        """
        return self._vertex_ids

    @property
    def edges(self) -> np.ndarray:
        """
        Numpy array [[u,v], [u', v'], ...] with the edges.
        The vertices are saved as ids.
        """
        return self._edges

    @property
    def prizes(self) -> np.ndarray:
        """
        A numpy array with the prizes of the vertices.
        self.prizes[self.vertex_ids.get_id(v_0)] == self.get_node_prize(v_0)
        """
        return self._prizes

    @property
    def costs(self) -> np.ndarray:
        """
        A numpy array with the weight/costs of the edges.
        This function is primarily used internally for passing the data to the solver.
        Use get_edge_cost or update_edge_costs.
        """
        return self._costs

    def update_edge_costs(self, d: typing.Dict):
        """
        Update the costs for some edges.
        The dict maps from edge to cost.
        """
        for edge in d:
            self._costs[self._edge_ids.get_id(edge)] = d[edge]

    def update_vertex_prizes(self, d: typing.Dict):
        for node in d:
            self._prizes[self._vertex_ids.get_id(node)] = d[node]

    def get_vertex_prize(self, label=None):
        """
        Returns the prize to a node identified by label. To access the prize regarding
        to the index, directly use self.prizes[i]
        """
        return self._prizes[self._vertex_ids.get_id(label)]

    def get_edge_cost(self, e):
        """
        Returns the costs of an edge identified by the networkx edge. To acces the edge
        regarding to its index, directly use self.costs[i]
        """
        return self._costs[self._edge_ids.get_id(e)]
