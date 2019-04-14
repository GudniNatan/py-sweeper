from pathlib import Path
from abc import ABC, abstractmethod
import pygame
from pygame.sprite import LayeredUpdates, groupcollide
from pygame import ftfont
from utils.pygame_utils import fix_path
from game_objects.game_object import GameObject


class Scene(ABC):
    REGULAR_FONT = "fonts/Connection/Connection.otf"
    BOLD_FONT = "fonts/Connection/ConnectionBold.otf"

    def __init__(self, controller):
        try:
            open(self.REGULAR_FONT).close()
        except FileNotFoundError:
            fix_path()
        self._font = ftfont.Font(self.REGULAR_FONT, 50)
        self._small_font = ftfont.Font(self.REGULAR_FONT, 30)
        self._bold_font = ftfont.Font(self.BOLD_FONT, 30)
        self.__controller = controller
        try:
            self.__last_scene = controller.get_scene()
        except AttributeError:
            self.__last_scene = None
        self.game_objects = LayeredUpdates()
        self.screen_rect = pygame.display.get_surface().get_rect()
        background = pygame.Surface(self.screen_rect.size)
        background.fill((240, 240, 240))
        self.background = GameObject(
            self.game_objects, pygame.Rect(0, 0, 0, 0), background
        )
        self.game_objects.add(self.background)

    @abstractmethod
    def handle_events(self, events):
        pass

    @abstractmethod
    def update(self, ms):
        game_objects = self.game_objects
        game_objects.update(ms)
        collisions = groupcollide(game_objects, game_objects, False, False)
        for key, value in collisions.items():
            value.pop(0)
            if value:
                try:
                    key.collide(value)
                except AttributeError:
                    pass

    @abstractmethod
    def render(self, screen):
        return self.game_objects.draw(screen)

    def load(self):
        pass

    def back(self):  # return to last scene
        self.__controller.set_scene(self.__last_scene)

    def set_scene(self, SceneClass: 'Scene', *args):
        self.__controller.set_scene(SceneClass(self.__controller, *args))
