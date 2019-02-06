import numpy as np
from graph import generate6
# from util import pause


def nature(graph, width=500, height=500, iterations=100, temp=1, cool=lambda t: np.exp(-t)):
    """
    Graph drawing by forced-directed placement.
    temp is the maximum displacement of a given vertex on an iteration which
    is annealed over time with the cooling function
    """
    C = 10  # constant used for tuning the spring constant
    area = width * height
    K = C * np.sqrt(area/len(graph.V))

    # attractive force
    # def fa(d): return (d*d) / k
    # def fa(d): return k*np.log(d)
    # def fa(d): return d/k
    def fa(d, k): return (k*d*d) / K

    # repulsive force
    # def fr(d): return k / (d*d)
    # def fr(d): return (k*k) / d
    # def fr(d): return -k/d
    def fr(d, r1, r2): return K*(r1+r2) / (d*d)

    for i in range(iterations):
        # calculate repulsive forces
        # if not pause("Iteration {}: ".format(i)):
        #     break
        # print("Calculature repulsive forces:\n")
        for v1 in graph.V:
            v1.disp = np.zeros(2)
            for v2 in graph.V:
                if v1 is not v2:
                    d = v1.pos - v2.pos
                    norm = np.linalg.norm(d)
                    # v1.disp = v1.disp + (d / norm) * fr(norm)
                    v1.disp = v1.disp + (d / norm) * fr(norm, v1.radius, v2.radius)

                    # print("d = {}, norm = {},\nv1 {!s}\nv2 {!s}".format(d, norm, v1, v2))

        # print("Calculature attractive forces:\n")
        # calculate attractive forces
        for e in graph.E:
            d = e.v1.pos - e.v2.pos
            norm = np.linalg.norm(d)
            e.v1.disp = e.v1.disp - (d/norm)*fa(norm, e.k)
            e.v2.disp = e.v2.disp + (d/norm)*fa(norm, e.k)
            
            # print("d = {}, norm = {},\nv1 {!s}\nv2 {!s}".format(d, norm, e.v1, e.v2))

        # limit the maximum displacement using a temperature
        for v in graph.V:
            """
            For some reason the algorithm in the paper normalizes the
            displacement and multiplies by the minimum of the temperature and
            the norm to remove the norm. I think this way is much more
            efficient.
            """
            norm = np.linalg.norm(v.disp)
            v.pos = v.pos + (v.disp/norm) * temp
            # prevent being displaced outside of the frame which only
            # has positive coordinates
            v.pos[0] = min(width-v.radius, max(v.radius, v.pos[0]))
            v.pos[1] = min(height-v.radius, max(v.radius, v.pos[1]))
            # v.pos[0] = min(width, max(0, v.pos[0]))
            # v.pos[1] = min(height, max(0, v.pos[1]))

        temp = cool(temp)

    return graph


if __name__ == '__main__':
    G = generate6()
    print(G)
    G = nature(G, iterations=5)
    print(G)
