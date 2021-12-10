# Render an image of the data for day 9 of AOC 2021, Smoke Basin
# https://adventofcode.com/2021/day/9

# Based on, https://stackoverflow.com/questions/12423601/simplest-way-to-plot-3d-surface-given-3d-points

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

f = open('input.txt')
t = f.read()
f.close()

x, y = 0, 0

Xs, Ys, Zs = [], [], []

for row in t.split('\n'):
    for height in row:
        Xs.append(x)
        Ys.append(y)
        Zs.append(int(height))
        x += 1
    x = 0
    y += 1

my_colour_map = plt.get_cmap('gist_earth')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_trisurf(Xs, Ys, Zs, cmap=my_colour_map, linewidth=0)
fig.colorbar(surf)

ax.xaxis.set_major_locator(MaxNLocator(5))
ax.yaxis.set_major_locator(MaxNLocator(5))
ax.zaxis.set_major_locator(MaxNLocator(10))

fig.tight_layout()

plt.show()
