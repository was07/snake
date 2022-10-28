import pygame
import random


class Snake:
    def __init__(self, screen: pygame.Surface, cord=(0, 0)):
        self.screen = screen
        self.rects = [pygame.Rect(cord[0] * 20, cord[1] * 20, 20, 20)]
        self.direction = (1, 0)
        self.tail_length = 0
        self.alive = True

        self.grow(4)
    
    def head_xy(self, d=20):  # 20: return in cell units, 1: return in pixels
        return int(self.rects[0].x / d), int(self.rects[0].y / d)
    
    def tile_cords(self):  # return list of cordinates of tiles of the snake
        return [(rect.x / 20, rect.y / 20) for rect in self.rects]
    
    def draw(self):
        s1 = 6
        s2 = 16
        # drawing rects (in reversed order)
        for i, rect in reversed(list(enumerate(self.rects))):
            # calculate the color (white, white, white)
            if i < s1:
                x = 225 - i*10
            elif i < s2:
                x = (225 - s1*10)-(i - s1)*5
            else:
                x = 115
            
            pygame.draw.rect(self.screen, (x, x, x), rect)
    
    def update(self, nf: int):
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

        head.x += self.direction[0] * 20
        head.y += self.direction[1] * 20

        x, y = self.head_xy()
        x, y = x * 20, y * 20
        w, h = self.screen.get_size()
        if x < 0:      head.x = w - 20
        if x > w - 20: head.x = 0
        if y < 0:      head.y = h - 20
        if y > h - 20: head.y = 0

    def grow(self, n=1):
        for _ in range(n):
            x, y = self.rects[-1].x, self.rects[-1].y
            self.update(0)
            self.rects.append(pygame.Rect(x, y, 20, 20))


class Food:
    def __init__(self, screen: pygame.Surface, color='#ff1c2f'):
        self.screen = screen
        self.color = color
        self.x = 0  # 1st position of food
        self.y = 0
        self.rect = pygame.Rect(self.x * 20, self.y * 20, 20, 20)
    
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=5)
    
    def update(self, nf):
        pass

    def new_spot(self, snake_tile_cords):
        while True:
            self.x = random.randint(0, 35-1)
            self.y = random.randint(0, 20-1)
            if (self.x, self.y) not in snake_tile_cords:  # if food position not in snake
                self.rect = pygame.Rect(self.x * 20, self.y * 20, 20, 20)
                break


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((35*20, 20*20))
        pygame.display.set_caption('Snake')
        self.snake = Snake(self.screen, (3, 9))
        self.food = Food(self.screen)
        self.food.new_spot(self.snake.tile_cords())
        self.updates_count = 0

        self.points = 0
        self.run = True

        self.counter_font = pygame.font.SysFont('Consolas', 30)
        self.bigger_font = pygame.font.SysFont('Consolas', 60)
    
    def update(self):
        if not self.run: return

        snake = self.snake
        d = self.snake.direction
        sx, sy = self.snake.head_xy()

        if (sx, sy) == (self.food.x, self.food.y):  # food eaten
            snake.grow()
            snake.tail_length += 1

            self.food.new_spot(snake.tile_cords())
            self.points += 1

        self.updates_count += 1
        snake_status = self.snake.update(self.updates_count)
        self.food.update(self.updates_count)

        if snake_status == 1:  # game over
            self.screen.fill((30, 30, 50))  # making the screen lighter for freezing effect
            self.food.color = '#990000'  # ^
            self.run = False  # stopping updates
            text = self.bigger_font.render(f"{self.points}", True, "#ffffff")
            self.screen.blit(text, (20, 20))
            text = self.bigger_font.render(f":(", True, "#ff1c2f")
            self.screen.blit(text, (80, 20))
            return
        
        self.screen.fill((0, 0, 0))

    def draw(self):
        self.snake.draw()  # draw snake
        self.food.draw()  # draw food
        if self.run:
            text = self.counter_font.render(f'{self.points}', True, '#FFFFFF')
            self.screen.blit(text, (20, 20))  # draw points

        pygame.display.flip()
