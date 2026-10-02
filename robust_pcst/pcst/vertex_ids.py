class VertexIds:
    """
    Mapping between the labels of the PPI-graph and the ids in the numpy-representation
    for the pcst_fast implementation.
    """

    def __init__(self, node_names):
        self._id_to_name = list(node_names)
        self._name_to_id = {name: i for i, name in enumerate(self._id_to_name)}

    def get_label(self, i: int) -> str:
        """
        Returns the networkx label of the vertex at position i in the numpy-representation
        for pcst_fast.
        """
        return self._id_to_name[i]

    def get_id(self, label: str) -> int:
        """
        Returns the position of the networkx label in the numpy array of the
        representation for pcst_fast.
        """
        return self._name_to_id[label]
