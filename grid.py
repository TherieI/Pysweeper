import config
from tile import Tile, TileContents
from pygame.rect import Rect
from random import randint

# minesweeper spawn documentation: https://dspace.cvut.cz/bitstream/handle/10467/68632/F3-BP-2017-Cicvarek-Jan-Algorithms%20for%20Minesweeper%20Game%20Grid%20Generation.pdf

class Grid:
    def __init__(self):
        self.dimensions = config.GameMode.EASY
        self.grid = []
        self.mine_count = 40
        self.running = False

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
            return self.grid[x][y]
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
                tile = Tile(x, y, rect, TileContents(-2))
                self.grid[x].append(tile)

    def get_neighbors_of(self, tile, cardinal_only=True):
        x, y = tile.xy
        # cardinal neighbors only
        neighbors = list(filter(None.__ne__, [  # None.__ne__ function checking if a value is not None, filtering NoneType (tiles out of bound)
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

    def fast_clear_around(self, tile):
        flagged_count = 0
        for neighbor in self.get_neighbors_of(tile, cardinal_only=False):
            if neighbor.cont.FLAGGED:
                flagged_count += 1
        if flagged_count == tile.get_value():
            for neighbor in self.get_neighbors_of(tile, cardinal_only=False):
                if neighbor.get_value() == 0:
                    self.clear_area(neighbor)
                neighbor.cont.CLEARED = True

    def clear_area(self, initial_tile):
        if initial_tile.get_value() != 0:  # to make sure area clearing doesnt run when a number tile is clicked
            initial_tile.cont.CLEARED = True
            self.fast_clear_around(initial_tile)
            return
        initial_tile.cont.CLEARED = True
        # breadth algorithm to clear an area
        frontier = [initial_tile]
        scanned = set()
        while len(frontier) != 0:
            current = frontier.pop(0)
            neighbors = self.get_neighbors_of(current, cardinal_only=False)
            neighbors.append(current)  # necessary to clear area around current tile
            for tile in neighbors:  # looping through clear tiles
                if tile.get_value() == 0 and tile not in scanned:
                    for num_tile in self.get_neighbors_of(tile, cardinal_only=False):
                        num_tile.cont.CLEARED = True
                    frontier.append(tile)
                    scanned.add(tile)

    def gen_values(self):
        for x in range(self.dimensions.x):
            for y in range(self.dimensions.y):
                tile = self.get_tile(x, y)
                mines_around = 0
                if not tile.is_mine():
                    neighbors = self.get_neighbors_of(tile, cardinal_only=False)
                    for neighbor in neighbors:
                        if neighbor.is_mine():
                            mines_around += 1
                    tile.set_value(mines_around)

    def fill_grid(self, initial_tile):  # runs breadth algorithm from initial tile mined, each cycle mines get more commonly spawned

        spawn_chance = -10
        mines_left = self.mine_count
        total_tiles = self.dimensions.x * self.dimensions.y
        tiles_to_mines = int(total_tiles/mines_left)

        count = 0

        frontier = [initial_tile]
        scanned = set()
        while len(frontier) != 0:
            current = frontier.pop(0)
            for tile in self.get_neighbors_of(current):
                if tile not in scanned:
                    # Determines whether tile will become a mine
                    spawn_chance += 1
                    tile.set_value(-2)
                    if randint(0, tiles_to_mines) == 1 and spawn_chance > 0:
                        count += 1
                        tile.set_value(-1)
                    frontier.append(tile)
                    scanned.add(tile)
        print(f"{count=}")
        self.gen_values()
