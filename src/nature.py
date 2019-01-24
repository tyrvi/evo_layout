import numpy as np
from graph import generate


def nature(graph, width=200, length=200, iterations=100, temp=1, cool=lambda t: t):
    """
    Graph drawing by forced-directed placement.
    temp is the maximum displacement of a given vertex on an iteration which
    is annealed over time with the cooling function
    """
    C = 1  # constant used for tuning the spring constant
    area = width * length
    k = C * np.sqrt(area/len(graph.V))

    # attractive force
    def fa(d): return (d*d) / k

    # repulsive force
    def fr(d): return -(k*k) / d

    for i in range(iterations):
        # calculate repulsive forces
        x = input("Iteration {}: ".format(i))
        if x != "":
            break

        for v1 in graph.V:
            v1.disp = np.zeros(2)
            for v2 in graph.V:
                if v1 is not v2:
                    d = v1.pos - v2.pos
                    norm = np.linalg.norm(d)
                    print("d = {}, norm = {},\nv1 = {!s}\nv2 = {!s}".format(d, norm, v1, v2))
                    v1.disp = v1.disp + (d / norm) * fr(norm)

        # calculate attractive forces
        for e in graph.E:
            d = e.v1.pos - e.v2.pos
            norm = np.linalg.norm(d)
            e.v1.disp = e.v1.disp - (d/norm)*fa(norm)
            e.v2.disp = e.v2.disp + (d/norm)*fa(norm)

        # limit the maximum displacement using a temperature
        for v in graph.V:
            """
            For some reason the algorithm in the paper normalizes the
            displacement and multiplies by the minimum of the temperature and
            the norm to remove the norm. I think this way is much more
            efficient.
            """
            v.pos = v.pos + v.disp*temp
            # prevent from being moved outside the frame
            v.pos[0] = min(width/2, max(-width/2, v.pos[0]))
            v.pos[1] = min(length/2, max(-length/2, v.pos[1]))

        temp = cool(temp)

    return graph


if __name__ == '__main__':
    G = generate()
    print(G)
    G = nature(G, iterations=5)
    print(G)
