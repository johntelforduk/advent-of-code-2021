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
            # print(next_num, end='')
            new_cavern[cx * cavern_x + x, cy * cavern_y + y] = next_num
            next_num += 1
            if next_num == 10:
                next_num = 1
        # print()
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

# function Dijkstra(Graph, source):
#
# create vertex set Q
q, dist, prev = [], {}, {}
# for each vertex v in Graph:
for v in cavern:
    # dist[v] ← INFINITY
    dist[v] = sys.maxsize
    # prev[v] ← UNDEFINED
    prev[v] = None
    # add v to Q
    q.append(v)
# dist[source] ← 0
dist[source] = 0

# while Q is not empty:
while len(q) is not 0:

    print('len(q):', len(q))

    # u ← vertex in Q with min dist[u]
    print(len(q), len(dist))
    u = None
    shortest = sys.maxsize
    for coords in q:
        if dist[coords] < shortest:
            shortest = dist[coords]
            u = coords

    # x = min(dist, key=dist.get)
    # print(x)

    # remove u from Q
    q.remove(u)

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
                # prev[v] ← u
                prev[v] = u

# return dist[], prev[]




# print()
# for py in range(cavern_y):
#     for px in range(cavern_x):
#         print(cavern[(px, py)], end='')
#     print()

# print(dist)
print(dist[cavern_x, cavern_y])
