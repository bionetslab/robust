import pandas as pd

from ..ppi import PpiInstance


class SolutionSet(list):
    """
    A simple class that allows some aggregation functions on the solution set.
    """

    def __init__(self, ppi_instance: PpiInstance):
        super().__init__()
        self.ppi_instance = ppi_instance

    def min_cost(self) -> float:
        return min(self.ppi_instance.compute_cost(s) for s in self)

    def max_cost(self) -> float:
        return max(self.ppi_instance.compute_cost(s) for s in self)

    def avg_cost(self) -> float:
        costs = [self.ppi_instance.compute_cost(s) for s in self]
        return sum(costs) / len(costs)

    def vertices(self, first_n=None):
        all_vertices = set()
        if first_n is None:
            first_n = len(self)
        for s in self[0:first_n]:
            for v in s.nodes:
                all_vertices.add(v)
        return all_vertices

    def number_of_vertices(self) -> int:
        return len(self.vertices())

    def number_of_occurrences(self, v):
        return sum(v in s.nodes for s in self)

    def get_occurrences(self, include_terminals=False, first_n=None) -> pd.DataFrame:
        """
        Returns a pandas data frame with the occurrences of the vertices.
        It has the vertex label as index and the columns
        * #occurrences: The number of occurrences
        * %occurrences: The relative occurences (0.0-1.0)
        * terminal: If it is a terminal (use include_terminals=True to include them).
        """
        data = {"vertex": [], "#occurrences": [], "%occurrences": [], "terminal": []}
        for v in self.vertices(first_n=first_n):
            if include_terminals or v not in self.ppi_instance.terminals:
                data["vertex"].append(v)
                data["#occurrences"].append(self.number_of_occurrences(v))
                data["%occurrences"].append(self.number_of_occurrences(v) / len(self))
                data["terminal"].append(v in self.ppi_instance.terminals)
        return pd.DataFrame(data).sort_values(["#occurrences"], ascending=False,
                                              kind="mergesort").set_index("vertex")

    def avg_size(self) -> float:
        return sum(s.number_of_nodes() for s in self) / len(self)

    def __contains__(self, item):
        vertices = set(item.nodes)
        return any(vertices == set(g.nodes) for g in self)
