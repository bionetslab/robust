import sys
from pcst_approach.utils.ppi import PpiInstance, read_terminals, UnitEdgeWeight, read_ppi
from pcst_approach.utils import ExpMinMaxDiverseSteinerTreeComputer


def call_robust(path_to_graph, path_to_seeds, outfile, init, red, numberOfSteinerTrees, threshold):
    import networkx as nx
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
    steiner_trees = engine(ppi_instance, n=numberOfSteinerTrees)
    t = steiner_trees.get_occurrences(include_terminals=True)
    t = t[t["%occurrences"] >= threshold]
    subgraph = steiner_trees.get_subgraph(threshold=threshold)
    comp_idx = 0
    for comp in sorted(nx.connected_components(subgraph), key=len, reverse=True):
        for node in comp:
            subgraph.nodes[node]['connected_components_id'] = comp_idx
        comp_idx += 1
    print("Writing results...")
    if outfile.endswith(".csv"):
        t.to_csv(path_to_outfile)
    elif outfile.endswith(".graphml"):
        nx.write_graphml(subgraph, path_to_outfile)
    else:
        nx.write_edgelist(subgraph, path_to_outfile, data=False)


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
    # [7] threshold
    input_list = sys.argv
    print("Parsing input...")
    path_to_graph = str(input_list[1])
    path_to_seeds = str(input_list[2])
    path_to_outfile = str(input_list[3])

    initial_fraction = float(input_list[4])
    reduction_factor = float(input_list[5])
    number_of_steiner_trees = int(input_list[6])
    threshold = float(input_list[7])

    print(f"Computing Steiner Trees with the following parameters: \n "
          f"graph: {path_to_graph}\n"
          f"seeds: {path_to_seeds}\n"
          f"outfile: {path_to_outfile}\n"
          f"initial fraction: {initial_fraction}\n"
          f"reduction factor: {reduction_factor}\n"
          f"number of steiner trees: {number_of_steiner_trees}\n"
          f"threshold: {threshold}")
    number_of_steiner_trees -=1
    call_robust(path_to_graph, path_to_seeds, path_to_outfile, initial_fraction, reduction_factor,
                    number_of_steiner_trees, threshold)
