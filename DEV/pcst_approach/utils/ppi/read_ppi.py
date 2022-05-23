import networkx as nx
import pandas as pd

def read_ppi_biasaware(file_path: str, pathToStudyBiasData: str, flag: int):
    """
    Reads the PPI-graph from file without any attributes such as weight.
    """
    vertices = set()
    edges = []
    with open(file_path, "r") as file:
        file.readline()
        for line in file:
            parsed_line = line.split('\t')
            v = parsed_line[0].strip()
            w = parsed_line[1].strip()
            vertices.add(v)
            vertices.add(w)
            edges.append((v,w))
    graph=nx.Graph()
    for v in vertices:
        graph.add_node(v, label=str(v))
    graph.add_edges_from(edges)
    
    # --------------------------------
    
    BIASAWARE_USAGE=pd.read_csv(pathToStudyBiasData, sep=',', usecols=['gene'])
    bias_symbol_List=list(BIASAWARE_USAGE['gene'])
    if flag==1:
        BIASAWARE_USAGE=pd.read_csv(pathToStudyBiasData, sep=',', usecols=['bait_usage'])
        bias_usage_List=list(BIASAWARE_USAGE['bait_usage'])
    elif flag==2:
        BIASAWARE_USAGE=pd.read_csv(pathToStudyBiasData, sep=',', usecols=['study_attention'])
        bias_usage_List=list(BIASAWARE_USAGE['study_attention'])
    elif flag==3:
        BIASAWARE_USAGE=pd.read_csv(pathToStudyBiasData, sep=',', usecols=['custom'])
        bias_usage_List=list(BIASAWARE_USAGE['custom'])
    
    NoOfGenesInBIASDATA=len(bias_symbol_List)
    Z=zip(bias_symbol_List, bias_usage_List)
    D=dict(Z)
    
    NODES=list(graph.nodes)
    NoOfNodes=len(NODES)
    BIASUSAGE=[]
    nx.set_node_attributes(graph, BIASUSAGE, 'bias_data')
        
    for i in range(NoOfNodes):
        graph.nodes[NODES[i]]['bias_data']=1
        
    for i in range(NoOfNodes):
        try:
            graph.nodes[NODES[i]]['bias_data']=int(D[NODES[i]])
        # except KeyError:
        except:
            graph.nodes[NODES[i]]['bias_data']=1
        
    EDGES=list(graph.edges)
    NoOfEdges=len(EDGES)

    sourceNODES=[]
    targetNODES=[]
    for src, tgt in graph.edges:
        sourceNODES.append(src)
        targetNODES.append(tgt)
    
    # --------------------------------
    return graph






def read_ppi(file_path: str):
    """
    Reads the PPI-graph from file without any attributes such as weight.
    """
    vertices = set()
    edges = []
    with open(file_path, "r") as file:
        file.readline()
        for line in file:
            parsed_line = line.split('\t')
            v = parsed_line[0].strip()
            w = parsed_line[1].strip()
            vertices.add(v)
            vertices.add(w)
            edges.append((v,w))
    graph=nx.Graph()
    for v in vertices:
        graph.add_node(v, label=str(v))
    graph.add_edges_from(edges)
    return graph