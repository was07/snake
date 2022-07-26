from msilib.schema import SelfReg
from operator import le
import pygame
import random


class Snake:
    def __init__(self, screen, cord=(0, 0)):
        self.screen = screen
        self.rects = [pygame.Rect(cord[0] * 20, cord[1] * 20, 20, 20)]
        self.d = (1, 0)
        self.tail_length = 0
        self.alive = True

        for _ in range(4): self.grow()
    
    def head_xy(self, d=20):  # 20: cell units, 1: pixels
        return int(self.rects[0].x / d), int(self.rects[0].y / d)
    
    def tile_cords(self):
        return [(rect.x / 20, rect.y / 20) for rect in self.rects]
    
    def draw(self):
        s1 = 6
        s2 = 16
        s3 = 26
        # drawing rects (in reversed order)
        for i, rect in reversed(list(enumerate(self.rects))):
            if i < s1:
                white = 225 - i*10
            elif i < s2:
                white = (225 - s1*10)-(i - s1)*5
                print(white)
            else:
                white = 115
            
            pygame.draw.rect(self.screen, (white, white, white), rect)
    
    def update(self, nf):
        if nf % 10:
            return

        poses = [(rect.x, rect.y) for rect in self.rects]

        if (self.head_xy(1) in poses[1:]) or not self.alive:
            print('Game should be over')
            self.alive = False
            return 1
        
        head = self.rects[0]
        
        for i, rect in enumerate(self.rects):
            if i:  # not head
                rect.x = poses[i - 1][0]
                rect.y = poses[i - 1][1]

        head.x += self.d[0] * 20
        head.y += self.d[1] * 20

        x, y = self.head_xy()
        x, y = x * 20, y * 20
        w, h = self.screen.get_size()
        if x < 0:      head.x = w - 20
        if x > w - 20: head.x = 0
        if y < 0:      head.y = h - 20
        if y > h - 20: head.y = 0

    def grow(self):
        x, y = self.rects[-1].x, self.rects[-1].y
        self.update(0)
        self.rects.append(pygame.Rect(x, y, 20, 20))


class Food:
    def __init__(self, screen, color='#FF0000'):
        self.screen = screen
        self.color = color
        self.x: int = 0
        self.y: int = 0
        self.rect = pygame.Rect(self.x * 20, self.y * 20, 20, 20)
    
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
    
    def update(self, nf):
        pass

    def new_spot(self, snake_tile_cords):
        while True:
            self.x = random.randint(0, 35-1)
            self.y = random.randint(0, 20-1)
            if (self.x, self.y) not in snake_tile_cords:
                self.rect = pygame.Rect(self.x * 20, self.y * 20, 20, 20)
                break


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((35*20, 20*20))
        self.snake = Snake(self.screen, (3, 9))
        self.food = Food(self.screen)
        self.food.new_spot(self.snake.tile_cords())
        self.updates_count = 0

        self.run = True
    
    def update(self):
        if not self.run: return

        self.updates_count += 1
        snake_status = self.snake.update(self.updates_count)
        self.food.update(self.updates_count)
        if snake_status == 1:
            self.screen.fill((20, 20, 30))
            self.food.color = '#990000'
            self.run = False
            return
        self.screen.fill((0, 0, 0))

        snake = self.snake
        d = self.snake.d
        sx, sy = self.snake.head_xy()

        if (sx + d[0], sy + d[1]) == (self.food.x, self.food.y):
            print('Food eaten!')
            snake.grow()
            snake.tail_length += 1

            self.food.new_spot(snake.tile_cords())
        
    def draw(self):
        self.snake.draw()
        self.food.draw()
        pygame.display.flip()
