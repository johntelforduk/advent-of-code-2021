# Solution to day1 of AOC 2021, Dumbo Octopus
# https://adventofcode.com/2021/day/11

import pygame
import imageio                          # For making animated GIFs.


# k = (x, y)
# v = current value of octopus energy.
octopuses = {}

scale = 12

filenames = []


def print_octopuses(tick: int):
    print('After step', tick)
    for print_y in range(grid_y):
        for print_x in range(grid_y):
            print(octopuses[print_x, print_y], end='')
        print()
    print()


def render_octopuses(tick: int):
    background_colour = (0, 0, 0)           # Black.
    off_colour = (40, 40, 40)               # Grey
    on_colour = (255, 255, 255)             # White

    screen.fill(background_colour)

    for render_y in range(grid_y):
        for render_x in range(grid_x):
            if (render_x, render_y) in all_flashers:
                bulb = on_colour
            else:
                bulb = off_colour
            pygame.draw.circle(screen, color=bulb,
                               center=(scale + render_x * scale, scale + render_y * scale), radius=scale // 2.5)

    screenshot_name = 'screenshots/screen' + format(tick, '03') + '.png'
    pygame.image.save(screen, screenshot_name)
    filenames.append(screenshot_name)
    pygame.display.flip()


f = open('input.txt')
t = f.read()
f.close()

grid_x, grid_y = 0, 0
for row in t.split('\n'):
    grid_x = 0
    for position in row:
        octopuses[(grid_x, grid_y)] = int(position)
        grid_x += 1
    grid_y += 1


pygame.init()                                               # Initialize the game engine.

screen_size = [scale * (grid_x + 1), scale * (grid_y + 1)]  # [width, height]
screen = pygame.display.set_mode(screen_size)

print_octopuses(0)

# new_flashers = set()           # Flashes to be processed.
# all_flashers = set()           # All flashers in this generation.

total_flashers = 0

for step in range(1, 100 + 1):

    new_flashers = set()  # Flashes to be processed.
    all_flashers = set()  # All flashers in this generation.

    # First, the energy level of each octopus increases by 1.
    for grower in octopuses:
        octopuses[grower] += 1
        if octopuses[grower] > 9:
            new_flashers.add(grower)
            all_flashers.add(grower)

    # This process continues as long as new octopuses keep having their energy level increased beyond 9.
    while len(new_flashers) != 0:
        newest_flashers = set()
        for (x, y) in new_flashers:

            # Then, any octopus with an energy level greater than 9 flashes. This increases the energy level of all
            # adjacent octopuses by 1, including octopuses that are diagonally adjacent.
            for dx, dy in [(-1, -1), (0, -1), (1, -1),
                           (-1, 0),           (1, 0),
                           (-1, 1), (0, 1),   (1, 1)]:
                if x + dx >= 0 and x + dx + 1 <= grid_x and y + dy >= 0 and y + dy + 1 <= grid_y:
                    neighbour = (x + dx, y + dy)
                    octopuses[neighbour] += 1

                    if octopuses[neighbour] > 9:            # If this causes an octopus to have an energy level greater
                                                            # than 9, it also flashes.
                        if neighbour not in all_flashers:   # An octopus can only flash at most once per step.
                            newest_flashers.add(neighbour)
                            all_flashers.add(neighbour)
        new_flashers = newest_flashers.copy()

    # Finally, any octopus that flashed during this step has its energy level set to 0,
    # as it used all of its energy to flash.
    for this in all_flashers:
        octopuses[this] = 0

    print_octopuses(step)
    render_octopuses(step)

    total_flashers += len(all_flashers)

pygame.quit()

print(total_flashers)

images = []
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('day11.gif', images, fps=5)
