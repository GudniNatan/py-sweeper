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
        background_color = (240, 240, 240)
        padding = (5, 5, 5, 5)
        if win:
            title_str = "Congratulations!"
            title_color = (40, 255, 40,)
        else:
            title_str = "GAME OVER"
            title_color = (255, 40, 40)

        title = Text(title_str, self._font, title_color, border=3,
                     background_color=background_color, padding=padding)

        sub_str = "press ESC to quit"
        sub_str2 = "press any other key to try again..."

        sub1 = Text(sub_str, self._small_font, (20, 20, 20), border=3,
                    background_color=background_color, padding=padding)
        sub2 = Text(sub_str2, self._small_font, (20, 20, 20), border=3,
                    background_color=background_color, padding=padding)

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
                from scenes import difficulty_selection_scene as df
                self.set_scene(df.DifficultySelectionScene)

    def update(self, ms):
        return super().update(ms)

    def render(self, screen):
        return super().render(screen)
