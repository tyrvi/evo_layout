import pygame
from pygame import gfxdraw


def draw_example():
    pygame.init()
    size = (600, 600)
    screen = pygame.display.set_mode(size)
    white = pygame.Color('white')
    black = pygame.Color('black')

    done = False
    clock = pygame.time.Clock()
    fps = 40

    gfxdraw.filled_circle(screen, 610, 238, 14, white)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        clock.tick(fps)
        pygame.display.flip()


def draw_graph(graph):
    raise(NotImplementedError("draw_graph has not been implemented yet"))

    
if __name__ == '__main__':
    draw_example()
