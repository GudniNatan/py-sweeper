import os
from random import shuffle
import pygame
from pygame.locals import *
from scenes.scene import Scene
from better_timers import timers
from utils import pygame_utils, chain_reveal
from game_objects.game_object import GameObject
from game_objects.tile import Tile
from game_objects.text import Text
from scenes.game_over_scene import GameOverScene


class MinesweeperScene(Scene):
    def __init__(self, controller, difficulty):
        super().__init__(controller)
        self.clock = 900000
        self.clock_text = Text(self.get_clock_str(), self._font, (20, 20, 20))
        self.clock_text.rect.center = (400, 50)
        if difficulty == "Easy":
            self.tile_count = (10, 10)
            self.tile_offset = (220, 150)
        elif difficulty == "Medium":
            self.tile_count = (14, 14)
            self.tile_offset = (150, 100)
        elif difficulty == "Hard":
            self.tile_count = (20, 14)
            self.tile_offset = (40, 100)
        self.unrevealed = self.tile_count[0] * self.tile_count[1]
        back_rect = pygame.Rect(
            self.tile_offset,
            (self.tile_count[0] * Tile.TILE_SIZE[0] + 1,
             self.tile_count[1] * Tile.TILE_SIZE[1] + 1)
        )
        self.backdrop = GameObject(self.game_objects, back_rect)
        self.mine_count = self.unrevealed // 8
        self.original_mine_count = self.mine_count
        self.unmarked = Text("x"+str(self.mine_count), self._small_font)
        self.unmarked.rect.center = (600, 50)

        mine_icon = pygame.image.load(
            os.path.join('spritesheet', f'mine.png')
        )
        mine_icon = pygame_utils.aspect_scale(mine_icon, (25, 25))
        mine_icon = GameObject(
            self.game_objects, mine_icon.get_rect(), mine_icon)
        mine_icon.rect.center = (550, 50)
        self.tiles = self.make_tiles()
        self.place_tiles()
        self.game_objects.add(self.backdrop, *self.tiles, self.clock_text,
                              self.unmarked, mine_icon)
        self.win_sound = pygame.mixer.Sound("sounds/ta da.wav")
        self.lose_sound = pygame.mixer.Sound("sounds/bomb.wav")

    def get_clock_str(self):
        minutes = self.clock // 60000
        seconds = (self.clock - (minutes * 60000)) // 1000
        return str(minutes).zfill(2) + ":" + str(seconds).zfill(2)

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
            elif event.type == MOUSEBUTTONDOWN and event.button != 1:
                self.right_click(event.pos)
            elif event.type == USEREVENT and event.code == "lose":
                self.reveal_all()
                self._Scene__controller.render(pygame.display.get_surface())
                self.set_scene(GameOverScene, pygame.display.get_surface())
                timers.set_timer(event, 0)
            elif event.type == USEREVENT and event.code == "win":
                self.reveal_all()
                self._Scene__controller.render(pygame.display.get_surface())
                self.set_scene(
                    GameOverScene, pygame.display.get_surface(), True
                )
                timers.set_timer(event, 0)

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
                    if tile.marked:
                        if self.mine_count <= 0:
                            tile.toggle_mark()
                        else:
                            self.mine_count -= 1
                    else:
                        self.mine_count += 1
                    self.unmarked.text = "x" + str(self.mine_count)
                    self.unmarked.render()
                    return

    def reveal_tile(self, tile, x, y):
        if tile.revealed or tile.marked:
            return
        print(self.unrevealed)
        self.unrevealed -= chain_reveal.chain_reveal(self.tiles, tile)
        print(self.unrevealed)
        if tile.type == "mine":
            # game over
            self.lose_sound.play()
            event = pygame.event.Event(USEREVENT, code="lose")
            timers.set_timer(event, 500)
        elif self.unrevealed == self.original_mine_count:
            # win!
            self.win_sound.play()
            event = pygame.event.Event(USEREVENT, code="win")
            timers.set_timer(event, 200)

    def reveal_all(self):
        for row in self.tiles:
            for tile in row:
                if tile.marked and tile.type != "mine" and not tile.revealed:
                    tile.type = "misplaced"
                tile.reveal()

    def update(self, ms):
        self.clock -= ms
        if self.clock <= 1000:
            event = pygame.event.Event(USEREVENT, code="lose")
            timers.set_timer(event, 200)
        return super().update(ms)

    def render(self, screen):
        clock_str = self.get_clock_str()
        if self.clock_text.text != clock_str:
            self.clock_text.text = self.get_clock_str()
            self.clock_text.render()
        return super().render(screen)
