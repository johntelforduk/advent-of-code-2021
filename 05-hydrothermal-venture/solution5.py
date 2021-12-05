# Solution to day 5 of AOC 2021, Hydrothermal Venture
# https://adventofcode.com/2021/day/5

f = open('input.txt')
t = f.read()
f.close()


def increment(x: int) -> int:
    """Return the delta (0, 1, or -1) that is needed to get from zero to the parm number in single unit increments."""
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0


# k = (x, y) coordinates of a place on the seabed.
# v = number of lines crossing that coordinate.
seabed = {}

# for row in t.split('\n'):
#     xxx = row.split(' -> ')
#     print(xxx)
#

for row in t.split('\n'):
    terms = row.split(' -> ')
    x1, y1 = tuple([int(cart) for cart in terms[0].split(',')])
    x2, y2 = tuple([int(cart) for cart in terms[1].split(',')])

    # For now, only consider horizontal and vertical lines.
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

count = 0
for (x, y) in seabed:
    if seabed[(x, y)] >= 2:
        count += 1

print(count)
