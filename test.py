import numpy as np

grid = [[2, 3, 3], [1, 3, 3], [1, 6, 3]]
grid_dim = (3, 3)

for x in range(grid_dim[0]):  # row major order
    for y in range(grid_dim[1]):
        pass
        # print(f"{grid[x][y]}")

coc = {
    "fart": 10,
    "yomama": 0
}

for e in coc.keys():
    print(type(e))