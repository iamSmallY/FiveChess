import pygame
from pygame.sprite import Sprite
from Settings import *


class Bird(Sprite):
    def __init__(self, _screen):
        super(Bird, self).__init__()

        self.__screen = _screen

        self.__images = [
            pygame.image.load(BIRDS_IMAGES_LOCATION[0]),
            pygame.image.load(BIRDS_IMAGES_LOCATION[1]),
            pygame.image.load(BIRDS_IMAGES_LOCATION[2])
        ]
        self.__wing_sound = pygame.mixer.Sound(BIRDS_WING_SOUND_LOCATION)

    def show_bird(self):
        self.__screen.blit(self.__images[1], [0, 0])


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    bird = Bird(screen)
    bird.show_bird()
    pygame.display.update()
