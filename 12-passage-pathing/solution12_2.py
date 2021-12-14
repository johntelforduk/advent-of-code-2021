# Solution to part 2 of day 12 of AOC 2021, Passage Pathing
# https://adventofcode.com/2021/day/12

def search(current_cave: str, visited: list):
    global all_routes

    visited = visited.copy()
    visited.append(current_cave)

    if current_cave == 'end':
        all_routes.append(visited)
        return

    for next_vertex in extra_caves[current_cave]:
        if next_vertex.isupper():                   # Large cave.
            search(current_cave=next_vertex, visited=visited)
        elif next_vertex not in visited:            # Unvisited, small cave.
            if '_extra' not in next_vertex:         # Unvisited, small cave, non-extra cave.
                search(current_cave=next_vertex, visited=visited)

            else:                                   # Unvisited, lower case, _extra cave.
                count_extras = 0

                parent_found = False
                parent = next_vertex.split('_')[0]

                for c in visited:
                    if '_extra' in c:
                        count_extras += 1
                    if c == parent:
                        parent_found = True
                if count_extras == 0 and parent_found:
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

for a in caves:
    extra_caves = [b + '_extra' for b in caves[a] if b.islower() and b not in ['start', 'end']]
    caves[a] = caves[a] + extra_caves

extra_caves = caves.copy()
for a in caves:
    if a.islower() and a not in ['start', 'end']:
        extra_caves[a + '_extra'] = caves[a]

print(extra_caves)

all_routes = []
search(current_cave='start', visited=[])
print(all_routes)
print(len(all_routes))
