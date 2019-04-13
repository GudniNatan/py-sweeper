import pygame
from components.component import Component
from math import pi


class Sprite(Component):
    def __init__(self, game_object):
        super().__init__(game_object)
        try:
            self.physics = game_object.get_component(Physics)
        except TypeError:
            self.physics = None
        self.direction = 0.0
        self.original_image = game_object.image

    def update(self, ms):
        pass

    def set_direction(self, direction: float = None):
        if direction is None:
            if self.physics:
                direction = self.physics.get_direction()
            else:
                direction = self.direction
        if direction != self.direction:
            self.rotate(direction)
            self.direction = direction

    def rotate(self, direction):
        '''rotate an image while keeping its center and size'''
        image = self.original_image
        angle = direction / pi * 180
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_rect = rot_rect.clip(rot_image.get_rect())
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.game_object.image = rot_image
