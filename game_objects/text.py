import pygame
from game_objects.game_object import GameObject
from utils import pygame_utils


class Text(GameObject):
    def __init__(self, text, font, color, padding=None,
                 background_color=None, location=(0, 0)):
        self.text = text
        self.font = font
        self.color = color
        self.padding = padding
        self.background_color = background_color
        super().__init__([], pygame.Rect(location, (0, 0)))
        self.image = font.render(text, True, color)
        if padding is not None:
            self.image = pygame_utils.pad(
                self.image, padding, background_color
            )
        self.rect.size = self.image.get_rect().size

    def render(self):
        new_text = Text(self.text, self.font, self.color,
                        self.padding, self.background_color)
        self.image = new_text.image
        self.rect.size = new_text.rect.size
