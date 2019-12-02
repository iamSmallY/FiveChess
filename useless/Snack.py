import random
import pygame
from pygame.sprite import Sprite
from useless.Settings import Settings
from useless.Direction import Direction


# class Snake(Sprite):
#     def __init__(self, x, y, direction):
#         Sprite.__init__(self)
#         self.__image = pygame.image.load('')
#         self.__x = x
#         self.__y = y
#         self.__direction = direction


class Snake(Sprite):
    def __init__(self, _settings, _screen):
        Sprite.__init__(self)

        self.__head_x = random.randint(3, _settings.MAP_WIDTH - 8)
        self.__head_y = random.randint(3, _settings.MAP_HEIGHT - 8)
        self.__bodies = [
            {'x': self.__head_x, 'y': self.__head_y},
            {'x': self.__head_x - 1, 'y': self.__head_y},
            {'x': self.__head_x - 2, 'y': self.__head_y}
        ]

        self.__direction = Direction.RIGHT

        self.draw_snake(_settings, _screen)

    def turn(self, _event):
        if _event.type == pygame.QUIT:
            return True
        elif _event.type == pygame.KEYDOWN:
            if (_event.key == pygame.K_LEFT or _event.key == pygame.K_a) and\
                    self.__direction != Direction.RIGHT:
                self.__direction = Direction.LEFT
            elif (_event.key == pygame.K_RIGHT or _event.key == pygame.K_d) and\
                    self.__direction != Direction.LEFT:
                self.__direction = Direction.RIGHT
            elif (_event.key == pygame.K_UP or _event.key == pygame.K_w) and\
                    self.__direction != Direction.DOWN:
                self.__direction = Direction.UP
            elif (_event.key == pygame.K_DOWN or _event.key == pygame.K_s) and\
                    self.__direction != Direction.UP:
                self.__direction = Direction.DOWN
            elif _event.key == pygame.K_ESCAPE:
                return True
        return False

    def draw_snake(self, _settings, _screen):
        for body in self.__bodies:
            print(body['x'], body['y'])
            temp_x = body['x']
            temp_y = body['y']
            snake_rect = pygame.Rect(temp_x, temp_y, _settings.SIZE, _settings.SIZE)
            pygame.draw.rect(_screen, _settings.BLUE, snake_rect)
            # snake_inner_rect = pygame.Rect(temp_x + 4, temp_y + 4, _settings.SIZE - 8, _settings.SIZE - 8)
            # pygame.draw.rect(_screen, _settings.BLUE, snake_inner_rect)

    def eat(self, food):
        # TODO fill eat part
        pass

    def alive(self):
        # TODO fill alive part
        pass

    def move(self):
        # TODO fill move part
        pass


if __name__ == '__main__':
    from useless.Food import Food
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.MAP_WIDTH, settings.MAP_HEIGHT))
    screen.fill(settings.WHITE)
    snake = Snake(settings, screen)
    food = Food(settings, screen)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break