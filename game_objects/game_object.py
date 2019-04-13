import pygame
from pygame.sprite import DirtySprite
from components import Component


class GameObject(DirtySprite):
    def __init__(self, game_objects, rect: pygame.Rect,
                 image: pygame.Surface = None):
        super().__init__()
        self.rect = rect
        if image:
            rect.size = image.get_rect().size
        else:
            image = pygame.Surface(rect.size)
        self.image = image
        self.area = None
        self.components = dict()
        self.real_x = self.rect.x
        self.real_y = self.rect.y
        self.game_objects = game_objects

    def add_component(self, ComponentClass) -> Component:
        if self.components.get(ComponentClass):
            return self.components[ComponentClass]
        component = ComponentClass(self)
        self.components[ComponentClass] = component
        return component

    def update_pos(self):
        self.rect.x = int(round(self.real_x))
        self.rect.y = int(round(self.real_y))

    def get_component(self, ComponentClass) -> Component:
        if isinstance(ComponentClass, Component):
            ComponentClass = type(ComponentClass)
        try:
            return self.components[ComponentClass]
        except KeyError:
            raise TypeError(
                "{} {} {} {} {}".format(
                    "GameObject", str(self), "does not have a",
                    ComponentClass.__name__,
                    "component."
                )
            )

    def update(self, ms):
        for comp in self.components.values():
            comp.update(ms)

    def handle_events(self, events):
        for comp in self.components.values():
            comp.handle_events(events)

    def blit(self, game_object, absolute=False):
        '''
        Pass in a game_object. If absolute, the location of the blit
        will be absolute, otherwise it will be relative to the parent object.
        '''
        rect = game_object.rect
        if absolute:
            rect = pygame.Rect(rect)
            rect.x -= self.rect.x
            rect.y -= self.rect.y
        self.image.blit(game_object.image, rect)

    def set_position(self, position):
        self.rect.topleft = position
