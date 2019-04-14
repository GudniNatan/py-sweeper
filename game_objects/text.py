import pygame
from game_objects.game_object import GameObject
from utils import pygame_utils


class Text(GameObject):
    def __init__(self, text, font, color=(20, 20, 20), padding=(0, 0, 0, 0),
                 background_color=None, location=(0, 0), border=0):
        self.text = text
        self.font = font
        self.color = color
        self.padding = padding
        self.background_color = background_color
        super().__init__([], pygame.Rect(location, (0, 0)))
        self.image = font.render(text, True, color)
        if any(padding) or background_color is not None:
            self.image = pygame_utils.pad(
                self.image, padding, background_color
            )
        self.rect.size = self.image.get_rect().size
        self.borderless = self.image.copy()
        self.border = 0
        self.set_border(border)

    def render(self):
        new_text = Text(self.text, self.font, self.color,
                        self.padding, self.background_color)
        self.image = new_text.image
        self.rect.size = new_text.rect.size

    def set_border(self, width, color=(20, 20, 20)):
        if self.border == width:
            return
        if not self.border:
            self.borderless = self.image.copy()
        self.border = width
        borderless = self.borderless.copy()
        if width > 0:
            pygame.draw.rect(borderless, color, self.image.get_rect(), width)
        self.image.fill((255, 255, 255, 0))
        self.image.blit(borderless, (0, 0))
