import pygame
from pygame.locals import *
from scenes.scene import Scene
from utils import pygame_utils
from game_objects.game_object import GameObject
from game_objects.text import Text


class GameOverScene(Scene):
    def __init__(self, controller, last_frame, win=False):
        super().__init__(controller)
        last_frame = GameObject(
            self.game_objects, last_frame.get_rect(), last_frame
        )
        self.background.blit(last_frame)
        if win:
            title_str = "Congratulations!"
            title = Text(title_str, self._font, (40, 255, 40))
        else:
            title_str = "GAME OVER"
            title = Text(title_str, self._font, (255, 40, 40))

        sub_str = "press ESC to quit"
        sub_str2 = "press any other key to try again..."

        sub1 = Text(sub_str, self._small_font, (20, 20, 20))
        sub2 = Text(sub_str2, self._small_font, (20, 20, 20))

        title.rect.center = (400, 200)
        sub1.rect.center = (400, 400)
        sub2.rect.center = (400, 500)
        self.title = title
        self.game_objects.add(
            title, sub1, sub2
        )

    def handle_events(self, events):
        for event in events:
            if event.type == KEYDOWN:
                from scenes.minesweeper_scene import MinesweeperScene
                self.set_scene(MinesweeperScene)

    def update(self, ms):
        return super().update(ms)

    def render(self, screen):
        return super().render(screen)
