import numpy as np
from util import RoomTypes, pause
import random
from numpy.random import choice


class Graph:
    """A Graph is a list of vertices and a list of edges"""
    def __init__(self, V=[], E=[]):
        self.V = V
        self.E = E
        self.points = []
        self.room_types = []
        for v in V:
            self.points.append([v.pos[0], v.pos[1]])
            self.room_types.append(v.room_type)

    def add_vertex(self, v):
        self.V.append(v)
        self.points.append([v.pos[0], v.pos[1]])

    def add_edge(self, e):
        self.E.append(e)

    # def is_connected(self):
    #     return len(self.dfs()) == len(self.V)

    # def dfs(self):
    #     stack = []
    #     random.seed(42)
    #     stack.append(random.choice(G.V))
    #     visited = []
    #     while len(stack) != 0:
    #         v = stack.pop()
    #         if v not in visited:
    #             visited.append(v)
    #             for a in self.get_adjacent(v):
    #                 stack.append(a)

    # def get_adjacent(self, v):
    #     adjacent = []
    #     for e in self.E:
    #         if v == e.v1:
    #             adjacent.append(e.v2)
    #         if v == e.v2:
    #             adjacent.append(e.v1)

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
    def __init__(self, idx, pos=[0, 0], disp=[0, 0], radius=10, random=False,
                 width=200, height=200, room_type=None):
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
        self.room_type = room_type

    def __str__(self):
        return "idx = {!s}, room type = {!s}, pos = ({:.2f}, {:.2f}), radius = {!s}, disp = {!s}".format(self.idx, self.room_type, self.pos[0], self.pos[1], self.radius, self.disp)


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
        return "{!s} <--> {!s}: ({:.2f}, {:.2f}) <--> ({:.2f}, {:.2f})".format(self.v1.idx, self.v2.idx, self.v1.pos[0], self.v1.pos[1], self.v2.pos[0], self.v2.pos[1])


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
        v = Vertex(i, random=True, room_type=random.choice(list(RoomTypes)))
        V.append(v)

    E.append(Edge(V[0], V[1], k=1/2, random=True))
    E.append(Edge(V[0], V[3], k=1/2, random=True))
    E.append(Edge(V[0], V[4], k=1/2, random=True))
    E.append(Edge(V[1], V[2], k=1/2, random=True))
    E.append(Edge(V[2], V[5], k=1/2, random=True))
    E.append(Edge(V[4], V[5], k=1/2, random=True))

    return Graph(V, E)


def dfs(G):
    stack = []
    # random.seed(42)
    stack.append(random.choice(G.V))
    visited = []
    while len(stack) != 0:
        v = stack.pop()
        if v not in visited:
            visited.append(v)
            for a in get_adjacent(G, v):
                stack.append(a)

    return visited


def get_adjacent(G, v):
    adjacent = []
    for e in G.E:
        if v == e.v1:
            adjacent.append(e.v2)
        elif v == e.v2:
            adjacent.append(e.v1)

    return adjacent


def is_connected(G):
    return len(dfs(G)) == len(G.V)


def generate_example():
    V = []
    E = []
    num_vertices = random.randrange(20, 30)
    choices = [RoomTypes.DINING, RoomTypes.KITCHEN,
               RoomTypes.LOUNGE, RoomTypes.SHOP]
    p = [0.4, 0.05, 0.35, 0.2]
    for i in range(num_vertices):
        # v = Vertex(i, random=True, room_type=random.choice(list(RoomTypes)))
        v = Vertex(i, random=True, room_type=choice(choices, 1, p=p)[0])
        V.append(v)

    G = Graph(V, E)
    while not is_connected(G):
        sample = random.sample(range(num_vertices), 2)
        # print(sample)
        if not duplicate_edge(E, sample):
            G.add_edge(Edge(V[sample[0]], V[sample[1]], k=1/2, random=True))
        # print(G)
        # pause()

    return G


def duplicate_edge(E, sample):
    for e in E:
        if (e.v1.idx == sample[0] and e.v2.idx == sample[1]) or (e.v1.idx == sample[1] and e.v2.idx == sample[0]):
            return True

    return False


if __name__ == '__main__':
    # G = generate6()
    G = generate_example()
    print(G)
    # print(is_connected(G))
