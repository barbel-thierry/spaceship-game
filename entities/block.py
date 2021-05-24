from entities.entity import Entity


class Block(Entity):
    def __init__(self, pos, size):
        super().__init__(
            pos=pos,
            size=size,
            source='assets/block.png'
        )
