from Entity import Entity


class Food(Entity):

    size = 5

    def __init__(self, x: int, y: int):
        super().__init__(x, y, Food.size, 'plant')
        self.set_color(255, 255, 0)