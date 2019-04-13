from abc import ABC, abstractmethod


class Component(ABC):
    """
    Add different components to GameObjects for added functionality.
    Common collections of components can be made into a game_object subclass.
    Don't forget to call super() in Component subclass __init__() methods!
    """
    def __init__(self, game_object):
        '''Called at creation'''
        self.game_object = game_object

    @abstractmethod
    def update(self, ms):
        '''Called every frame. Includes time since last frame.'''
        pass

    def handle_event(self, events):
        '''Component specific events.'''
        pass
