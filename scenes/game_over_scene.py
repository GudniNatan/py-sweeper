import pygame
from pygame.locals import *
from scenes.scene import Scene
from utils import pygame_utils
from game_objects.game_object import GameObject
from game_objects.tile import Tile
from scenes.minesweeper_scene import MinesweeperScene


class MenuScene(Scene):
    def __init__(self, controller, last_frame):
        super().__init__(controller)
        self.background.image = last_frame
        title_str = "GAME OVER"
        sub_str = "press ESC to quit"
        sub_str2 = "press any other key to try again..."
        title_text = self._font.render(title_str, True, (255, 255, 255))
        title_text.set_alpha(100)
        title_text_rect = title_text.get_rect()
        title_text_rect.center = (400, 200)

        sub_text = self._small_font.render(sub_str, True, (20, 20, 20))
        sub_text.set_alpha(100)
        sub_text_rect = sub_text.get_rect()
        sub_text_rect.center = (400, 400)

        sub_text2 = self._small_font.render(sub_str2, True, (20, 20, 20))
        sub_text2.set_alpha(100)
        sub_text2_rect = sub_text2.get_rect()
        sub_text2_rect.center = (400, 500)

        title = GameObject(self.game_objects, title_text_rect, title_text)
        sub1 = GameObject(self.game_objects, sub_text_rect, sub_text)
        sub2 = GameObject(self.game_objects, sub_text2_rect, sub_text2)
        self.game_objects.add(
            title, sub1, sub2
        )

    def handle_events(self, events):
        for event in events:
            if event.type == KEYDOWN:
                self.set_scene(MinesweeperScene)

    def update(self, ms):
        return super().update(ms)

    def render(self, screen):
        return super().render(screen)
