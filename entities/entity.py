class Entity:
    """
    A network is a graph consists of nodes and edges.
    both nodes and edges are entities.
    """
    def __init__(self, id, name, description):
        self._id = id
        self._name = name
        self._description = description

    def hi(self):
        print("hi from entity")

    def add(self, a, b):
        return a + b
