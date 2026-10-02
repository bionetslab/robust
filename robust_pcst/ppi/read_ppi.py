import networkx as nx

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