import pygame
from pygame import draw
from pygame import freetype
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi
from shapely.geometry import Polygon
import matplotlib.patches as patches
from util import ROOM_COLORS, create_color_legend_handles
import graph
import nature


def draw_graph(graph, size=(500, 500), i=0, prefix=''):
    ax = plt.gca()
    ax.set_xlim(0, size[0])
    ax.set_ylim(0, size[1])
    for v in graph.V:
        circle = plt.Circle((v.pos[0], v.pos[1]), radius=v.radius, fc=ROOM_COLORS[v.room_type], alpha=0.4)
        ax.add_patch(circle)
        # ax.text(v.pos[0], v.pos[1], str(v.idx), fontsize=12)

    for e in graph.E:
        line = plt.Line2D((e.v1.pos[0], e.v2.pos[0]),
                          (e.v1.pos[1], e.v2.pos[1]), color='black')
        ax.add_line(line)

    plt.gca().legend(handles=create_color_legend_handles(), bbox_to_anchor=(1.1, 1.05))
    plt.axis('scaled')
    plt.axis('off')
    fig = plt.gcf()
    fig.set_size_inches(10, 10)
    dpi = 200
    plt.savefig("/home/thais/ws/evo/samples/graph-{}{}.pdf".format(prefix, i), dpi=dpi, bbox_inches='tight')
    plt.savefig("/home/thais/ws/evo/samples/graph-{}{}.svg".format(prefix, i), dpi=dpi, bbox_inches='tight')
    plt.savefig("/home/thais/ws/evo/samples/graph-{}{}.png".format(prefix, i), dpi=dpi, bbox_inches='tight')
    plt.clf()
    # plt.show()


def draw_voronoi(graph, layout=None, lw=2, ps=2, i=0):
    points = np.array(graph.points)
    vor = Voronoi(points)
    regions, vertices = voronoi_finite_polygons_2d(vor)
    box = Polygon(layout)
    # colorize
    for r, region in enumerate(regions):
        polygon = vertices[region]
        # poly = Polygon(polygon)
        # poly = poly.intersection(box)
        # polygon = [p for p in poly.exterior.coords]
        plt.fill(*zip(*polygon), alpha=0.4, color=ROOM_COLORS[graph.room_types[r]])
        plt.gca().add_patch(patches.Polygon(polygon, linewidth=1, color='black', fill=False))

    c = 10
    bounds = [[vor.min_bound[0]-c, vor.min_bound[1]-c],
              [vor.max_bound[0]+c, vor.min_bound[1]-c],
              [vor.max_bound[0]+c, vor.max_bound[1]+c],
              [vor.min_bound[0]-c, vor.max_bound[1]+c]]
    plt.gca().add_patch(patches.Polygon(bounds, linewidth=3, color='black', fill=False))
    plt.plot(points[:, 0], points[:, 1], 'ko')
    plt.xlim(vor.min_bound[0] - 10, vor.max_bound[0] + 10)
    plt.ylim(vor.min_bound[1] - 10, vor.max_bound[1] + 10)

    # create legend
    plt.gca().legend(handles=create_color_legend_handles(), bbox_to_anchor=(1, 1))
    plt.axis('off')
    fig = plt.gcf()
    fig.set_size_inches(10, 10)
    dpi = 200
    plt.savefig("/home/thais/ws/evo/samples/layout{}.pdf".format(i), dpi=dpi, bbox_inches='tight')
    plt.savefig("/home/thais/ws/evo/samples/layout{}.svg".format(i), dpi=dpi, bbox_inches='tight')
    plt.savefig("/home/thais/ws/evo/samples/layout{}.png".format(i), dpi=dpi, bbox_inches='tight')
    plt.clf()
    # plt.show()


def voronoi_finite_polygons_2d(vor, radius=None):
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.

    Parameters
    ----------
    vor : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.

    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.

    """

    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max()

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        # print("p1 = {}, region = {}".format(p1, region))
        vertices = vor.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = vor.points[p2] - vor.points[p1]  # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())

    return new_regions, np.asarray(new_vertices)


if __name__ == '__main__':
    # G = graph.generate6()
    i = 4
    G = graph.generate_example()
    print(G)
    draw_graph(G, i=i, prefix='before')
    G = nature.nature(G, iterations=250)
    print(G)
    draw_graph(G, i=i, prefix='after')
    points = [[0, 0], [400, 0], [400, 50], [500, 50],
              [500, 450], [400, 450], [400, 500], [0, 500]]
    draw_voronoi(G, points, i=i)


def draw_graph_pygame(graph, size=(500, 500)):
    pygame.init()
    screen = pygame.display.set_mode(size)
    white = pygame.Color('white')
    black = pygame.Color('black')
    screen.fill(white)

    font = freetype.SysFont("monospace", 10)

    done = False

    for v in graph.V:
        draw.circle(screen, black, (int(v.pos[0]), int(v.pos[1])), v.radius)
        font.render_to(screen, (int(v.pos[0]), int(v.pos[1])), str(v.idx))

    for e in graph.E:
        draw.line(screen, black, (int(e.v1.pos[0]), int(e.v1.pos[1])), (int(e.v2.pos[0]), int(e.v2.pos[1])))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.display.flip()
