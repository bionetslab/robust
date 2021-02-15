from typing import Tuple, List

import networkx as nx
from .vertex_ids import VertexIds


class EdgeIds:
    """
    Maps between networkx-edges and the two necessary representations in pcst_fast:
    Position in the cost-array and the pair of ids of the vertices.
    """
    def __init__(self, ppi_graph: nx.Graph, vertex_ids: VertexIds):
        self._vertex_ids = vertex_ids
        self.key_to_nx = {self.get_key(e): e for e in ppi_graph.edges}
        self.id_to_edge_key = sorted(self.edge_ids())
        self._edge_key_to_id = {edge: i for i, edge in enumerate(self.id_to_edge_key)}

    def get_key(self, e: Tuple[str,  str]) -> Tuple[int, int]:
        """
        Returns a unique representation of the networkx edge e in the numpy representation
        because edges in networkx are tuples and (a,b)=(b,a). Unfortunately, this is
        problematic in dictionaries so we use this key-function.
        """
        id1 = self._vertex_ids.get_id(e[0])
        id2 = self._vertex_ids.get_id(e[1])
        return min(id1, id2), max(id1, id2)

    def get_id(self, e: Tuple[str, str]) -> int:
        """
        Returns the position of the networkx-edge in the numpy-array of the
        pcst_fast graph representation.
        """
        key = self.get_key(e)
        return self._edge_key_to_id[key]

    def get_nx_edge(self, i: Tuple[int, int]) -> Tuple[str, str]:
        """
        Returns the networkx-edge for two numpy vertex-ids.
        TODO: Why are they not made unique?
        """
        return self.key_to_nx[i]

    def edge_ids(self) -> List[Tuple[int, int]]:
        """
        Returns all edges (numpy id tuples).
        """
        return list(self.key_to_nx.keys())
