import random
import pygame
from pygame import gfxdraw


def definePoints(numPoints, mapSize):
    points = []
    # we want to take a group of points that will fit on our map at random
    for typ in range(numPoints):
        # here's the random points
        x = random.randrange(0, mapSize)
        y = random.randrange(0, mapSize)
        # "type:" decides what point it is
        # x, y: location
        # citizens: the cells in our grid that belong to this point
        points.append([typ, x, y, []])

    # brute force-y but it works
    # for each cell in the grid
    for x in range(mapSize):
        for y in range(mapSize):
            # find the nearest point
            lowestDelta = (0, mapSize * mapSize)
            for p in range(len(points)):
                # for each point get the difference in distance
                # between our point and the current cell
                delta = abs(points[p][1] - x) + abs(points[p][2] - y)
                # store the point nearest if it's closer than the last one
                if delta < lowestDelta[1]:
                    lowestDelta = (p, delta)

            # push the cell to the nearest point
            activePoint = points[lowestDelta[0]]
            dx = x - activePoint[1]
            dy = y - activePoint[2]
            activePoint[3].append((dx, dy))

    return points


def main():
    pygame.init()
    size = (400, 400)
    screen = pygame.display.set_mode(size)
    white = pygame.Color('white')

    done = False
    clock = pygame.time.Clock()
    fps = 40

    points = definePoints(50, 400)

    # Draw the points before the while loop starts. No need to draw them again.
    for point in points:
        # Use different random colors for the points.
        color = (random.randrange(256), random.randrange(256),
                 random.randrange(256))
        for p in point[3]:
            # Draw the citizen points.
            # Add the offset of the citizen to the positions of the points.
            gfxdraw.pixel(screen, point[1]+p[0], point[2]+p[1], color)
        # draw white wherever there's a point.
        gfxdraw.pixel(screen, point[1], point[2], white)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        clock.tick(fps)
        pygame.display.flip()


if __name__ == '__main__':
    main()
