import pygame
import sys
import config
from numpy import ndindex as np_iter
from tile import Tile
from grid import Grid


class Minesweeper:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode(config.resolution.xy)
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
            self.clock.tick(20)
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
            if start_button_rect.collidepoint(self.mouse_pos) == 1:
                self.screen.blit(self.on_hover, (130, 530))
            self.screen.blit(self.start_button, (165, 570))
            pygame.display.update()
        self.run()

    def run(self):
        self.create_tiles()

        while True:
            self.clock.tick(20)
            self.screen.fill((230, 230, 230))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # where all clicking events take place
                    self.mouse_click_events(event)
            if self.round_over:
                self.complete()
            self.draw_grid()
            self.draw_stats()
            pygame.display.update()
        self.reset_map()
        self.run_menu()

    def reset_map(self):
        self.round_over = False
        Tile.total_flagged = 0
        self.initial_mine = True

    def mouse_click_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed(5)[0]: # user drawing cells
            for x, y in np_iter(self.grid.shape): # iterating using np (gaming)
                if self.grid.get_tile(x, y).rect.collidepoint(mouse_pos):
                    self.grid.set_cell(x, y, self.draw_type)

    def create_tiles(self):
        Tile.tiles = []
        for x in range(int(self.display_size[0]/self.block_size)):
            Tile.tiles.append([])
            for y in range(int(self.display_size[1]/self.block_size)-1):
                tile = Tile(self.screen, (x*self.block_size, y*self.block_size+50))
                print(tile.position)
                Tile.tiles[-1].append(tile)

    def setup_map(self, initial_pos):
        self.map.lay_mines(initial_pos)
        self.total_mines = self.map.get_total_mines()
        self.grid = self.map.get_full_grid()
        self.set_tile_values()

    def set_tile_values(self):
        for ix, iy in np_iter(self.grid.grid.shape):
            tile = Tile.tile_from_position((ix * 50, iy * 50 + 50), (16, 16))
            tile.value = self.grid[ix][iy]

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

    def draw_grid(self):
        for x in range(int(self.display_size[0]/self.block_size)):
            for y in range(int(self.display_size[1]/self.block_size)-1):
                Tile.tiles[x][y].set((x*self.block_size, y*self.block_size+50))
