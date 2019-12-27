from Settings import *
import pygame
from Text import Text


class Button(object):
    def __init__(self, screen, text, x, y, color, enable):
        self.__screen = screen
        self.__width = BUTTON_WIDTH
        self.__height = BUTTON_HEIGHT
        self.__button_color = color
        self.__text_color = WHITE_COLOR

        self.__enable = enable

        self.__rect = pygame.Rect(0, 0, self.__width, self.__height)
        self.__rect.topleft = (x, y)
        self.__text = text

        self.__msg_image = Text(self.__screen, None, BUTTON_HEIGHT*2//3, self.__text, self.__text_color,
                                *self.__rect.center)

    def draw(self):
        self.__screen.fill(self.__button_color[0] if self.__enable else self.__button_color[1], self.__rect)
        self.__screen.blit(*self.__msg_image.get_text_element())

    def get_enable(self):
        return self.__enable

    def set_enable(self, enable):
        self.__enable = enable

    def set_msg_image(self, text):
        self.__msg_image = Text(self.__screen, None, BUTTON_HEIGHT * 2 // 3, text, self.__text_color,
                                *self.__rect.center)

    def get_rect(self):
        return self.__rect

    def get_text_color(self):
        return self.__text_color

    def get_text(self):
        return self.__text

    def set_text(self, text):
        self.__text = text
