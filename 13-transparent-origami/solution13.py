# Solution to day 13 of AOC 2021, Transparent Origami
# https://adventofcode.com/2021/day/13

f = open('input.txt')
t = f.read()
f.close()

raw_dots, raw_folds = t.split('\n\n')

dots = set()


def print_dots():
    for dy in range(max_y + 1):
        for dx in range(max_x + 1):
            if (dx, dy) in dots:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()


for raw_dot in raw_dots.split('\n'):
    raw_x, raw_y = raw_dot.split(',')
    dots.add((int(raw_x), int(raw_y)))

max_x, max_y = 0, 0
for px, py in dots:
    max_x, max_y = max(px, max_x), max(py, max_y)

print(len(dots))

for instruction in raw_folds.split('\n'):
    raw_axis, raw_position = instruction.split('=')

    axis = raw_axis[-1]
    position = int(raw_position)

    new_dots = set()
    for x, y in dots:
        if axis == 'x':
            if x < position:
                new_dots.add((x, y))
            elif x > position:
                new_dots.add((2 * position - x, y))
            max_x = position - 1

        else:
            if y < position:
                new_dots.add((x, y))
            elif y > position:
                new_dots.add((x, 2 * position - y))
            max_y = position - 1

    dots = new_dots.copy()
    print(len(dots))

print_dots()
