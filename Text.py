import pygame


class Text(object):
    def __init__(self, screen, font, size, text, text_color, x, y):
        self.__screen = screen
        self.__text_font = pygame.font.SysFont(font, size)
        self.__text_image = self.__text_font.render(text, True, text_color)
        self.__text_image_rect = self.__text_image.get_rect()
        self.__text_image_rect.center = (x, y)

    def get_text_element(self):
        return self.__text_image, self.__text_image_rect
