import pygame
from pygame import gfxdraw


def draw():
    pygame.init()
    size = (600, 600)
    screen = pygame.display.set_mode(size)
    white = pygame.Color('white')
    black = pygame.Color('black')

    done = False
    clock = pygame.time.Clock()
    fps = 40

    gfxdraw.filled_circle(screen, 200, 200, 100, white)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        clock.tick(fps)
        pygame.display.flip()


def main():
    draw()


if __name__ == '__main__':
    main()
