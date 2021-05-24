from kivy.graphics import Rectangle, Color


class Entity:
    def __init__(self, pos, size, source):
        self._pos = pos
        self._size = size
        self._source = source
        self._instruction = Rectangle(
            pos=self._pos,
            size=self._size,
            source=self._source
        )

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self._instruction.pos = self._pos

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self._instruction.size = self._size

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value
        self._instruction.source = self._source
