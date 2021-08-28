import pygame
import sys
import config
from interface import Interface
from tile import Tile
from grid import Grid


class Minesweeper:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode(config.resolution.padded)

        self.clock = pygame.time.Clock()
        self.grid = Grid()

        self.interface = Interface()
        self.interface.load_basic()

    def run_menu(self):
        running = True
        while running:
            self.clock.tick(config.fps)
            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    left_click = pygame.mouse.get_pressed(5)[0]
                    if left_click and self.interface.menu.button_clicked(mouse_pos):
                        running = False

            self.interface.menu.draw(self.screen)
            pygame.display.update()
        self.run()

    def run(self):
        self.grid.new_grid()
        while self.grid.is_alive():
            self.clock.tick(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.click_event_handler(event)
            self.draw_game()
            pygame.display.update()

    def draw_game(self):
        self.screen.fill((230, 230, 230))
        self.grid.draw(self.screen)

    def click_event_handler(self, event):
        buttons_clicked = pygame.mouse.get_pressed(5)
        mouse_pos = pygame.mouse.get_pos()

        tile_clicked = self.grid.get_clicked(mouse_pos)
        if tile_clicked is None:  # anything that isn't a tile will return None (the border)
            return
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if buttons_clicked[0]:  # Left mouse button
                if not self.grid.running:
                    self.grid.running = True
                    self.grid.fill_grid(tile_clicked)
                if not tile_clicked.cont.FLAGGED or not tile_clicked.cont.CLEARED:
                    self.grid.clear_area(tile_clicked)

            elif buttons_clicked[2]:  # Right mouse button
                tile_clicked.update_flag_state()

            elif buttons_clicked[1]:  # Middle mouse button
                print(f"{tile_clicked.xy=} {tile_clicked.get_value()=} {tile_clicked.cont=}")

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

