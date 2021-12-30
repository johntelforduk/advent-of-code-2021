# Solution to part 2 of day 23 of AOC 2021, Amphipod
# https://adventofcode.com/2021/day/23

import queue


def manhattan(t1b: tuple, t2b: tuple) -> int:
    """For parm pair of coordinate tuples, each (x, y). Return the Manhattan distance between them."""
    t1x, t1y = t1b
    t2x, t2y = t2b
    return abs(t1x - t2x) + abs(t1y - t2y)


def distance(origin: (int, int), destination: (int, int), positions: dict):
    species = positions[origin]
    energy_per_step = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}[species]
    return energy_per_step * manhattan(origin, destination)


def dict_hash(di: dict):
    # Based on one of the answers here, https://stackoverflow.com/questions/5884066/hashing-a-dictionary
    return hash(frozenset(di.items()))


def home_column(species: str) -> int:
    return {'A': 3, 'B': 5, 'C': 7, 'D': 9}[species]


def in_hallway(position: (int, int)) -> bool:
    _, row = position
    return row == 1


def other_species(species: str) -> list:
    return {'A': ['B', 'C', 'D'],
            'B': ['A', 'C', 'D'],
            'C': ['A', 'B', 'D'],
            'D': ['A', 'B', 'C']}[species]


# def print_burrow(creatures: dict):
#     graphic = """#############
# #...........#
# ###.#.#.#.###
#   #.#.#.#.#
#   #########"""
#     x, y = 0, 0
#     for g in graphic:
#         if (x, y) in creatures:
#             print(creatures[x, y], end='')
#         else:
#             print(g, end='')
#         x += 1
#         if g == '\n':
#             x = 0
#             y += 1
#     print()


def str_to_creatures(s: str) -> dict:
    creatures = {}
    x, y = 0, 0
    for c in s:
        if c in ['A', 'B', 'C', 'D']:
            creatures[(x, y)] = c
        x += 1
        if c == '\n':
            x = 0
            y += 1
    return creatures


def currently_reachable(position: (int, int), creature_positions: dict, found_so_far: list) -> list:
    """For the creature at parm position. Return list of all possible places it can reach right now."""

    # No move possible.
    if len(edges[position]) == 0:
        return []

    for candidate_pos in edges[position]:
        # Check no creature in the candidate position.
        # Also check it is not a position that we've found already.
        if candidate_pos not in creature_positions and candidate_pos not in found_so_far:
            found_so_far.append(candidate_pos)
            currently_reachable(candidate_pos, creature_positions, found_so_far)
    return found_so_far


def possible_moves(position: (int, int), all_positions: dict) -> list:
    """For the creature at parm position. Return a list of its possible next moves."""

    candidates_moves = currently_reachable(position, all_positions, [])
    valid_moves = []

    if in_hallway(position):
        species = all_positions[position]
        home_col = home_column(species)

        for this_candidate in candidates_moves:
            (x, y) = this_candidate
            if x == home_col:       # Will only move from hallway to its own home column.

                # Check there no creatures of other species in the home column.
                all_my_species = True
                for check_y in range(2, 5 + 1):
                    if (x, check_y) in all_positions:
                        if all_positions[x, check_y] in other_species(species):
                            all_my_species = False
                if all_my_species:

                    # Check row is first unoccupied one.
                    first_unoccupied = None
                    for check_y in range(5, 2 - 1, -1):
                        if first_unoccupied is None and (x, check_y) not in all_positions:
                            first_unoccupied = check_y
                    if y == first_unoccupied:
                        valid_moves.append(this_candidate)

    else:           # In a home. So only places to go are hallways.
        for this_candidate in candidates_moves:
            if in_hallway(this_candidate):
                valid_moves.append(this_candidate)

    return valid_moves

# (1, 1)  (2, 1)      (4, 1)      (6, 1)      (8, 1)      (10, 1)  (11, 1)
#               (3, 2)      (5, 2)      (7, 2)      (9, 2)
#               (3, 3)      (5, 3)      (7, 3)      (9, 3)
#               (3, 4)      (5, 4)      (7, 4)      (9, 4)
#               (3, 5)      (5, 5)      (7, 5)      (9, 5)


all_home_hash = dict_hash({(3, 2): 'A', (3,3): 'A', (5,2): 'B', (5,3): 'B', (7, 2): 'C', (7, 3): 'C', (9, 2): 'D', (9, 3): 'D'})

# hallway = [(1, 1), (2, 1), (4, 1), (6, 1), (8, 1), (10, 1), (11, 1)]

edges_1_way = [(1, 1, 2, 1), (2, 1, 4, 1), (4, 1, 6, 1), (6, 1, 8, 1), (8, 1, 10, 1), (10, 1, 11, 1),

               (2, 1, 3, 2), (4, 1, 3, 2), (4, 1, 5, 2), (6, 1, 5, 2), (6, 1, 7, 2), (8, 1, 7, 2),
               (8, 1, 9, 2), (10, 1, 9, 2),

               (3, 2, 3, 3), (5, 2, 5, 3), (7, 2, 7, 3), (9, 2, 9, 3),

               (3, 3, 3, 4), (5, 3, 5, 4), (7, 3, 7, 4), (9, 3, 9, 4),

               (3, 4, 3, 5), (5, 4, 5, 5), (7, 4, 7, 5), (9, 4, 9, 5)]

# All edges are bi-directional. So work out the opposite directions.
edges_2_ways = edges_1_way.copy()
for xo, yo, xd, yd in edges_1_way:
    edges_2_ways.append((xd, yd, xo, yo))

# k = Origin coordinates (x, y).
# v = List of possible destinations from the origin, each (x, y).
edges = {}
for (xo, yo, xd, yd) in edges_2_ways:
    if (xo, yo) in edges:
        destinations = edges[(xo, yo)]
        destinations.append((xd, yd))
    else:
        edges[(xo, yo)] = [(xd, yd)]


f = open('input2.txt')
t = f.read()
f.close()

amphipods = str_to_creatures(t)
# print(amphipods)
source_hash = dict_hash(amphipods)

# self.graph[source_hash] = self.amphipods

pq = queue.PriorityQueue()
unfinished = set()
discovered = {}
dist = {}
# for v_hash in self.graph:
#     dist[v_hash] = sys.maxsize
#
#     if v_hash != source_hash:
#         pq.put((dist[v_hash], v_hash))
#         unfinished.add(v_hash)

# dist[source] ← 0
dist[source_hash] = 0
unfinished.add(source_hash)
discovered[source_hash] = amphipods
pq.put((dist[source_hash], source_hash))

while not pq.empty():
    print('pq.qsize(), len(unfinished):', pq.qsize(), len(unfinished))
    _, u = pq.get()

    if u in unfinished:
        unfinished.remove(u)

        u_positions = discovered[u]

        for u_creature in u_positions:
            species = u_positions[u_creature]
            for pick_move in possible_moves(u_creature, u_positions):

                v_positions = u_positions.copy()
                del v_positions[u_creature]
                v_positions[pick_move] = species

                v_hash = dict_hash(v_positions)

                # print('u_creature', u_creature)
                # print('pick_move', pick_move)
                # print('species', species)
                # print('u_positions', u_positions)
                # print('v_positions', v_positions)

                alt = dist[u] + distance(u_creature, pick_move, u_positions)

                if v_hash in unfinished:
                    alt = dist[u] + distance(u_creature, pick_move, u_positions)

                    if alt < dist[v_hash]:
                        dist[v_hash] = alt
                        #
                        # if v_hash in unfinished:
                        pq.put((alt, v_hash))

                elif v_hash not in discovered:
                    discovered[v_hash] = v_positions
                    pq.put((alt, v_hash))
                    unfinished.add(v_hash)
                    dist[v_hash] = alt

home_diagram = """#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########"""

all_home_hash = dict_hash(str_to_creatures(home_diagram))

# print(str_to_creatures(home_diagram))
#
# print(all_home_hash)

print(dist[all_home_hash])

# print(len(unfinished), len(dist), len(discovered))
