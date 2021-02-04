from typing import Tuple, List

import networkx as nx
from .vertex_ids import VertexIds


class EdgeIds:
    def __init__(self, ppi_graph: nx.Graph, vertex_ids: VertexIds):
        self._vertex_ids = vertex_ids
        self.key_to_nx = {self.get_key(e): e for e in ppi_graph.edges}
        self.id_to_edge_key = sorted(self.edge_ids())
        self._edge_key_to_id = {edge: i for i, edge in enumerate(self.id_to_edge_key)}

    def get_key(self, e) -> Tuple[int, int]:
        id1 = self._vertex_ids.get_id(e[0])
        id2 = self._vertex_ids.get_id(e[1])
        return min(id1, id2), max(id1, id2)

    def get_id(self, e) -> int:
        key = self.get_key(e)
        return self._edge_key_to_id[key]

    def get_nx_edge(self, i: Tuple[int, int]):
        return self.key_to_nx[i]

    def edge_ids(self) -> List[Tuple[int, int]]:
        return list(self.key_to_nx.keys())
