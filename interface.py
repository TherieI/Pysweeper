import config
from pygame.display import set_caption, set_icon
from pygame.font import SysFont
from pygame.image import load
from pygame.transform import scale
from pygame.mouse import get_pos as get_mouse_pos

class Interface:

    MENU = 0
    GAME = 1

    def __init__(self):
        self.mode = Interface.MENU
        self.font = SysFont("Courier New", 24)
        self.menu = Menu()

    def set_mode(self, mode):
        self.mode = mode

    def load_basic(self):
        set_caption("Pysweeper")
        set_icon(load("assets/icon.png").convert())


class Menu:
    def __init__(self):
        menu_screen = load("assets/minesweepermenu.png").convert()
        self.menu_screen = scale(menu_screen, config.resolution.padded)

        self.start_button = load("assets/start_button.png").convert()
        self.on_hover = load("assets/mouse_hover.png")

    def draw(self, screen):
        screen.blit(self.menu_screen, (0, 0))
        start_btn_pos = self.get_button_pos()
        if self.start_button.get_rect(topleft=start_btn_pos).collidepoint(get_mouse_pos()):
            screen.blit(self.on_hover, (start_btn_pos[0]-30, start_btn_pos[1]-40))  # wacky coords idk why i need to slightly edit them probably something to do with source image
        screen.blit(self.start_button, start_btn_pos)

    def get_button_pos(self):
        w, h = config.resolution.padded
        button_x = int(w/2 - self.start_button.get_width()/2)
        button_y = int(h*13/20)
        return button_x, button_y

    def button_clicked(self, mouse_pos):
        start_btn_rect = self.start_button.get_rect(topleft=(self.get_button_pos()))
        return start_btn_rect.collidepoint(mouse_pos)





