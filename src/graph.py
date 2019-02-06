import numpy as np


class Graph:
    """A Graph is a list of vertices and a list of edges"""
    def __init__(self, V=[], E=[]):
        self.V = V
        self.E = E

    def add_vertex(self, v):
        self.V.append(v)

    def add_edge(self, e):
        self.E.append(e)

    def __str__(self):
        s = "Vertices:\n"
        for v in self.V:
            s += str(v) + "\n"
        s += "Edges:\n"
        for e in self.E:
            s += str(e) + "\n"

        return s


class Vertex:
    """A Vertex consists of a 2-tuple for position, `pos`, and a 2-tuple for
    displacement, `disp`."""
    def __init__(self, idx, pos=[0, 0], disp=[0, 0], radius=10, random=False, width=200, height=200):
        # TODO: allow for random instantiation of position
        if random is True:
            self.radius = np.random.randint(4, 25)
            x = np.random.randint(self.radius, width-self.radius)
            y = np.random.randint(self.radius, height-self.radius)
            self.pos = np.array([x, y])
        else:
            self.radius = radius
            self.pos = np.array(pos)

        # self.radius = radius
        self.disp = np.array(disp)
        self.idx = idx

    def __str__(self):
        return "idx = {!s}, pos = {!s}, radius = {!s}, disp = {!s}".format(self.idx, self.pos, self.radius, self.disp)


class Edge:
    """An Edge consists of two instances of Vertex, `v1` and `v2`."""
    def __init__(self, v1=None, v2=None, k=1, random=False):
        # The 'spring' constant for the edge.
        if random is True:
            k = k*np.random.random()

        self.k = k
        self.v1 = v1
        self.v2 = v2

    def __str__(self):
        return "{!s} <--> {!s}".format(self.v1.idx, self.v2.idx)


def generate3():
    V = []
    E = []
    for i in range(3):
        v = Vertex(i, random=True)
        V.append(v)

    E.append(Edge(V[0], V[1]))
    E.append(Edge(V[0], V[2]))

    return Graph(V, E)


def generate6():
    """Generate a graph"""
    V = []
    E = []
    for i in range(6):
        v = Vertex(i, random=True)
        V.append(v)

    E.append(Edge(V[0], V[1], k=1/2, random=True))
    E.append(Edge(V[0], V[3], k=1/2, random=True))
    E.append(Edge(V[0], V[4], k=1/2, random=True))
    E.append(Edge(V[1], V[2], k=1/2, random=True))
    E.append(Edge(V[2], V[5], k=1/2, random=True))
    E.append(Edge(V[4], V[5], k=1/2, random=True))

    return Graph(V, E)


if __name__ == '__main__':
    G = generate6()
    print(G)
