import numpy as np
import config
from tile import Tile, TileContents
from pygame import draw
from pygame.rect import Rect

# minesweeper spawn documentation: https://dspace.cvut.cz/bitstream/handle/10467/68632/F3-BP-2017-Cicvarek-Jan-Algorithms%20for%20Minesweeper%20Game%20Grid%20Generation.pdf

class Grid:
    def __init__(self):
        self.dimensions = config.GameMode.EASY
        self.grid = np.full(self.dimensions, Tile)

    def new_grid(self):



        #  Tile dimensions
        rect_width, rect_height = (
            int(config.resolution.x/self.dimensions.x),
            int(config.resolution.y/self.dimensions.y)
        )

        for x, y in np.ndindex(self.dimensions):
            # pygame.rect.Rect((position), (width/length))
            rect = Rect(
                (x*rect_width + config.padding["LEFT"], y*rect_height + config.padding["TOP"]),
                (rect_width, rect_height)
            )
            self.grid[x, y] = Tile(x, y, TileContents(0), rect)

    def draw(self, screen):
        for x, y in np.ndindex(self.grid.shape):
            tile = self.get_tile(x, y)
            tile.draw(screen)

    def get_tile(self, x, y):
        if 0 <= x < self.dimensions.x and 0 <= y < self.dimensions.y:
            return self.grid[x, y]
        return None

    def get_total_mines(self):
        mine_count = 0
        for ix, iy in np.ndindex(self.basic_grid.shape):
            if self.basic_grid[ix][iy] == -1:
                mine_count += 1
        return mine_count
