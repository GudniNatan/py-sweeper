from pygame.locals import KEYDOWN, K_ESCAPE, QUIT
from pygame import event as pyEvent
from scenes.menu_scene import MenuScene


class SceneController(object):
    def __init__(self):
        self.__scene = MenuScene(self)

    def render(self, screen):
        return self.__scene.render(screen)

    def handle_events(self, events):
        # Handle global events
        for event in events:
            if event.type == KEYDOWN:
                self.handle_keydown(event)

        # Pass remaining events to scene
        self.__scene.handle_events(events)

    def handle_keydown(self, event):
        if event.key == K_ESCAPE:
            pyEvent.post(pyEvent.Event(QUIT))

    def update(self, ms):
        # Time-based updates
        # self.scene.update(ms)
        self.__scene.update(ms)

    def get_scene(self):
        return self.__scene

    def set_scene(self, scene):
        self.__scene = scene
