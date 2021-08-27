import pygame
import sys
import config
from threading import Thread
from time import sleep
from tile import Tile, TileContents
from grid import Grid


class Minesweeper:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode(config.resolution.padded)

        TileContents.init_sprites()  # i dislike having to do this but i cant find a better way

        self.clock = pygame.time.Clock()
        self.grid = Grid()

        pygame.display.set_caption("Minesweeper")
        icon = pygame.image.load("assets/icon.png").convert()
        self.font = pygame.font.SysFont("malgungothic", 24)
        self.menu_screen = pygame.image.load("assets/minesweepermenu.png").convert()
        self.start_button = pygame.image.load("assets/start_button.png").convert()
        self.on_hover = pygame.image.load("assets/mouse_hover.png")
        pygame.display.set_icon(icon)

    def run_menu(self):
        start_button_rect = pygame.Rect((165, 570), (450, 100))
        menu = True
        while menu:
            self.clock.tick(config.fps)
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # where all clicking events take place
                    left_click = pygame.mouse.get_pressed(num_buttons=5)[0]
                    button_clicked = start_button_rect.collidepoint(mouse_pos)
                    if left_click and button_clicked:
                        menu = False
                    # print(f"right click: {right_click}")
                    # print(f"left click: {left_click}")
                    # print(f"Tile clicked: {tile_clicked.position}")

            self.screen.blit(self.menu_screen, (0, 0))
            if start_button_rect.collidepoint(mouse_pos) == 1:
                self.screen.blit(self.on_hover, (130, 530))
            self.screen.blit(self.start_button, (165, 570))
            pygame.display.update()
        self.run()

    def run(self):

        self.grid.new_grid()

        while True:
            self.clock.tick(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.click_event_handler(event)

            self.draw()

            pygame.display.update()

    def draw(self):
        self.screen.fill((230, 230, 230))
        self.grid.draw(self.screen)

    def click_event_handler(self, event):
        buttons_clicked = pygame.mouse.get_pressed(5)
        mouse_pos = pygame.mouse.get_pos()

        if buttons_clicked[0]:  # Left mouse button
            tile_clicked = self.grid.get_clicked(mouse_pos)
            if not self.grid.running:
                print("troll")
                self.grid.running = True
                self.grid.fill_grid(tile_clicked)
            if not tile_clicked.cont.FLAGGED:
                self.grid.clear_area(tile_clicked)

        elif buttons_clicked[2]:
            tile_clicked = self.grid.get_clicked(mouse_pos)
            print(f"{tile_clicked.xy=} {tile_clicked.get_value()=}")

    def complete(self):
        for row in Tile.tiles:
            for tile in row:
                tile.reveal()
        game_over = self.font.render(f"Game Over", True, (255, 0, 0))
        self.screen.blit(game_over, (400, 10))

    def draw_stats(self):
        total_mines_text = self.font.render(f"Total mines: {self.total_mines}", True, (255, 0, 0))
        self.screen.blit(total_mines_text, (20, 10))
        total_flagged = self.font.render(f"Total flagged: {Tile.total_flagged}", True, (255, 0, 0))
        self.screen.blit(total_flagged, (200, 10))
        tct = self.font.render(f"Tile clicked: {self.tc}", True, (255, 0, 0))
        self.screen.blit(tct, (400, 10))

