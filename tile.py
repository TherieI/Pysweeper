import pygame
from dataclasses import dataclass

@dataclass
class TileContents:
    VALUE: int
    FLAGGED: bool = False
    DESTROYED: bool = False
    sprites = None

    def get_image(self):
        return TileContents.sprites[self.VALUE]

    @staticmethod
    def init_sprites():  # cant load images before pygame.init() and the display has been set so this exists
        TileContents.sprites = {
            -2: pygame.image.load("assets/tile_clear.png").convert(),
            -1: pygame.image.load("assets/bomb.png").convert(),
            0: pygame.image.load("assets/tile.png").convert(),
            1: pygame.image.load("assets/tile_numbers/tile_1.png").convert(),
            2: pygame.image.load("assets/tile_numbers/tile_2.png").convert(),
            3: pygame.image.load("assets/tile_numbers/tile_3.png").convert(),
            4: pygame.image.load("assets/tile_numbers/tile_4.png").convert(),
            5: pygame.image.load("assets/tile_numbers/tile_5.png").convert(),
            6: pygame.image.load("assets/tile_numbers/tile_6.png").convert(),
            7: pygame.image.load("assets/tile_numbers/tile_7.png").convert(),
            8: pygame.image.load("assets/tile_numbers/tile_8.png").convert()
        }


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

    def draw(self, screen):
        screen.blit(self.cont.get_image(), self.rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

