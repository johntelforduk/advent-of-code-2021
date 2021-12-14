# Solution to part 1 of day 12 of AOC 2021, Passage Pathing
# https://adventofcode.com/2021/day/12

def search(current_cave: str, visited: list):
    global all_routes

    visited = visited.copy()
    visited.append(current_cave)

    if current_cave == 'end':
        all_routes.append(visited)
        return

    for next_vertex in caves[current_cave]:
        if not next_vertex.islower() or next_vertex not in visited:
            search(current_cave=next_vertex, visited=visited)


f = open('input.txt')
t = f.read()
f.close()

caves = {}

for line in t.split('\n'):
    a, b = line.split('-')

    # Store from a -> b.
    if a in caves:
        caves[a].append(b)
    else:
        caves[a] = [b]

    # Also store from b -> a.
    if b in caves:
        caves[b].append(a)
    else:
        caves[b] = [a]

print(caves)

all_routes = []
search(current_cave='start', visited=[])
print(all_routes)
print(len(all_routes))
