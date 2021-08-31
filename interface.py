import time

import config
import colors
from tile import Tile
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.display import set_caption, set_icon
from pygame.font import SysFont
from pygame.image import load
from pygame.transform import scale
from pygame.mouse import get_pos as get_mouse_pos
from pygame.mouse import get_pressed as mouse_pressed
from threading import Thread
from time import sleep


class Interface:
    MENU = 0
    GAME = 1
    END_W = 2
    END_L = 3

    def __init__(self):
        self.mode = Interface.MENU
        self.menu = GameMenu()
        self.game = Game()
        self.end = GameEnd()

    def set_mode(self, mode):
        self.mode = mode
        if mode == Interface.GAME:
            self.game.init_timer()
        elif mode == Interface.END_W or mode == Interface.END_L:
            self.game.pause_timer()
            self.end.set_stats(mode, self.game.elapsed)

    def load_basic(self):
        set_caption("Pysweeper")
        set_icon(load("assets/icon.png").convert())


class GameMenu:
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

        self.elapsed = 0
        self.count_seconds = True

    def draw_stats(self, screen):
        mines_left = self.font.render(f"Mines: {config.GameMode.get_mines_from_difficulty(config.game_mode) - Tile.total_flagged}", True, colors.DARK_RED)
        screen.blit(self.background, (config.padding["LEFT"], 10))
        screen.blit(mines_left, (config.padding["LEFT"] + 120, 25))

        _time = self.font.render(f"Time: {self.elapsed}s", True, colors.DARK_RED)
        screen.blit(_time, (config.padding["LEFT"] + config.resolution.x - 280, 25))

    def init_timer(self):
        self.elapsed = 0
        self.count_seconds = True
        timer_thread = Thread(target=self.timer, daemon=True)
        timer_thread.start()

    def timer(self):
        while self.count_seconds:
            sleep(1)
            self.elapsed += 1

    def pause_timer(self):
        self.count_seconds = False


class GameEnd:
    def __init__(self):
        self.font = SysFont("Courier New", 24)
        self.font.bold = True

        self.end_state = None
        self.time_elapsed = None

        background = load("assets/tile_clear.png").convert()
        self.background = scale(background, config.resolution.padded)

        retry_txt = self.font.render(f"Retry", True, colors.DARK_RED)
        retry = Surface((100, 50))
        retry.fill(colors.DARK_GREY)
        retry.blit(retry_txt, (0, 0))
        self.btn_retry = Button(retry)

        menu_txt = self.font.render(f"Menu", True, colors.DARK_RED)
        menu = Surface((100, 50))
        menu.fill(colors.DARK_GREY)
        menu.blit(menu_txt, (0, 0))
        self.btn_menu = Button(menu)

    def set_stats(self, state, elapsed):
        if state == Interface.END_W:
            s = "Win"
        else:
            s = "Loss"
        self.end_state = self.font.render(f"{s}", True, colors.DARK_RED)
        self.time_elapsed = self.font.render(f"Total time: {elapsed}s", True, colors.DARK_RED)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.btn_retry.draw(screen, (275, 350))
        self.btn_menu.draw(screen, (435, 350))
        screen.blit(self.end_state, (350, 250))
        screen.blit(self.time_elapsed, (300, 300))


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
