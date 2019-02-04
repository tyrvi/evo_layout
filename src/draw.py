import pygame
from pygame import gfxdraw
from pygame import freetype
import graph
import nature


def draw_example():
    pygame.init()
    size = (600, 600)
    screen = pygame.display.set_mode(size)
    white = pygame.Color('white')
    black = pygame.Color('black')

    done = False
    clock = pygame.time.Clock()
    fps = 40

    gfxdraw.filled_circle(screen, 200, 200, 10, white)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # clock.tick(fps)
        pygame.display.flip()


def draw_graph(graph, size=(500, 500)):
    pygame.init()
    screen = pygame.display.set_mode(size)
    white = pygame.Color('white')

    font = freetype.SysFont("monospace", 10)

    done = False

    for v in graph.V:
        gfxdraw.filled_circle(screen, int(v.pos[0]), int(v.pos[1]), v.radius, white)
        font.render_to(screen, (int(v.pos[0]), int(v.pos[1])), str(v.idx))

    for e in graph.E:
        gfxdraw.line(screen, int(e.v1.pos[0]), int(e.v1.pos[1]), int(e.v2.pos[0]), int(e.v2.pos[1]), white)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.display.flip()


if __name__ == '__main__':
    G = graph.generate6()
    print(G)
    # draw_graph(G)
    G = nature.nature(G, iterations=1000)
    print(G)
    draw_graph(G)
