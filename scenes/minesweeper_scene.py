from random import shuffle
import pygame
from pygame.locals import *
from scenes.scene import Scene
from utils import pygame_utils, chain_reveal
from game_objects.game_object import GameObject
from game_objects.tile import Tile


class MinesweeperScene(Scene):
    def __init__(self, controller):
        super().__init__(controller)
        self.tile_count = (20, 14)
        self.tile_offset = (40, 100)
        self.mine_count = 20
        self.unrevealed = self.tile_count[0] * self.tile_count[1]
        self.tiles = self.make_tiles()
        self.place_tiles()
        self.game_objects.add(*self.tiles)

    def make_tiles(self):
        tile_x, tile_y = self.tile_count
        normal_count = self.unrevealed - self.mine_count
        tiles = [Tile("mine") for _ in range(self.mine_count)]
        tiles += [Tile("0") for _ in range(normal_count)]
        shuffle(tiles)
        formatted = list()
        for i in range(tile_x):
            formatted.append(list())
            for j in range(tile_y):
                cur = tiles[tile_y * i + j]
                cur.x, cur.y = i, j
                formatted[i].append(cur)
        return formatted

    def place_tiles(self):
        off_x, off_y = self.tile_offset
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                tile.rect.topleft = (
                    i * tile.TILE_SIZE[0] + off_x,
                    j * tile.TILE_SIZE[1] + off_y
                )
                self.set_tile_level(tile, i, j)

    def set_tile_level(self, tile, x, y):
        tile_level = 0
        if tile.type == "mine":
            return
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0 or i + x < 0 or j + y < 0:
                    continue
                try:
                    if self.tiles[i + x][j + y].type == "mine":
                        tile_level += 1
                except IndexError:
                    pass
        tile.type = str(tile_level)

    def handle_events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.left_click(event.pos)
            if event.type == MOUSEBUTTONDOWN and event.button != 1:
                self.right_click(event.pos)

    def left_click(self, position):
        for x, row in enumerate(self.tiles):
            for y, tile in enumerate(row):
                if tile.rect.collidepoint(position):
                    self.reveal_tile(tile, x, y)
                    return

    def right_click(self, position):
        for row in self.tiles:
            for tile in row:
                if tile.rect.collidepoint(position):
                    tile.toggle_mark()
                    return

    def reveal_tile(self, tile, x, y):
        if tile.revealed:
            return
        tile.reveal()
        self.unrevealed -= 1
        if tile.type == "mine":
            # game over
            print("game over")
        elif tile.type == "0":
            # chain reveal
            chain_reveal.chain_reveal(self.tiles, tile)

    def update(self, ms):
        return super().update(ms)

    def render(self, screen):
        return super().render(screen)
