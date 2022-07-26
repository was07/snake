import sys
import pygame

import stuff
 
pygame.init()

fps = 60
fpsClock = pygame.time.Clock()
 
game = stuff.Game()

nf = 0
while True:
    nf += 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_UP    and game.snake.direction != (0, 1):
                game.snake.direction = (0, -1)
            if event.key == pygame.K_DOWN  and game.snake.direction != (0, -1):
                game.snake.direction = (0, 1)
            if event.key == pygame.K_LEFT  and game.snake.direction != (1, 0):
                game.snake.direction = (-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction != (-1, 0):
                game.snake.direction = (1, 0)
            if event.key == pygame.K_SPACE:
                game.run = not game.run
            game.update()
            game.draw()
    
    game.update()
    game.draw()

    pygame.display.flip()
    fpsClock.tick(fps)
