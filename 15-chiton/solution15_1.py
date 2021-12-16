# Solution to part 1 of day 15 of AOC 2021, Chiton
# https://adventofcode.com/2021/day/15

def find_least_risk(current: tuple, goal: tuple, visited: list, total_risk: int):

    global best

    # This search is getting too circuitous, so best to give up.
    # Why 220? Its greater than cavern_x + cavern_y which is length of shortest routes to goal (no backtracking).
    # The higher this number is, the longer the search takes. 220 is big enough to produce correct answer.
    # Greater than about 950, and Python recursion stack is likely to overflow.
    if len(visited) > 220:
        return

    # We've gone outside of the boundaries of the cavern.
    if current not in cavern:
        return

    # Abandon paths that visit a coordinate that we've been to before in this search.
    if current in visited:
        return

    total_risk += cavern[current]

    # Abandon paths that have greater total risk than previous best found.
    if current in best and best[current] <= total_risk:
        if current == (cavern_x, cavern_y):
            print(best[current])
        return

    # Exciting times... this is the best path to this coordinate so far!
    best[current] = total_risk

    # Great! We've reached the end.
    if current == goal:
        return

    # Let's continue the search.
    new_visited = visited.copy()
    new_visited.append(current)
    x, y = current
    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:                       # Search West, East, North and South.
        find_least_risk((x + dx, y + dy), goal, new_visited, total_risk)


cavern, best = {}, {}

f = open('input.txt')
t = f.read()
f.close()

cavern_x, cavern_y = 0, 0
for row in t.split('\n'):
    cavern_x = 0
    for risk in row:
        cavern[cavern_x, cavern_y] = int(risk)
        cavern_x += 1
    cavern_y += 1

# Fix a gatepost error.
cavern_x -= 1
cavern_y -= 1

cavern[(0, 0)] = 0

find_least_risk(current=(0, 0), goal=(cavern_x, cavern_y), visited=[], total_risk=0)

print(best[(cavern_x, cavern_y)])
