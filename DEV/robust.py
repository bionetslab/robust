import sys
from pcst_approach.utils.ppi import PpiInstance, read_terminals, UnitEdgeWeight, CoVexEdgeWeight, BiasAwareEdgeWeight_Additive, BiasAwareEdgeWeight_Exponential, read_ppi, read_ppi_biasaware
from pcst_approach.utils import ExpMinMaxDiverseSteinerTreeComputer
import argparse



def call_robust(path_to_graph, edge_cost_mode, node_namespace_mode, normalize_mode, lambda_value, path_to_seeds, outfile, init, red, numberOfSteinerTrees, threshold):
    import networkx as nx
    
    lambda_=lambda_value
    
    if lambda_>1 or lambda_<0:
        lambda_=0.00
    
        
    if normalize_mode=='BAIT_USAGE':
        if node_namespace_mode=='ENTREZ_GENE_ID':
            pathToStudyBiasData='../../data/edgeweightdata/gene_bait_usage.csv'
        elif node_namespace_mode=='GENE_SYMBOL':
            pathToStudyBiasData='../../data/edgeweightdata/gene_bait_usage.csv'
        elif node_namespace_mode=='UNIPROT_PROTEIN_ID':
            pathToStudyBiasData='../../data/edgeweightdata/gene_bait_usage.csv'
        flag=int(1)
            
    elif normalize_mode=='STUDY_ATTENTION':
        if node_namespace_mode=='ENTREZ_GENE_ID':
            pathToStudyBiasData='../../data/edgeweightdata/study_attention.csv'
        elif node_namespace_mode=='GENE_SYMBOL':
            pathToStudyBiasData='../../data/edgeweightdata/study_attention.csv'
        elif node_namespace_mode=='UNIPROT_PROTEIN_ID':
            pathToStudyBiasData='../../data/edgeweightdata/study_attention.csv'
        flag=int(2)
        
    elif normalize_mode=='CUSTOM':
        if node_namespace_mode=='ENTREZ_GENE_ID':
            pathToStudyBiasData='../../data/edgeweightdata/custom.csv'
        elif node_namespace_mode=='GENE_SYMBOL':
            pathToStudyBiasData='../../data/edgeweightdata/custom.csv'
        elif node_namespace_mode=='UNIPROT_PROTEIN_ID':
            pathToStudyBiasData='../../data/edgeweightdata/custom.csv'
        flag=int(3)
        
    if edge_cost_mode=='UNIFORM':
        graph = read_ppi(path_to_graph)
    else:
        graph = read_ppi_biasaware(path_to_graph, pathToStudyBiasData, flag)
        
    terminals = read_terminals(path_to_seeds)
    #kick out terminals not in graph
    terminals = list(set(terminals).intersection(set(graph.nodes)))
        
    if edge_cost_mode=='UNIFORM':
        edge_weights = UnitEdgeWeight()
    else:
        if edge_cost_mode=='ADDITIVE':
            edge_weights = BiasAwareEdgeWeight_Additive(graph, lambda_)
        elif edge_cost_mode=='EXPONENTIAL':
            edge_weights = BiasAwareEdgeWeight_Exponential(graph, lambda_)
            
        
    ppi_instance = PpiInstance(graph, terminals, edge_weights)
    
    nx.write_graphml_lxml(graph, "TEMP.graphml")
    
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
        t.to_csv(args.path_to_outfile)
    elif outfile.endswith(".graphml"):
        nx.write_graphml(subgraph, args.path_to_outfile)
    else:
        nx.write_edgelist(subgraph, args.path_to_outfile, data=False)




def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_graph', type=str, help='specify path to graph')
    parser.add_argument('path_to_seeds', type=str, help='specify path to seeds')
    parser.add_argument('path_to_outfile', type=str, help='specify path to outfile')
    parser.add_argument('--node_namespace', type=str, choices=['ENTREZ_GENE_ID', 'GENE_SYMBOL', 'UNIPROT_PROTEIN_ID'], default='GENE_SYMBOL')
    parser.add_argument('initial_fraction', default=0.25, type=float, help='specify initial fraction, default=0.25')
    parser.add_argument('reduction_factor', default=0.9, type=float, help='specify reduction factor')
    parser.add_argument('number_of_steiner_trees', default=30, type=int, help='specify no. of steiner trees')
    parser.add_argument('threshold', default=0.1, type=float, help='specify threshold')
    parser.add_argument('--edge_cost', type=str, choices=['UNIFORM', 'ADDITIVE', 'EXPONENTIAL'], default='UNIFORM')
    parser.add_argument('--normalize', type=str, default='BAIT_USAGE', choices=['BAIT_USAGE', 'STUDY_ATTENTION', 'CUSTOM'], help='Specifies edge weight function used by ROBUST')
    parser.add_argument('--lambda_', type=float, default=0.5, help='Hyper-parameter lambda used by PAIR_FREQ, BAIT_USAGE and CUSTOM edge weights. Should be set to value between 0 and 1.')
    args = parser.parse_args()
    return parser




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
    
    
    
    # python robust.py data/human_annotated_PPIs_brain.txt data/ms_seeds.txt ms.graphml 0.25 0.9 30 0.1
    args = get_parser().parse_args()
    # python robust.py data/human_annotated_PPIs_brain.txt data/ms_seeds.txt ms.graphml 0.25 0.9 30 0.1
    
    
    
    # input_list = sys.argv
    # print("Parsing input...")
    # path_to_graph = str(input_list[1])
    # edge_cost_mode=str(input_list[2])
    # node_namespace_mode=str(input_list[3])
    # normalize_mode=str(input_list[4])
    # lambda_value=float(input_list[5])
    # path_to_seeds = str(input_list[6])
    # path_to_outfile = str(input_list[7])
    # initial_fraction = float(input_list[8])
    # reduction_factor = float(input_list[9])
    # number_of_steiner_trees = int(input_list[10])
    # threshold = float(input_list[11])

    print(f"Computing Steiner Trees with the following parameters: \n "
          f"graph: {args.path_to_graph}\n"
          f"edgeWeightMode: {args.path_to_graph}\n"
          f"seeds: {args.path_to_seeds}\n"
          f"outfile: {args.path_to_outfile}\n"
          f"initial fraction: {args.initial_fraction}\n"
          f"reduction factor: {args.reduction_factor}\n"
          f"number of steiner trees: {args.number_of_steiner_trees}\n"
          f"threshold: {args.threshold}")
    args.number_of_steiner_trees -=1
    call_robust(args.path_to_graph, args.edge_cost, args.node_namespace, args.normalize, args.lambda_, args.path_to_seeds, args.path_to_outfile, args.initial_fraction, args.reduction_factor, args.number_of_steiner_trees, args.threshold)
    