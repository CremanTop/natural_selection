import random

import pygame
from random import randint

from Entity import Entity, get_distance, get_distance_pos
# from Game import WIDTH, HEIGHT
from Position import Position

sp_evol = 20  # speed evolution


class Animal(Entity):

    def __init__(self, x: float, y: float, size: int, speed: int, range_view: int, stamina: int, e_type: str):
        super().__init__(x, y, size, e_type)
        self.speed = 0
        self.range_view = 0
        self.stamina = 0
        self.energy = 0
        self.wayX = 0
        self.wayY = 0
        self.waiting = 0
        self.tired = False
        self.hunger = False

        self._set_speed(speed)
        self._set_range_view(range_view)
        self._set_stamina(stamina)
        self.fill_energy()

        r = min(self.stamina // 2, 255)
        g = min(self.speed * 3, 255)
        b = min(self.range_view // 3, 255)
        self.color = pygame.Color(r, g, b)
        self.saturation = 0

    def render(self, surface, debug):
        super(Animal, self).render(surface)
        if debug:
            pygame.draw.circle(surface=surface, color=pygame.Color('black'), center=(self.pos.x, self.pos.y),
                           radius=self.range_view, width=1)
        if self.is_raptor():
            pygame.draw.circle(surface=surface, color=pygame.Color('white'), center=(self.pos.x, self.pos.y), radius=self.size // 2)

    def _set_speed(self, speed: int):
        self.speed = min(max(0, speed), 10000) # 100

    def _set_range_view(self, range_view: int):
        self.range_view = min(max(0, range_view), 10000) #400

    def _set_stamina(self, stamina: int):
        self.stamina = min(max(10, stamina), 10000) # 500

    def _subtract_energy(self, value: float):
        self.energy = max(0.0, self.energy - value)

    def fill_energy(self):
        self.energy = self.stamina

    def is_raptor(self):
        return self.type == 'raptor'

    def is_herbivorous(self):
        return self.type == 'herbivorous'

    def move(self, move_x: float, move_y: float):
        pos = (self.pos.x, self.pos.y)
        new_pos = (pos[0] + move_x, pos[1] + move_y)
        #print(move_x, move_y, pos[0], pos[1])
        self._set_pos(new_pos[0], new_pos[1])
        self._subtract_energy(get_distance_pos(Position(pos[0], pos[1]), Position(new_pos[0], new_pos[1])))

    def is_saturated(self):
        if self.is_herbivorous() and self.saturation >= 2:
            return True
        elif self.is_raptor() and self.saturation >= 2:
            return True
        return False

    def search_entity(self, entities: list, phase: int, debug: bool):
        #if self.energy > 0:
            minimal = 99999999
            wayX = 0
            wayY = 0
            # if self.saturation >= 2 and phase == 0:
            #     self.wayX = 0
            #     self.wayY = 0
            #     return
            if (phase == 1 and not self.tired) or (phase == 0 and not self.is_saturated()):
                goal = 0
                for entity in entities:
                    distance = get_distance(self, entity)
                    if self != entity:
                        if distance <= self.size + entity.size:
                            if entity.type == self.type and phase == 1 and self.is_saturated() and entity.is_saturated():# and not entity.tired:
                                #print('Размножение')
                                self.saturation = 1
                                entity.saturation = 1
                                self.tired = True
                                entity.tired = True
                                entities.append(reproduct(self, entity))
                                return
                            elif (entity.type == 'plant' and self.is_herbivorous()) or (entity.is_herbivorous() and self.is_raptor()):
                                entities.pop(entities.index(entity))
                                self.saturation += 1
                                if self.hunger:
                                    self.hunger = False
                                return
                        elif distance <= self.range_view and distance < minimal:
                            if distance == 0.0:
                                wayX = 0
                                wayY = 0
                            elif (phase == 0 and not self.is_saturated() and ((entity.type == 'plant' and self.is_herbivorous()) or (entity.is_herbivorous() and self.is_raptor()))) or (phase == 1 and self.is_saturated() and entity.is_saturated() and self.type == entity.type):# and not entity.tired):
                                wayX = self.speed * (entity.pos.x - self.pos.x) / distance
                                wayY = self.speed * (entity.pos.y - self.pos.y) / distance
                                minimal = distance
                                goal = entity
                # if goal != 0 and debug:
                #     goal.color = pygame.Color('red')

            while wayX == 0 and wayY == 0:
                if self.waiting == 0:
                    wayX = randint(-1, 1) * self.speed
                    wayY = randint(-1, 1) * self.speed
                    self.waiting = 1
                else:
                    self.waiting = (self.waiting + 1) % randint(10, 15)
                    return

            self.wayX = wayX
            self.wayY = wayY

    def follow_nearest(self):
        if self.energy > 0:
            self.move(self.wayX, self.wayY)


def reproduct(entity1: Animal, entity2: Animal):
    pos = Position((entity1.pos.x + entity2.pos.x) / 2, (entity1.pos.y + entity2.pos.y) / 2)
    size = (entity1.size + entity2.size) // 2 + randint(-sp_evol, sp_evol)
    speed = (entity1.speed + entity2.speed) // 2 + randint(-sp_evol * 3, sp_evol * 3) #- size // 3
    range_view = (entity1.range_view + entity2.range_view) // 2 + randint(-sp_evol * 8, sp_evol * 8)
    stamina = (entity1.stamina + entity2.stamina) // 2 + randint(-sp_evol * 5, sp_evol * 5)

    e_type = random.choices([entity1.type, 'raptor' if entity1.type == 'herbivorous' else 'herbivorous'], weights=[99, 0])

    entity = Animal(pos.x, pos.y, size, speed, range_view, stamina, e_type[0])
    #print(size, speed, e_type[0], entity)
    #print(entity1.type, entity2.type, e_type
    entity.saturation = 1
    entity.energy = 0
    return entity
