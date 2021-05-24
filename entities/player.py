from kivy.core.window import Window

from entities.entity import Entity


class Player(Entity):
    def __init__(self):
        super().__init__(
            pos=((Window.width / 2) - 25, 10),
            size=(62, 51),
            source='assets/ship.png'
        )
