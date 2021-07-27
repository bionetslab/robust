import numpy as np
import networkx as nx

from .solution_set import SolutionSet
from ..pcst import PcstInstance, solve_pcst
from ..ppi import PpiInstance


class ExpMinMaxDiverseSteinerTreeComputer:
    """
    A simple version to compute diverse steiner trees based on the minimum and the
    maximum edge weights.
    * Terminals: Will get 2*diameter*max_edge_costs as prize. This way they should always
        be included.
    * Other vertices: Will get some fraction of the minimum edge weight as prize. This way
        they are to expensive to add without a connection to a terminal. As soon as they
        are used, their prizes will get reduced by a factor to make them less attractive
        to integrate.
    * The edge weights of the ppi instances are used.
    """

    def __init__(self, initial_fraction=0.1, reduction_factor=0.3,
                 initial_terminal_multiple=2):
        """
        initial_fraction: The prize for non-terminals will be
                    initial_fraction*min_edge_costs. A lower value will result in cheaper
                    steiner trees but less variation.
        reduction_factor: Whenever a vertex is used as steiner vertex, it's prize will be
                    multiplied by this value to make it less attractive. We do not
                    set it to zero because if we have to use some vertices multiple time
                    (looks like 50%-90% of the vertices have to be reused to obtain
                    reasonably cheap steiner trees), we want to make using those that
                    are used the least more attractive.
        initial_terminal_multiple: The prize for the terminals will be this times the
                    diameter of the graph times the maximal edge cost. If it is too low
                    to force all terminals to be integrated, it will be doubled up to
                    10 times (2^10) automatically.
        """
        self.initial_fraction = initial_fraction
        self.reduction_factor = reduction_factor
        self.initial_terminal_multiple = initial_terminal_multiple

    def iterate_solutions(self, ppi_instance: PpiInstance):
        """
        Returns an infinite amount of steiner trees as a generator.
        """
        data = {
            "ppi_instance": ppi_instance,
            "pcst_graph": PcstInstance(ppi_instance)
        }
        data["min_edge_cost"] = np.min(data["pcst_graph"].costs)
        data["max_edge_cost"] = np.max(data["pcst_graph"].costs)
        self._set_initial_prizes(data)
        while True:
            steiner_tree = self._compute_steiner_tree(data)
            yield steiner_tree
            self._reduce_prizes_of_used_steiner_vertices(data, steiner_tree)

    def __call__(self, ppi_instance: PpiInstance, n=10):
        """
        Returns a solution set with n steiner trees for the instance.
        Will stop automatically after the first repetition, thus, it may be less than
        n steiner trees.
        """
        solution_set = SolutionSet(ppi_instance)
        for s in self.iterate_solutions(ppi_instance):
            if s in solution_set:
                break
            solution_set.append(s)
            if len(solution_set) > n:
                break
        return solution_set

    def _reduce_prizes_of_used_steiner_vertices(self, data, steiner_tree: nx.Graph):
        """
        The prizes of the steiner points in the pcst-graph will be reduced.
        """
        data["pcst_graph"].update_vertex_prizes(
            {
                v: self.reduction_factor * data["pcst_graph"].get_vertex_prize(v)
                for v in steiner_tree.nodes if v not in data["ppi_instance"].terminals
            }
        )

    def _set_initial_prizes(self, data):
        """
        Sets the initial prizes of the pcst-graph. We don't use the initialize function
        in the constructor of the pcst-graph because we can much more efficiently get
        the min and max edge costs for the numpy representation in the pcst-graph.
        """
        self._set_initial_terminal_prizes(data)
        self._set_initial_steiner_prizes(data)

    def _set_initial_terminal_prizes(self, data):
        """
        The terminal prizes are based on the diameter.
        """
        d = data["ppi_instance"].meta["graph_diameter"]
        terminal_prize = self.initial_terminal_multiple * d * data["max_edge_cost"]
        data["pcst_graph"].update_vertex_prizes(
            {v: terminal_prize for v in data["ppi_instance"].terminals}
        )

    def _double_terminal_prizes(self, data):
        """
        Doubles the prizes of the terminals. Used if it was too low and not all terminals
        are integrated in the prize collecting steiner tree.
        """
        data["pcst_graph"].update_vertex_prizes(
            {
                v: 2 * data["pcst_graph"].get_vertex_prize(v)
                for v in data["ppi_instance"].terminals
            }
        )

    def _set_initial_steiner_prizes(self, data):
        """
        Sets the prizes of the steiner vertices (non-terminals).
        """
        ppi_instance: PpiInstance = data["ppi_instance"]
        p = self.initial_fraction * data["min_edge_cost"]
        data["pcst_graph"].update_vertex_prizes(
            {
                v: p
                for v in ppi_instance.ppi_graph.nodes if
                v not in ppi_instance.terminals
            }
        )

    def _compute_steiner_tree(self, data):
        """
        Does the expensive computation of the steiner tree including doubling the prizes
        of the terminals if not all are integrated in the solution.
        """
        st = solve_pcst(data["pcst_graph"])
        # TODO: The following code was actually useless as it did not compute anything.
        #       The PCST algorithm cannot guarantee to contain all seeds. This would require
        #       an additional algorithm, possibly based on shortest path. Because the primary
        #       part of the solution is already complete, one could also try to contract the
        #       steiner tree and rerun the algorithm.
        #i_doubled = 0
        #while not data["ppi_instance"].is_feasible_solution(st, percentage_terminals_req_in_solution):
        #    self._double_terminal_prizes(data)
        #    i_doubled += 1
        #    if i_doubled >= max_nr_of_doublings:
        #        print(f"Doubled the prizes {max_nr_of_doublings} times and could not find a feasible solution "
        #              f"with these parameters. Returning current Steiner Tree anyway.")
        #        return st
                #raise Exception(
                #    """
                #    Could not find a feasible solution even after doubling the prizes
                #    of the terminals multiple times. Something is odd. Maybe check input?
                #    """
                #)
        return st