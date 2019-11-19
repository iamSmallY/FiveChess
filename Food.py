import pygame
from pygame.sprite import Sprite
import random
from Settings import Settings


class Food(Sprite):
    def __init__(self, _settings, _screen):
        Sprite.__init__(self)

        self.__x = random.randint(0, _settings.MAP_WIDTH - 1)
        self.__y = random.randint(0, _settings.MAP_HEIGHT - 1)
        self.__size = _settings.FOOD_SIZE

        self.draw_food(_settings, _screen)

    def draw_food(self, _settings, _screen):
        pygame.draw.circle(_screen, _settings.RED, (self.__x, self.__y), 10)


if __name__ == '__main__':
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.MAP_WIDTH, settings.MAP_HEIGHT))
    screen.fill(settings.WHITE)
    food = Food(settings, screen)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
