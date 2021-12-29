# Solution to day 23 of AOC 2021, Amphipod
# https://adventofcode.com/2021/day/23

import sys
import queue


def manhattan(t1b: tuple, t2b: tuple) -> int:
    """For parm pair of coordinate tuples, each (x, y). Return the Manhattan distance between them."""
    t1x, t1y = t1b
    t2x, t2y = t2b
    return abs(t1x - t2x) + abs(t1y - t2y)


def dict_hash(di: dict):
    # Based on one of the answers here, https://stackoverflow.com/questions/5884066/hashing-a-dictionary
    return hash(frozenset(di.items()))
    # return json.dumps(di)


def add_extras(positions: dict, species: str, column: int) -> list:
    if positions[(column, 3)] == species:
        return [(column, 2), (column, 3)]
    elif positions[(column, 2)] == species:
        return [(column, 2)]
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

                                        creatures = {}
                                        creatures[a1], creatures[a2] = 'A', 'A'
                                        creatures[b1], creatures[b2] = 'B', 'B'
                                        creatures[c1], creatures[c2] = 'C', 'C'
                                        creatures[d1], creatures[d2] = 'D', 'D'

                                        if len(creatures) == 8:         # Check that the 8 coordinates are disjoint.
                                            self.graph[dict_hash(creatures)] = creatures

        # assert dict_hash({(5, 2): 'C', (7, 2): 'B', (9, 2): 'D', (3, 3): 'A', (5, 3): 'D', (7, 3): 'C', (9, 3): 'A', (2, 1): 'B'}) in self.graph

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
        pq = queue.PriorityQueue()

        q = set()
        dist = {}
        # for each vertex v in Graph:
        for v_hash in self.graph:
            # dist[v] ← INFINITY
            dist[v_hash] = sys.maxsize
            # # prev[v] ← UNDEFINED
            # prev[v_hash] = None
            # add v to Q


            # XXXXXXXX

            if v_hash != source_hash:
                pq.put((dist[v_hash], v_hash))
                q.add(v_hash)

        # dist[source] ← 0
        dist[source_hash] = 0
        q.add(source_hash)
        pq.put((dist[source_hash], source_hash))

        # while Q is not empty:
        while not pq.empty():

            # for i in dist:
            #     if dist[i] != sys.maxsize:
            #         print(i, self.graph[i], dist[i])
            print('pq.qsize(), len(q):', pq.qsize(), len(q))

            # u ← vertex in Q with min dist[u]
            # u = min(q, key=q.get)
            _, u = pq.get()
            # print(u)

            # XXXXXXXX
            # if d <= dist[u]:
                # print('u', u)

            # remove u from Q
            if u in q:
                q.remove(u)

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
                                    pq.put((alt, v_hash))
                                # prev[v] ← u
                                # prev[v_hash] = u

        # return dist[], prev[]
        print(dist[self.all_home_hash])


assert manhattan((3, 2), (2, 1)) == 2
assert manhattan((2, 1), (3, 2)) == 2
assert manhattan((11, 1), (10, 1)) == 1
assert manhattan((3, 2), (3, 3)) == 1

assert dict_hash({(3, 2): 'A', (3, 3): 'B'}) == dict_hash({(3, 2): 'A', (3, 3): 'B'})   # Not random.
assert dict_hash({(3, 2): 'A', (3, 3): 'B'}) == dict_hash({(3, 3): 'B', (3, 2): 'A'})   # Not random.

assert dict_hash({(3, 2): 'A', (3, 3): 'B'}) != dict_hash({(3, 2): 'A', (3, 4): 'B'})   # Change a key.
assert dict_hash({(3, 2): 'A', (3, 3): 'B'}) != dict_hash({(3, 2): 'A', (3, 3): 'C'})   # Change a value.

f = open('input.txt')
t = f.read()
f.close()

my_burrow = Burrow(diagram=t)
my_burrow.print_burrow()
my_burrow.search()
