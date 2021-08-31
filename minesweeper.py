import pygame
import sys
import config
import colors
from interface import Interface
from grid import Grid
from tile import Tile


class Minesweeper:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode(config.resolution.padded)
        self.clock = pygame.time.Clock()
        self.grid = Grid()
        self.grid.new_grid()
        self.interface = Interface()
        self.interface.load_basic()

    def run(self):
        while True:
            self.clock.tick(config.fps)
            if self.interface.mode == Interface.MENU:
                self.run_menu()
            elif self.interface.mode == Interface.GAME:
                self.run_game()
            elif self.interface.mode == Interface.END_W or self.interface.mode == Interface.END_L:
                self.run_end()
            pygame.display.update()

    def run_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and self.interface.menu.start_button.is_clicked():
                self.interface.set_mode(Interface.GAME)
                self.grid.new_grid()
                return
        self.interface.menu.draw(self.screen)

    def run_game(self):
        if not self.grid.is_alive():
            self.interface.set_mode(Interface.END_L)
            self.grid.running = False
            return
        elif self.grid.has_won():
            self.interface.set_mode(Interface.END_W)
            self.grid.running = False
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.click_event_handler(event)
        self.draw_game()

    def run_end(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.interface.end.btn_retry.is_clicked():
                    self.interface.set_mode(Interface.GAME)
                    self.grid.new_grid()
                elif self.interface.end.btn_menu.is_clicked():
                    self.interface.set_mode(Interface.MENU)
        self.interface.end.draw(self.screen)

    def draw_game(self):
        self.screen.fill(colors.GREY)
        self.interface.game.draw_stats(self.screen)
        self.grid.draw(self.screen)

    def click_event_handler(self, event):
        buttons_clicked = pygame.mouse.get_pressed(5)
        mouse_pos = pygame.mouse.get_pos()
        tile_clicked = self.grid.get_clicked(mouse_pos)
        if tile_clicked is None:  # anything that isn't a tile will return None (the border)
            return
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if buttons_clicked[0]:  # Left mouse button
                if not tile_clicked.cont.FLAGGED:
                    if not self.grid.running:  # INITIAL CLICK (SPAWNS MINES)
                        self.grid.running = True
                        self.grid.fill_grid(tile_clicked)
                        Tile.total_flagged = 0
                    self.grid.clear_area(tile_clicked)
            elif buttons_clicked[2]:  # Right mouse button
                tile_clicked.update_flag_state()
            elif buttons_clicked[1]:  # Middle mouse button
                print(f"{tile_clicked.xy=} {tile_clicked.get_value()=} {tile_clicked.cont=}")

