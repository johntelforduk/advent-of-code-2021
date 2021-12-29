# Solution to day 23 of AOC 2021, Amphipod
# https://adventofcode.com/2021/day/23

import sys


def manhattan(t1b: tuple, t2b: tuple) -> int:
    """For parm pair of coordinate tuples, each (x, y). Return the Manhattan distance between them."""
    t1x, t1y = t1b
    t2x, t2y = t2b
    return abs(t1x - t2x) + abs(t1y - t2y)


def dict_hash(di: dict):
    # Based on one of the answers here, https://stackoverflow.com/questions/5884066/hashing-a-dictionary
    return hash(frozenset(di.items()))
    # return json.dumps(di)

def add_extras(positions: dict, species: str, rank: int) -> list:
    if positions[(rank, 3)] == species:
        return [(rank, 2), (rank, 3)]
    elif positions[(rank, 2)] == species:
        return [(rank, 2)]
    return []


class Burrow:
    def __init__(self, diagram: str):

        vertices = [
        (1, 1),  (2, 1),      (4, 1),      (6, 1),      (8, 1),      (10, 1),  (11, 1),
                        (3, 2),      (5, 2),      (7, 2),      (9, 2),
                        (3, 3),      (5, 3),      (7, 3),      (9, 3)]

        self.amphipods = {}

        self.home = []              # List of creatures that have made it home. When this is 8 length, all are home.

        # self.amphipods_start = {}

        x, y = 0, 0
        for c in diagram:
            if c in ['A', 'B', 'C', 'D']:
                self.create_amphipod(c, (x, y))
            x += 1
            if c == '\n':
                x = 0
                y += 1

        a_extras = [(3, 2), (3, 3)] + add_extras(self.amphipods, 'A', 5) + add_extras(self.amphipods, 'A', 7) + add_extras(self.amphipods, 'A', 9)
        b_extras = [(5, 2), (5, 3)] + add_extras(self.amphipods, 'B', 3) + add_extras(self.amphipods, 'B', 7) + add_extras(self.amphipods, 'B', 9)
        c_extras = [(7, 2), (7, 3)] + add_extras(self.amphipods, 'C', 3) + add_extras(self.amphipods, 'C', 5) + add_extras(self.amphipods, 'C', 9)
        d_extras = [(9, 2), (9, 3)] + add_extras(self.amphipods, 'D', 3) + add_extras(self.amphipods, 'D', 5) + add_extras(self.amphipods, 'D', 7)

        print(a_extras)
        print(b_extras)
        print(c_extras)
        print(d_extras)


        self.all_home_hash = dict_hash({(3, 2): 'A', (3,3): 'A', (5,2): 'B', (5,3): 'B', (7, 2): 'C', (7, 3): 'C', (9, 2): 'D', (9, 3): 'D'})

        # print(self.all_home_hash)
        # print(sys.maxsize)

        hallway = [(1, 1), (2, 1), (4, 1), (6, 1), (8, 1), (10, 1), (11, 1)]

        # k = Hashed value of dictionary of 8 creature positions.
        # v = The dictionary of their positions: k = position, v = species.
        self.graph = {}

        for a1 in hallway + a_extras:
            print(a1)
            for a2 in hallway + a_extras:
                for b1 in hallway + b_extras:
                    for b2 in hallway + b_extras:
                        for c1 in hallway + c_extras:
                            for c2 in hallway + c_extras:
                                for d1 in hallway + d_extras:
                                    for d2 in hallway + d_extras:
                                        # all = set()
                                        # all.add(a1)
                                        # all.add(a2)
                                        # all.add(b1)
                                        # all.add(b2)
                                        # all.add(c1)
                                        # all.add(c2)
                                        # all.add(d1)
                                        # all.add(d2)
                                        # # if len(all) == 8:
                                        # #     y += 1

                                        creatures = {}
                                        creatures[a1], creatures[a2] = 'A', 'A'
                                        creatures[b1], creatures[b2] = 'B', 'B'
                                        creatures[c1], creatures[c2] = 'C', 'C'
                                        creatures[d1], creatures[d2] = 'D', 'D'

                                        if len(creatures) == 8:         # Check that the 8 coordinates are disjoint.
                                            self.graph[dict_hash(creatures)] = creatures

        assert dict_hash({(5, 2): 'C', (7, 2): 'B', (9, 2): 'D', (3, 3): 'A', (5, 3): 'D', (7, 3): 'C', (9, 3): 'A', (2, 1): 'B'}) in self.graph

        edges_1_way = [(1, 1, 2, 1), (2, 1, 4, 1), (4, 1, 6, 1), (6, 1, 8, 1), (8, 1, 10, 1), (10, 1, 11, 1),

                       (2, 1, 3, 2), (4, 1, 3, 2), (4, 1, 5, 2), (6, 1, 5, 2), (6, 1, 7, 2), (8, 1, 7, 2),
                       (8, 1, 9, 2), (10, 1, 9, 2),

                       (3, 2, 3, 3), (5, 2, 5, 3), (7, 2, 7, 3), (9, 2, 9, 3)]

        # All edges are bi-directional. So work out the opposite directions.
        edges_2_ways = edges_1_way.copy()
        for xo, yo, xd, yd in edges_1_way:
            edges_2_ways.append((xd, yd, xo, yo))

        # k = Origin coordinates (x, y).
        # v = List of possible destinations from the origin, each (x, y).
        self.edges = {}
        for (xo, yo, xd, yd) in edges_2_ways:
            if (xo, yo) in self.edges:
                destinations = self.edges[(xo, yo)]
                destinations.append((xd, yd))
            else:
                self.edges[(xo, yo)] = [(xd, yd)]

        self.energy = 0             # Total energy used so far.
        # self.moves = 0

        # k = Tuple (x, y), the position of the creature.
        # v = species of creature ('A'... 'D').


        # self.amphipods_history = []

    # def reset(self):
    #     self.energy = 0             # Total energy used so far.
    #     self.amphipods = self.amphipods_start.copy()
    #     self.home = []

    def create_amphipod(self, species: str, position: (int, int)):
        self.amphipods[position] = species

    def in_hallway(self, position: (int, int)) -> bool:
        """Return True for creature at parm position iff it is in the hallway (not in a room)."""
        _, y = position
        if y == 1:
            return True
        return False

    # def is_home(self, position: (int, int)):
    #     """For the creature at parm position. If it is in one of its home positions, add it to the list of creatures
    #     that are home."""
    #     species = self.amphipods[position]
    #     home1 = {'A': (3, 2), 'B': (5, 2), 'C': (7, 2), 'D': (9, 2)}[species]
    #     home2 = {'A': (3, 3), 'B': (5, 3), 'C': (7, 3), 'D': (9, 3)}[species]
    #
    #     if position == home2:           # The most 'home' a creature can be! Doesn't matter what creature is home1.
    #         self.home.append(position)
    #
    #     # This creature in the 2nd best 'home'. It only counts as home, if same kind of creature as it is in home2.
    #     elif position == home1 and home2 in self.amphipods and self.amphipods[home2] == species:
    #         self.home.append(position)


    def possible_moves(self, position: (int, int), all_positions: dict) -> list:
        """For the creature at parm position. Return a list of its possible next moves."""

        # # If it is home, then there are no possible next moves.
        # if position in self.home:
        #     return []

        possible = self.edges[position].copy()
        # print(possible)

        # Discard moves to positions occupied by a creature.
        kill = []
        for candidate in possible:
            if candidate in all_positions:
                kill.append(candidate)

            # TODO
            # Amphipods will never move from the hallway into a room unless that room is their destination room and that
            # room contains no amphipods which do not also have that room as their own destination. If an amphipod's
            # starting room is not its destination room, it can stay in that room until it leaves the room. (For example,
            # an Amber amphipod will not move from the hallway into the right three rooms, and will only move into the
            # leftmost room if that room is empty or if it only contains other Amber amphipods.)

            else:       # Possible move from hallway to a home.
                if self.in_hallway(position) and not self.in_hallway(candidate):
                    species = all_positions[position]
                    home1 = {'A': (3, 2), 'B': (5, 2), 'C': (7, 2), 'D': (9, 2)}[species]
                    home2 = {'A': (3, 3), 'B': (5, 3), 'C': (7, 3), 'D': (9, 3)}[species]

                    if candidate not in [home1, home2]:
                        kill.append(candidate)

        for k in kill:
            possible.remove(k)

        # TODO
        # Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room. (That
        # is, once any amphipod starts moving, any other amphipods currently in the hallway are locked in place and
        # will not move again until they can move fully into a room.)

        return possible

    # def move(self, origin: (int, int), destination: (int, int)):
    #     species = self.amphipods[origin]
    #     energy_per_step = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}[species]
    #     self.energy += energy_per_step * manhattan(origin, destination)
    #     # self.moves += 1
    #     self.amphipods[destination] = species
    #     del self.amphipods[origin]
    #
    #     self.is_home(destination)       # Check if it is home.

    def distance(self, origin: (int, int), destination: (int, int), positions: dict):
        species = positions[origin]
        energy_per_step = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}[species]
        return energy_per_step * manhattan(origin, destination)






    # def validated_move(self, origin: (int, int), destination: (int, int)):
    #     if destination not in self.possible_moves(origin):
    #         print('Invalid move!')
    #     else:
    #         self.move(origin, destination)


    def print_burrow(self):
        graphic = """#############
#...........#
###.#.#.#.###
  #.#.#.#.#
  #########"""
        x, y = 0, 0
        for g in graphic:
            if (x, y) in self.amphipods:
                print(self.amphipods[x, y], end='')
            else:
                print(g, end='')
            x += 1
            if g == '\n':
                x = 0
                y += 1
        print('\nEnergy:', self.energy)
        print()


    def search(self):
        # Implemented pseudo code from, https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
        # function Dijkstra(Graph, source):

        # print(self.amphipods)
        source_hash = dict_hash(self.amphipods)

        # Need to add source to graph, as creatures are in positions at start that they wouldn't normally move to.
        self.graph[source_hash] = self.amphipods

        # print(self.graph[source_hash])
        # print('source_hash', source_hash)

        # graph[source] = 0

        #
        # create vertex set Q
        q, dist = {}, {}
        # for each vertex v in Graph:
        for v_hash in self.graph:
            # dist[v] ← INFINITY
            dist[v_hash] = sys.maxsize
            # # prev[v] ← UNDEFINED
            # prev[v_hash] = None
            # add v to Q
            q[v_hash] = dist[v_hash]
        # dist[source] ← 0
        dist[source_hash] = 0
        q[source_hash] = 0

        # while Q is not empty:
        while len(q) is not 0:

            # for i in dist:
            #     if dist[i] != sys.maxsize:
            #         print(i, self.graph[i], dist[i])
            print('len(q):', len(q))

            # u ← vertex in Q with min dist[u]
            u = min(q, key=q.get)
            # print(u)

            # print('u', u)

            # remove u from Q
            del q[u]

            # for each neighbor v of u still in Q:
            # x, y = u
            u_positions = self.graph[u]

            for u_creature in u_positions:
                species = u_positions[u_creature]
                for pick_move in self.possible_moves(u_creature, u_positions):

                    v_positions = u_positions.copy()
                    del v_positions[u_creature]
                    v_positions[pick_move] = species

                    v_hash = dict_hash(v_positions)

                    # print('u_creature', u_creature)
                    # print('pick_move', pick_move)
                    # print('species', species)
                    # print('u_positions', u_positions)
                    # print('v_positions', v_positions)

                    if v_hash in q:

                        # alt ← dist[u] + length(u, v)
                        # alt = dist[u] + cavern[v]
                        # print('dist[u]', dist[u])
                        # print('distance', self.distance(u_creature, pick_move, u_positions))

                        alt = dist[u] + self.distance(u_creature, pick_move, u_positions)
                        # print('alt', alt)

                        # if alt < dist[v]:
                        if alt < dist[v_hash]:
                            # dist[v] ← alt
                            dist[v_hash] = alt
                            if v_hash in q:
                                q[v_hash] = alt
                            # prev[v] ← u
                            # prev[v_hash] = u

        # return dist[], prev[]

        print(dist[self.all_home_hash])


# def search(tb: Burrow):
#     global best
#     global best_so_far
#
#     # tb.print_burrow()
#
#     # If all of the creatures are home, then we are done!
#     if len(tb.home) == len(tb.amphipods):
#         if tb.energy < best:
#             best = tb.energy
#             print(best)
#         return
#
#     # If we've exceeded the best energy total already, there's no need to continue the search.
#     if tb.energy >= best:
#         return
#
#     # Infeasible number of moves. Also must be less than Python recursion limits.
#     if tb.moves > 200:
#         return
#
#     # If all creatures are stuck, abandon the search.
#     stuck = True
#     for pick_creature in tb.amphipods:
#         if len(tb.possible_moves(pick_creature)) > 0:
#             stuck = False
#     if stuck:
#         return
#
#     hash_key = hash(frozenset(tb.amphipods.items()))
#     # print('len(best_so_far):', len(best_so_far))
#     if hash_key in best_so_far:
#         if tb.energy <= best_so_far[hash_key]:
#             best_so_far[hash_key] = tb.energy
#         else:
#             return
#     else:
#         best_so_far[hash_key] = tb.energy
#
#     # TODO For each creature in turn, do it's next move.
#     crs = list(tb.amphipods)
#     random.shuffle(crs)
#     for pick_creature in crs:
#         if pick_creature not in tb.home:
#             pms = tb.possible_moves(pick_creature)
#             random.shuffle(pms)
#             for pick_move in pms:
#                 nb = Burrow()
#                 nb.energy = tb.energy
#                 nb.moves = tb.moves
#                 nb.amphipods = tb.amphipods.copy()
#                 nb.amphipods_start = tb.amphipods_start.copy()
#                 nb.home = tb.home.copy()
#
#                 nb.move(pick_creature, pick_move)
#                 search(nb)

assert manhattan((3, 2), (2, 1)) == 2
assert manhattan((2, 1), (3, 2)) == 2
assert manhattan((11, 1), (10, 1)) == 1
assert manhattan((3, 2), (3, 3)) == 1

assert dict_hash({(3, 2): 'A', (3, 3): 'B'}) == dict_hash({(3, 2): 'A', (3, 3): 'B'})   # Not random.
assert dict_hash({(3, 2): 'A', (3, 3): 'B'}) == dict_hash({(3, 3): 'B', (3, 2): 'A'})   # Not random.

assert dict_hash({(3, 2): 'A', (3, 3): 'B'}) != dict_hash({(3, 2): 'A', (3, 4): 'B'})   # Change a key.
assert dict_hash({(3, 2): 'A', (3, 3): 'B'}) != dict_hash({(3, 2): 'A', (3, 3): 'C'})   # Change a value.

f = open('test.txt')
t = f.read()
f.close()

my_burrow = Burrow(diagram=t)
my_burrow.print_burrow()
my_burrow.search()

# my_burrow.amphipods_start = my_burrow.amphipods.copy()

# # (1, 1)  (2, 1)      (4, 1)      (6, 1)      (8, 1)      (10, 1)  (11, 1)
# #               (3, 2)      (5, 2)      (7, 2)      (9, 2)
# #               (3, 3)      (5, 3)      (7, 3)      (9, 3)
#
# my_burrow.validated_move((7, 2), (6, 1))
# my_burrow.validated_move((6, 1), (4, 1))
# my_burrow.print_burrow()
# my_burrow.validated_move((5, 2), (6, 1))
# my_burrow.validated_move((6, 1), (7, 2))
# my_burrow.print_burrow()
# my_burrow.validated_move((5, 3), (5, 2))
# my_burrow.validated_move((5, 2), (6, 1))
# my_burrow.validated_move((4, 1), (5, 2))
# my_burrow.validated_move((5, 2), (5, 3))
# my_burrow.print_burrow()
# my_burrow.validated_move((3, 2), (4, 1))
# my_burrow.validated_move((4, 1), (5, 2))
# my_burrow.print_burrow()
# my_burrow.validated_move((9, 2), (8, 1))
# my_burrow.validated_move((9, 3), (9, 2))
# my_burrow.validated_move((9, 2), (10, 1))
# my_burrow.print_burrow()
# my_burrow.validated_move((8, 1), (9, 2))
# my_burrow.validated_move((9, 2), (9, 3))
# my_burrow.validated_move((6, 1), (8, 1))
# my_burrow.validated_move((8, 1), (9, 2))
# my_burrow.print_burrow()
# my_burrow.validated_move((10, 1), (8, 1))
# my_burrow.validated_move((8, 1), (6, 1))
# my_burrow.validated_move((6, 1), (4, 1))
# my_burrow.validated_move((4, 1), (3, 2))
# my_burrow.print_burrow()
# assert my_burrow.energy == 12521
#
# my_burrow.reset()
#
# best_so_far = {}
#
# best = 50000            # This should be an easy best score to beat.
# search(my_burrow)
# print(best)

# my_burrow.print_burrow()

# best = None
#
# best_so_far = {}
#
# for attempt in range(50000000):
#     my_burrow.reset()
#
#     if (attempt % 1000) == 0:
#         print('Attempt, Best:', attempt, best)
#
#
#     stuck, poor = False, False
#     while len(my_burrow.home) < 8 and not stuck and not poor:              # 8 home means we are done.
#
#         stuck = True
#         for pick_creature in my_burrow.amphipods:
#             if len(my_burrow.possible_moves(pick_creature)) > 0:
#                 stuck = False
#
#         if not stuck:
#             pick_creature, next_moves = (0, 0), []
#             while len(next_moves) == 0 or pick_creature in my_burrow.home:
#                 pick_creature = random.choice(list(my_burrow.amphipods))
#                 next_moves = my_burrow.possible_moves(pick_creature)
#                 # print(pick_creature, next_moves)
#
#             pick_move = random.choice(next_moves)
#             # print(pick_creature, next_moves, pick_move)
#
#             my_burrow.move(pick_creature, pick_move)
#             # my_burrow.print_burrow()
#
#         hash_key = hash(frozenset(my_burrow.amphipods.items()))
#         # print('len(best_so_far):', len(best_so_far))
#         if hash_key in best_so_far:
#             if my_burrow.energy <= best_so_far[hash_key]:
#                 best_so_far[hash_key] = my_burrow.energy
#             else:
#                 poor = True
#         else:
#             best_so_far[hash_key] = my_burrow.energy
#
#         if best is not None and my_burrow.energy > best:
#             poor = True
#
#     if not stuck and not poor:
#         if best is None:
#             best = my_burrow.energy
#             print('Attempt, Best:', attempt, best)
#         else:
#             if my_burrow.energy < best:
#                 best = my_burrow.energy
#                 print('Attempt, Best:', attempt, best)

# print(my_burrow.possible_moves((3, 3)))
#
# my_burrow.move((3, 2), (2, 1))
#
# my_burrow.print_burrow()
