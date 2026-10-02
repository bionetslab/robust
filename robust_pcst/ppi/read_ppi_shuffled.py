import networkx as nx
import random


def read_ppi_shuffled(file_path: str, shuffle=True):
    """
        Reads the PPI-graph from file without any attributes such as weight.
        In this version, the lines can be read in in a shuffled manner by first obtaining all lines in a list with readlines()
        and then shuffling the list before reading line by line.
    """
    vertices = set()
    edges = []
    file = open(file_path)
    lines = file.readlines()
    #remove header source_protein	target_protein
    lines.pop(0)
    #shuffle
    if shuffle:
        random.shuffle(lines)
    #print(lines[0])
    for line in lines:
        parsed_line = line.split('\t')
        v = parsed_line[0].strip()
        w = parsed_line[1].strip()
        vertices.add(v)
        vertices.add(w)
        edges.append((v, w))
    graph = nx.Graph()
    for v in vertices:
        graph.add_node(v, label=str(v))
    graph.add_edges_from(edges)
    return graph