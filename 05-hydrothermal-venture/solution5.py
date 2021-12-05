# Solution to day 5 of AOC 2021, Hydrothermal Venture
# https://adventofcode.com/2021/day/5

import pygame

f = open('input.txt')
t = f.read()
f.close()


def increment(num: int) -> int:
    """Return the delta (0, 1, or -1) that is needed to get from zero to the parm number in single unit increments."""
    if num < 0:
        return -1
    elif num > 0:
        return 1
    else:
        return 0


# k = (x, y) coordinates of a place on the seabed.
# v = number of lines crossing that coordinate.
seabed = {}

for row in t.split('\n'):
    terms = row.split(' -> ')
    x1, y1 = tuple([int(cart) for cart in terms[0].split(',')])
    x2, y2 = tuple([int(cart) for cart in terms[1].split(',')])

    # Part 1: For now, only consider horizontal and vertical lines.
    # if x1 == x2 or y1 == y2:

    xd = increment(x2 - x1)
    yd = increment(y2 - y1)

    print(terms)
    print(x1, y1, x2, y2, xd, yd)

    while x1 != x2 or y1 != y2:
        if (x1, y1) in seabed:
            seabed[(x1, y1)] += 1
        else:
            seabed[(x1, y1)] = 1

        x1 += xd
        y1 += yd

    if (x1, y1) in seabed:
        seabed[(x1, y1)] += 1
    else:
        seabed[(x1, y1)] = 1

for y in range(10):
    for x in range(10):
        if (x, y) in seabed:
            print(seabed[(x, y)], end='')
        else:
            print('.', end='')
    print()
print()

count, max_vents, max_x, max_y = 0, 0, 0, 0
for (x, y) in seabed:
    if seabed[(x, y)] >= 2:
        count += 1
    max_vents = max(max_vents, seabed[(x, y)])
    max_x = max(max_x, x)
    max_y = max(max_y, y)

print(count, max_vents, max_x, max_y)

screen_size = [max_x + 1, max_y + 1]  # [width, height]

pygame.init()                                               # Initialize the game engine.
screen = pygame.display.set_mode(screen_size)

background_colour = (255, 255, 255)
screen.fill(background_colour)

for (x, y) in seabed:
    intensity = 255 - 255 * seabed[(x, y)] // max_vents   # Normalise the colour intensity.
    colour = (intensity, intensity, intensity)
    screen.set_at((x, y), colour)

pygame.display.flip()

pygame.image.save(screen, 'screenshots/day5_2.jpg')

pygame.quit()
