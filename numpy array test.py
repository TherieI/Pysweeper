import numpy as np

grid = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
grid_dim = (3, 3)

for x, y in np.ndindex(grid_dim):
    print(f"{x=} {y=}")
