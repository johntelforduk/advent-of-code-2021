# Solution to part 1 of day 15 of AOC 2021, Chiton
# https://adventofcode.com/2021/day/15

import sys

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

new_cavern = {}
for x, y in cavern:
    num = cavern[x, y]
    row_start = num
    for cy in range(5):
        next_num = row_start
        for cx in range(5):
            new_cavern[cx * cavern_x + x, cy * cavern_y + y] = next_num
            next_num += 1
            if next_num == 10:
                next_num = 1
        row_start += 1
        if row_start == 10:
            row_start = 1

cavern = new_cavern.copy()
cavern_x *= 5
cavern_y *= 5

# Fix a gatepost error.
cavern_x -= 1
cavern_y -= 1

source = (0, 0)
cavern[source] = 0

# Implemented pseudo code from, https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
# function Dijkstra(Graph, source):
#
# create vertex set Q
q, dist, prev = {}, {}, {}
# for each vertex v in Graph:
for v in cavern:
    # dist[v] ← INFINITY
    dist[v] = sys.maxsize
    # prev[v] ← UNDEFINED
    prev[v] = None
    # add v to Q
    q[v] = dist[v]
# dist[source] ← 0
dist[source] = 0

# while Q is not empty:
while len(q) is not 0:

    print('len(q):', len(q))

    # u ← vertex in Q with min dist[u]
    u = min(q, key=q.get)

    # remove u from Q
    del q[u]

    # for each neighbor v of u still in Q:
    x, y = u
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        v = (x + dx, y + dy)
        if v in q:

            # alt ← dist[u] + length(u, v)
            alt = dist[u] + cavern[v]

            # if alt < dist[v]:
            if alt < dist[v]:
                # dist[v] ← alt
                dist[v] = alt
                if v in q:
                    q[v] = alt
                # prev[v] ← u
                prev[v] = u

# return dist[], prev[]

print(dist[cavern_x, cavern_y])
