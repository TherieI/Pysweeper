import numpy as np
import config
from tile import Tile, TileContents
from pygame import draw
from pygame.rect import Rect

# minesweeper spawn documentation: https://dspace.cvut.cz/bitstream/handle/10467/68632/F3-BP-2017-Cicvarek-Jan-Algorithms%20for%20Minesweeper%20Game%20Grid%20Generation.pdf

class Grid:
    def __init__(self):
        self.dimensions = config.GameMode.EASY
        self.count = 40
        self.grid = []

    def draw(self, screen):
        for x in range(self.dimensions.x):  # row major order
            for y in range(self.dimensions.y):
                tile = self.get_tile(x, y)
                tile.draw(screen)

    def get_clicked(self, mouse_pos):
        for x in range(self.dimensions.x):
            for y in range(self.dimensions.y):
                tile = self.get_tile(x, y)
                if tile.is_clicked(mouse_pos):
                    return tile

    def get_tile(self, x, y):
        if 0 <= x < self.dimensions.x and 0 <= y < self.dimensions.y:
            return self.grid[y][x]
        return None

    def new_grid(self):
        #  Tile dimensions
        rect_width, rect_height = (
            int(config.resolution.x/self.dimensions.x),
            int(config.resolution.y/self.dimensions.y)
        )
        self.grid = []
        for x in range(self.dimensions.x):  # row major order
            self.grid.append([])
            for y in range(self.dimensions.y):
                # pygame.rect.Rect((position), (width/length))
                rect = Rect(
                    (x*rect_width + config.padding["LEFT"], y*rect_height + config.padding["TOP"]),
                    (rect_width, rect_height)
                )
                tile = Tile(x, y, rect, TileContents(0))
                self.grid[x].append(tile)

    def get_neighbors_of(self, tile, cardinal_only=True):
        x, y = tile.xy
        # cardinal neighbors only
        neighbors = list(filter(None.__ne__, [  # None.__ne__ function checking if a value is not None, filtering NoneTyoe (tiles out of bound)
            self.get_tile(x - 1, y),
            self.get_tile(x + 1, y),
            self.get_tile(x, y - 1),
            self.get_tile(x, y + 1)
        ]))
        if not cardinal_only:
            # All 8 surrounding tiles
            neighbors += list(filter(None.__ne__, [
                self.get_tile(x - 1, y + 1),
                self.get_tile(x + 1, y + 1),
                self.get_tile(x - 1, y - 1),
                self.get_tile(x + 1, y - 1)
            ]))
        return neighbors

    def bomb(self, spawn_chance):
        def bias_function(num, bias=0.5):  # https://www.youtube.com/watch?v=lctXaT9pxA0&t=450s
            k = pow(1 - bias, 3)
            return (num * k) / (num * k - num + 1)


    def spawn_mines(self, initial_tile):  # runs breadth algorithm from initial tile mined, each cycle mines get more commonly spawned

        spawn_chance = -8
        mines_left = self.count
        total_tiles = self.dimensions.x * self.dimensions.y

        frontier = [initial_tile]
        scanned = set()
        while len(frontier) != 0:
            current = frontier.pop(0)
            for tile in self.get_neighbors_of(current):

                # do stuff with tile here
                tile.cont.VALUE = -2

                if tile not in list(scanned):
                    frontier.append(tile)
                    scanned.add(tile)
