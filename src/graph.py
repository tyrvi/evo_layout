import numpy as np

class Graph:
    """A Graph is a list of vertices and a list of edges"""
    def __init__(self, V=[], E=[]):
        self.V = V
        self.E = E


class Vertex:
    """A Vertex consists of a 2-tuple for position, `pos`, and a 2-tuple for 
    displacement, `disp`."""
    def __init__(self, pos=[0, 0], disp=[0, 0], random=False):
        # TODO: allow for random instantiation of position
        self.pos = np.array(pos)
        self.disp = np.array(disp)


class Edge:
    """An Edge consists of two instances of Vertex, `v1` and `v2`."""
    def __init__(self, v1=None, v2=None):
        self.v1 = v1
        self.v2 = v2
