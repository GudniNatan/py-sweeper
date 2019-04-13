import os
import pygame
from game_objects.game_object import GameObject
from utils.pygame_utils import aspect_scale


class Tile(GameObject):
    TILE_SIZE = (35, 35)

    def __init__(self, name, location_point=None, revealed=False):
        super().__init__([], pygame.Rect(0, 0, 0, 0))
        self.revealed = revealed
        self.type = name
        self.marked = False
        self.set_face("hidden")
        self.x = 0
        self.y = 0
        if location_point is not None:
            self.set_position(location_point)
        if revealed:
            self.reveal()

    def set_face(self, type_name):
        self.image = pygame.image.load(
            os.path.join('spritesheet', f'{type_name}.png')
        )
        self.image = aspect_scale(self.image, self.TILE_SIZE)
        self.rect.size = self.TILE_SIZE

    def reveal(self):
        self.set_face(self.type)
        self.revealed = True
        return self.type

    def toggle_mark(self):
        if self.revealed:
            return
        self.set_face("hidden" if self.marked else "flag")
        self.marked = not self.marked
