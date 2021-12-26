# Solution to part 1 of day 22 of AOC 2021, Reactor Reboot
# https://adventofcode.com/2021/day/22

f = open('input.txt')
t = f.read()
f.close()

grid = set()

for line in t.split('\n'):
    on_off, raw_ranges = line.split(' ')
    # print(on_off, raw_ranges)
    raw_x, raw_y, raw_z = raw_ranges.split(',')
    # print(raw_x, raw_y, raw_z)

    [from_x, to_x] = [int(term) for term in raw_x[2:].split('..')]
    [from_y, to_y] = [int(term) for term in raw_y[2:].split('..')]
    [from_z, to_z] = [int(term) for term in raw_z[2:].split('..')]

    in_range = False
    for check in [from_x, to_x, from_y, to_y, from_z, to_z]:
        if -50 <= check <= 50:          # considering only cubes in the region x=-50..50,y=-50..50,z=-50..50.
            in_range = True

    if in_range:
        for xi in range(from_x, to_x + 1):
            for yi in range(from_y, to_y + 1):
                for zi in range(from_z, to_z + 1):
                    if on_off == 'on':
                        grid.add((xi, yi, zi))
                    else:
                        if (xi, yi, zi) in grid:
                            grid.remove((xi, yi, zi))

    print(line, len(grid))

print(len(grid))