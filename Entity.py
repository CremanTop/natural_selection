import pygame
import numba

from Game import WIDTH, HEIGHT
from Position import Position


class Entity:

    def __init__(self, x: float, y: float, size: int, e_type: str):
        self.type = e_type
        self.pos = Position(0, 0)
        self.size = 0
        self._set_pos(x, y)
        self._set_size(size)
        self.color = pygame.Color(0, 0, 0)

    def render(self, surface):
        pygame.draw.circle(surface=surface, color=self.color, center=(self.pos.x, self.pos.y),
                           radius=self.size)

    def _set_pos(self, x: float, y: float):
        self.pos.x = (x if x <= WIDTH - self.size else WIDTH - self.size) if x >= self.size else self.size
        self.pos.y = (y if y <= HEIGHT - self.size else HEIGHT - self.size) if y >= self.size else self.size

    def _set_size(self, size: int):
        self.size = max(2, size)

    def set_color(self, r, g, b):
        self.color = pygame.Color(r, g, b)


def get_distance(entity1: Entity, entity2: Entity):
    return pow(pow(entity2.pos.x - entity1.pos.x, 2) + pow(entity2.pos.y - entity1.pos.y, 2), 0.5)


def get_distance_pos(pos1: Position, pos2: Position):
    return pow(pow(pos2.x - pos1.x, 2) + pow(pos2.y - pos1.y, 2), 0.5)
