import pygame
from pygame.locals import *
from scenes.scene import Scene
from utils import pygame_utils
from game_objects.game_object import GameObject
from game_objects.text import Text
from scenes.minesweeper_scene import MinesweeperScene


class DifficultySelectionScene(Scene):
    def __init__(self, controller):
        super().__init__(controller)
        title_str = "Choose difficulty"
        title = Text(title_str, self._font)

        padding = (5, 20, 5, 20)
        background = (100, 100, 100)
        easy = Text("Easy", self._small_font, padding=padding)
        medium = Text("Medium", self._small_font, padding=padding)
        hard = Text("Hard", self._small_font, padding=padding)

        easy.rect.center = (400, 400)
        medium.rect.center = (400, 450)
        hard.rect.center = (400, 500)
        title.rect.center = (400, 200)
        self.selected = easy
        self.menu = [easy, medium, hard]
        self.select(easy)
        self.game_objects.add(
            title, easy, medium, hard
        )

    def handle_events(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                self.set_scene(MinesweeperScene, self.selected.text)
            elif event.type == KEYDOWN and event.key == K_RETURN:
                self.set_scene(MinesweeperScene, self.selected.text)
            elif event.type == KEYDOWN and event.key == K_UP:
                index = self.menu.index(self.selected) - 1
                self.select(self.menu[index])
            elif event.type == KEYDOWN and event.key == K_DOWN:
                index = (self.menu.index(self.selected) + 1) % len(self.menu)
                self.select(self.menu[index])
            elif event.type == MOUSEMOTION:
                for obj in self.menu:
                    if obj.rect.collidepoint(event.pos):
                        self.select(obj)

    def select(self, item):
        for obj in self.menu:
            obj.set_border(0)
        item.set_border(5)
        self.selected = item

    def update(self, ms):
        return super().update(ms)

    def render(self, screen):
        return super().render(screen)
