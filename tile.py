import pygame
from dataclasses import dataclass

@dataclass
class TileContents:
    VALUE: int
    FLAGGED: bool = False
    CLEARED: bool = False
    sprites = None

    def get_image(self):
        if self.FLAGGED:
            return TileContents.sprites[-3]
        elif self.CLEARED:
            return TileContents.sprites[self.VALUE]
        return TileContents.sprites[-2]  # Cleared tile

    @staticmethod
    def init_sprites():  # cant load images before pygame.init() and the display has been set so this exists
        TileContents.sprites = {
            -3: pygame.image.load("assets/tile_flag.png").convert(),
            -2: pygame.image.load("assets/tile.png").convert(),

            -1: pygame.image.load("assets/bomb.png").convert(),
            0: pygame.image.load("assets/tile_clear.png").convert(),
            1: pygame.image.load("assets/tile_numbers/tile_1.png").convert(),
            2: pygame.image.load("assets/tile_numbers/tile_2.png").convert(),
            3: pygame.image.load("assets/tile_numbers/tile_3.png").convert(),
            4: pygame.image.load("assets/tile_numbers/tile_4.png").convert(),
            5: pygame.image.load("assets/tile_numbers/tile_5.png").convert(),
            6: pygame.image.load("assets/tile_numbers/tile_6.png").convert(),
            7: pygame.image.load("assets/tile_numbers/tile_7.png").convert(),
            8: pygame.image.load("assets/tile_numbers/tile_8.png").convert()
        }

    def __str__(self):
        return f"{self.VALUE=} {self.FLAGGED=} {self.CLEARED=}"


class Tile:

    total_flagged = 0
    tiles = []

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
            self.cont.FLAGGED = not self.cont.FLAGGED

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def is_mine(self):
        return self.cont.VALUE == -1

