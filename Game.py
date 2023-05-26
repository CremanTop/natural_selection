from random import randint

import pygame

WIDTH = 1200
HEIGHT = 700

from Animal import Animal
from Food import Food

count = 0


class Game:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.res = self.width, self.height
        self.fps = 10
        self.tick = 0

        pygame.init()
        self.surface = pygame.display.set_mode(self.res)
        self.clock = pygame.time.Clock()

        self.entities: list[Animal] = []
        self.foods: list[Food] = []
        self.phase = 0
        self.max_food = 200

        self.running = True
        self.debug = False
        # oldX = 0
        # oldY =

    def render(self):
        [entity.render(self.surface, self.debug) for entity in self.entities]
        [entity.render(self.surface) for entity in self.foods]

    def add_entity(self, entity: Animal):
        self.entities.append(entity)

    def kill_entity(self, entity: Animal):
        if self.entities.__contains__(entity):
            self.entities.pop(self.entities.index(entity))

    def spawn_food(self, x: int, y: int):
        self.foods.append(Food(x, y))

    def fill_foods(self, num: int):
        val = Food.size  # отступ
        count = len(self.foods)
        [self.foods.append(Food(randint(val, self.width - val), randint(val, self.height - val))) for _ in
         range(min(self.max_food - count, num))]

    def fill_entities(self, num: int):
        size = 10
        speed = 10
        view_range = 1000
        stamina = 1000
        [self.add_entity(
            Animal(randint(size, self.width - size), randint(size, self.height - size), size, speed, view_range,
                   stamina, 'herbivorous')) for _ in range(num)]

    def full_energy(self):
        [self.entities[i].fill_energy() for i in range(len(self.entities))]

    def setup_morning(self):
        self.phase = 0
        self.full_energy()
        print('Утро')

        entity_count = len(self.entities)
        a_speed = 0
        a_range = 0
        a_stamina = 0
        a_size = 0

        for entity in self.entities:
            entity.tired = False
            if entity.saturation == 0:
                # self.kill_entity(entity)
                if entity.hunger:
                    self.kill_entity(entity)
                else:
                    entity.hunger = True
            else:
                entity.saturation = 0

            a_speed += entity.speed
            a_range += entity.range_view
            a_stamina += entity.stamina
            a_size += entity.size

        a_speed = a_speed / entity_count
        a_size = a_size / entity_count
        a_range = a_range / entity_count
        a_stamina = a_stamina / entity_count
        print(entity_count, int(a_size), int(a_stamina), int(a_speed), int(a_range))

        self.fill_foods(100)

    def setup_evening(self):
        self.phase = 1
        print('Вечер')

    def reverse_phase(self):
        if self.phase == 0:
            self.setup_evening()
        elif self.phase == 1:
            self.setup_morning()

    def search_food(self, entity: Animal):
        if entity.is_raptor():
            entity.search_entity(self.entities, self.phase, self.debug)
        elif entity.is_herbivorous():
            entity.search_entity(self.foods, self.phase, self.debug)

    def life(self):
        # [print(entity.type, end=', ') for entity in self.entities]
        # print('')
        for entity in self.entities:
            if self.phase == 0:
                self.search_food(entity)
            elif self.phase == 1:
                if entity.is_saturated():
                    entity.search_entity(self.entities, self.phase, self.debug)
                else:
                    self.search_food(entity)
            entity.follow_nearest()
        global count
        if count % ((self.fps // 60) + 1) == 0:
            self.render()
            pygame.display.flip()
        self.clock.tick(self.fps)
        self.tick = (self.tick + 1) % 60
        if self.tick == 0:
            self.reverse_phase()
        count += 1
        # print(count)
