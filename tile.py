from pygame.image import load
from pygame.transform import scale
from config import Dimension
from dataclasses import dataclass

@dataclass
class TileContents:
    VALUE: int
    FLAGGED: bool = False
    CLEARED: bool = False
    images = None

    def get_image(self):
        if self.FLAGGED:
            return TileContents.images[-3]
        elif self.CLEARED:
            return TileContents.images[self.VALUE]
        return TileContents.images[-2]  # Cleared tile

    @staticmethod
    def init_images(game_mode: Dimension):  # initializes the sprites to the correct size for the gamemode
        TileContents.images = {
            -3: load("assets/tile_flag.png").convert(),
            -2: load("assets/tile.png").convert(),

            -1: load("assets/bomb.png").convert(),
            0: load("assets/tile_clear.png").convert(),
            1: load("assets/tile_numbers/tile_1.png").convert(),
            2: load("assets/tile_numbers/tile_2.png").convert(),
            3: load("assets/tile_numbers/tile_3.png").convert(),
            4: load("assets/tile_numbers/tile_4.png").convert(),
            5: load("assets/tile_numbers/tile_5.png").convert(),
            6: load("assets/tile_numbers/tile_6.png").convert(),
            7: load("assets/tile_numbers/tile_7.png").convert(),
            8: load("assets/tile_numbers/tile_8.png").convert()
        }
        constant_x, constant_y = game_mode.x/16, game_mode.y/16
        for img_id in TileContents.images.keys():
            img = TileContents.images[img_id]
            size = int(img.get_width()/constant_x), int(img.get_height()/constant_y)
            TileContents.images[img_id] = scale(img, size)

    def __str__(self):
        return f"{self.VALUE=} {self.FLAGGED=} {self.CLEARED=}"


class Tile:

    total_flagged = 0

    def __init__(self, x, y, rect, contents):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = rect
        self.cont = contents
        self.xy = x, y

    def set_value(self, value):
        self.cont.VALUE = value

    def get_value(self):
        return self.cont.VALUE

    def draw(self, screen):
        screen.blit(self.cont.get_image(), self.rect)

    def update_flag_state(self):
        if not self.cont.CLEARED:
            if self.cont.FLAGGED:
                Tile.total_flagged -= 1  # unflagging
            else:
                Tile.total_flagged += 1  # flagging
            self.cont.FLAGGED = not self.cont.FLAGGED

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def is_mine(self):
        return self.cont.VALUE == -1

