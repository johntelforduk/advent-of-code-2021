# Solution to part 2 of day 9 of AOC 2021, Smoke Basin
# https://adventofcode.com/2021/day/9


def search(search_x: int, search_y: int) -> int:
    """Starting at x, y... return the size of the basin found."""
    if (search_x, search_y) not in floor:
        return 0
    if floor[search_x, search_y] == 9:
        return 0

    floor[search_x, search_y] = 9

    size = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        size += search(search_x + dx, search_y + dy)

    return 1 + size


f = open('input.txt')
t = f.read()
f.close()

floor = {}
x, y = 0, 0

for row in t.split('\n'):
    for height in row:
        floor[(x, y)] = int(height)
        x += 1
    x = 0
    y += 1

print(floor)

basins = [search(x, y) for x, y in floor]

result = 1
for best in sorted(basins, reverse=True)[:3]:           # The top 3 largest basins.
    result *= best

print(result)
