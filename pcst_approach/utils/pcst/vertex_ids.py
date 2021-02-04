class VertexIds:
    def __init__(self, node_names):
        self._id_to_name = list(node_names)
        self._name_to_id = {name: i for i, name in enumerate(self._id_to_name)}
        
    def get_label(self, i):
        return self._id_to_name[i]
    
    def get_id(self, label):
        return self._name_to_id[label]