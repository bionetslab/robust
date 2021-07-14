import sys
from pcst_approach.utils.ppi import PpiInstance, read_terminals, UnitEdgeWeight, read_ppi
from pcst_approach.utils import ExpMinMaxDiverseSteinerTreeComputer


def call_robust(path_to_graph, path_to_seeds, init, red, numberOfSteinerTrees,
                    percentage_terminals_req_in_solution, max_nr_of_doublings):
    # 1. Loading the instance
    graph = read_ppi(path_to_graph)
    terminals = read_terminals(path_to_seeds)
    #kick out terminals not in graph
    terminals = list(set(terminals).intersection(set(graph.nodes)))
    #edge_weights = CoVexEdgeWeight(graph, 0.5)
    edge_weights = UnitEdgeWeight()
    ppi_instance = PpiInstance(graph, terminals, edge_weights)

    # 2. Solving the instance
    engine = ExpMinMaxDiverseSteinerTreeComputer(initial_fraction=init,
                                                 reduction_factor=red)
    # The most important parameter seems to be initial_fraction.
    steiner_trees = engine(ppi_instance, n=numberOfSteinerTrees,
                           percentage_terminals_req_in_solution=percentage_terminals_req_in_solution,
                           max_nr_of_doublings=max_nr_of_doublings)
    t = steiner_trees.get_occurrences(include_terminals=True)
    return t


if __name__ == '__main__':
    # -----------------------------------------------------
    # Checking for input from the command line:
    # -----------------------------------------------------
    #
    # [1] file providing the network in the form of an edgelist
    #     (tab-separated table, columns 1 & 2 will be used)
    #
    # [2] file with the seed genes (if table contains more than one
    #     column they must be tab-separated; the first column will be
    #     used only)
    #
    # [3] path to output file
    #
    # [4] initial fraction
    # [5] reduction factor
    # [6] number of steiner trees to be computed
    # [7] percentage of terminals that should be included in a steiner tree [0.0-1.0]
    # [8] how often should the terminal prizes be doubled before returning the tree anyway
    input_list = sys.argv
    print("Parsing input...")
    path_to_graph = str(input_list[1])
    path_to_seeds = str(input_list[2])
    path_to_outfile = str(input_list[3])

    initial_fraction = float(input_list[4])
    reduction_factor = float(input_list[5])
    number_of_steiner_trees = int(input_list[6])
    perc_terminals = float(input_list[7])
    doublings = int(input_list[8])

    print(f"Computing Steiner Trees with the following parameters: \n "
          f"graph: {path_to_graph}\n"
          f"seeds: {path_to_seeds}\n"
          f"outfile: {path_to_outfile}\n"
          f"initial fraction: {initial_fraction}\n"
          f"reduction factor: {reduction_factor}\n"
          f"number of steiner trees: {number_of_steiner_trees}\n"
          f"percentage terminals: {perc_terminals}\n"
          f"max number of doublings: {doublings}")
    number_of_steiner_trees -=1
    tree_table = call_robust(path_to_graph, path_to_seeds, initial_fraction, reduction_factor,
                    number_of_steiner_trees, perc_terminals, doublings)

    print("Writing results...")
    tree_table.to_csv(path_to_outfile)
