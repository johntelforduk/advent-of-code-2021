# Solution to day 17 of AOC 2021, Trick Shot
# https://adventofcode.com/2021/day/17

def detect_boundaries(t: dict) -> tuple:
    dx_min, dx_max, dy_min, dy_max = None, None, None, None
    for di, dy in t:
        if dx_min is None:
            dx_min, dx_max, dy_min, dy_max = di, di, dy, dy
        else:
            dx_min = min(dx_min, di)
            dx_max = max(dx_max, di)
            dy_min = min(dy_min, dy)
            dy_max = max(dy_max, dy)

    return dx_min, dx_max, dy_min, dy_max


def print_trench(t: dict):
    px_min, px_max, py_min, py_max = detect_boundaries(t)
    for print_y in range(py_max, py_min - 1, -1):
        for print_x in range(px_min, px_max + 1):
            if (print_x, print_y) in trench:
                print(t[(print_x, print_y)], end='')
            else:
                print('.', end='')
        print()
    print()


f = open('input.txt')
t = f.read()
f.close()

print(t)

parts = t.split(' ')
xs = parts[2].split('..')
ys = parts[3].split('..')

from_x, to_x = int(xs[0][2:]), int(xs[1][:-1])
from_y, to_y = int(ys[0][2:]), int(ys[1])
print(from_x, to_x, from_y, to_y)

trench = {}
trench[(0, 0)] = 'S'

best = None
best_xv = None
solutions = set()

for xi in range(from_x, to_x + 1):
    for yi in range(from_y, to_y + 1):
        trench[(xi, yi)] = 'T'

_, max_x, min_y, _ = detect_boundaries(trench)

for start_yv in range(-1000, 1000):
    print(start_yv, best, len(solutions))

    for start_xv in range(0, 1000):

        # print(start_yv, start_xv)

        x, y = 0, 0
        max_height = 0
        xv, yv = start_xv, start_yv

        hit_target = False
        while x <= max_x and y >= min_y and not hit_target:
            x += xv             # The probe's x position increases by its x velocity.
            y += yv             # The probe's y position increases by its y velocity.

            # The probe's x velocity changes by 1 toward the value 0.
            if xv > 0:          # it decreases by 1 if it is greater than 0
                xv -= 1
            elif xv < 0:        # increases by 1 if it is less than 0
                xv += 1

            yv -= 1             # Due to gravity, the probe's y velocity decreases by 1.

            if max_height is None:
                max_height = y
            else:
                max_height = max(max_height, y)

            if (x, y) in trench and trench[x, y] == 'T':
                hit_target = True
                solutions.add((start_xv, start_yv))
                if best is None:
                    best = max_height
                    best_xv = start_xv
                else:
                    best = max(best, max_height)
                    best_xv = min(best_xv, start_xv)

print('Part 1:', best)
print('Part 2:', len(solutions))
