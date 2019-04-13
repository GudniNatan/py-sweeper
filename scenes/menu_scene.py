import pygame
from pygame.locals import *
from scenes.scene import Scene
from utils import pygame_utils
from game_objects.game_object import GameObject
from game_objects.tile import Tile
from scenes.minesweeper_scene import MinesweeperScene


class MenuScene(Scene):
    def __init__(self, controller):
        super().__init__(controller)
        title_str = "py-sweeper"
        sub_str = "press any key to continue..."
        title_text = self._font.render(title_str, True, (255, 255, 255))
        title_text = pygame_utils.pad(title_text, (0, 100), (255, 100, 100))
        title_text_rect = title_text.get_rect()
        title_text_rect.center = (400, 200)

        sub_text = self._small_font.render(sub_str, True, (20, 20, 20))
        sub_text_rect = sub_text.get_rect()
        sub_text_rect.center = (400, 400)

        mine = Tile("mine", revealed=True)
        mine.rect.center = (400, 300)

        title = GameObject(self.game_objects, title_text_rect, title_text)
        sub = GameObject(self.game_objects, sub_text_rect, sub_text)
        self.game_objects.add(
            title, sub, mine
        )

    def handle_events(self, events):
        for event in events:
            if event.type == KEYDOWN:
                self.set_scene(MinesweeperScene)

    def update(self, ms):
        return super().update(ms)

    def render(self, screen):
        return super().render(screen)
