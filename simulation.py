import pygame

from Game import Game

game = Game()

game.fill_entities(2)
game.fill_foods(100)

while True:
    game.surface.fill(pygame.Color('gray'))
    for event in pygame.event.get():
        key_number = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]

        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.running = not game.running

            elif event.key in key_number:
                game.fps = 60 * pow(10, key_number.index(event.key))
                if event.key == key_number[0]:
                    game.fps = 10

            elif event.key == pygame.K_d:
                game.debug = not game.debug

        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 1:
        #         print(len(game.entities))
        #         #game.add_entity(Entity(event.pos[0], event.pos[1], 100, 10, 0, 100))
        #         #game.kill_entity(entity1)
        #         if game.phase == 0:
        #             game.setup_evening()
        #         elif game.phase == 1:
        #             game.setup_morning()
        #     elif event.button == 3:
        #         pass

        # elif event.type == pygame.MOUSEBUTTONUP:
        #     if event.button == 1:
        #         pass
        #
        # elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed(3)[0]:
        #     print('Движется')
        #     newX = event.pos[0]
        #     newY = event.pos[1]
        #     #if oldX != newX or oldY != newY:
        #     #    pass
        #     oldX = newX
        #     oldY = newY

    if game.running:
        game.life()
