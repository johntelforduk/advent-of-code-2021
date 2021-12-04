# Solution to part 1 of day 2 of AOC 2021, Dive!
# https://adventofcode.com/2021/day/2

f = open('input.txt')
t = f.read()
f.close()

h, d = 0, 0
for command, units_raw in [line.split() for line in t.split('\n')]:
    units = int(units_raw)

    if command == 'down':
        d += units
    elif command == 'up':
        d -= units
    elif command == 'forward':
        h += units

print(h * d)
