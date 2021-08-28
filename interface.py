import config
import colors
from tile import Tile
from pygame.sprite import Sprite
from pygame.display import set_caption, set_icon
from pygame.font import SysFont
from pygame.image import load
from pygame.transform import scale
from pygame.mouse import get_pos as get_mouse_pos
from pygame.mouse import get_pressed as mouse_pressed

class Interface:
    MENU = 0
    GAME = 1
    END = 2

    def __init__(self):
        self.mode = Interface.MENU
        self.menu = Menu()
        self.game = Game()

    def set_mode(self, mode):
        self.mode = mode

    def load_basic(self):
        set_caption("Pysweeper")
        set_icon(load("assets/icon.png").convert())


class Menu:
    def __init__(self):
        menu_screen = load("assets/minesweepermenu.png").convert()
        self.menu_screen = scale(menu_screen, config.resolution.padded)

        self.start_button = Button(load("assets/start_button.png").convert())
        self.on_hover = load("assets/mouse_hover.png")

    def draw(self, screen):
        screen.blit(self.menu_screen, (0, 0))
        # getting the correct position for the button on screen
        w, h = config.resolution.padded
        pos_x = int(w/2 - self.start_button.image.get_width()/2)
        pos_y = int(h*13/20)
        if self.start_button.mouse_hovering():
            screen.blit(self.on_hover, (pos_x-30, pos_y-40))  # wacky coords idk why i need to slightly edit them probably something to do with source image
        self.start_button.draw(screen, (pos_x, pos_y))


class Game:
    def __init__(self):
        self.background = scale(load("assets/tile_clear.png").convert(), (config.resolution.x, int(config.resolution.y/13)))  # yes I'm using the empty tile sprite for the background
        self.font = SysFont("Courier New", 24)
        self.font.bold = True

    def draw_stats(self, screen):
        text = self.font.render(f"Mines: {config.GameMode.get_mines_from_difficulty(config.game_mode) - Tile.total_flagged}", True, colors.DARK_RED)
        screen.blit(self.background, (config.padding["LEFT"], 10))
        screen.blit(text, (config.padding["LEFT"] + 120, 25))


class Button(Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = image.get_rect()

    def draw(self, screen, position: tuple[int, int]):
        self.rect.x, self.rect.y = position
        screen.blit(self.image, self.rect)

    def mouse_hovering(self):
        return self.rect.collidepoint(get_mouse_pos())

    def is_clicked(self):
        return self.rect.collidepoint(get_mouse_pos()) and mouse_pressed(num_buttons=5)[0]  # LMB







