import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import colors
from matplotlib import cm
import networkx as nx

from .solution_set import SolutionSet
from ..ppi import PpiInstance
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


class __VertexColor:

    def __init__(self, solution_set: SolutionSet):
        self.ppi_instance = solution_set.ppi_instance
        self.solution_set = solution_set
        self.max_occurence = max(
            solution_set.number_of_occurrences(v) for v in self.solution_set.vertices() if
            v not in self.ppi_instance.terminals)
        self.cmap = plt.get_cmap("cool")
        self.steiner_color = colors.Normalize(vmin=1.0, vmax=self.max_occurence)

    def __call__(self, v):
        if v in self.ppi_instance.terminals:
            return 'red'
        return self.cmap(self.steiner_color(self.solution_set.number_of_occurrences(v)))
        if self.solution_set.number_of_occurrences(v) > 1:
            return self.cmap(self.steiner_color(self.solution_set.number_of_occurrences(v)))
        else:
            return 'green'

    def draw_colorbar(self):
        cb = cm.ScalarMappable(norm=self.steiner_color,
                          cmap=self.cmap)
        plt.colorbar(cb)

        legend_elements = [
                           Line2D([0], [0], marker='o', color='red', label='Terminal',
                                  markerfacecolor='red', markersize=15)]
        plt.gca().legend(handles=legend_elements, loc='upper right')



def display_solution_set(solution_set: SolutionSet):
    print("Vertices in all solutions: ", solution_set.number_of_vertices())
    print("Average size of solution: ", solution_set.avg_size())
    print("Average cost of solution:", solution_set.avg_cost())
    print("Minimum cost of solution:", solution_set.min_cost())
    print("Maximum cost of solution:", solution_set.max_cost())
    color_selector = __VertexColor(solution_set)
    for s in solution_set:
        plt.figure(figsize=(20, 20))
        pos = nx.kamada_kawai_layout(s)
        nx.draw_networkx_labels(s, pos)
        nx.draw(s, pos, node_color=[color_selector(v) for v in s.nodes])
        color_selector.draw_colorbar()
        plt.show()
