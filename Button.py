import pygame
from Settings import *
import abc


class Button(object):
    def __init__(self, screen, text, x, y, color, enable):
        self.__screen = screen
        self.__width = BUTTON_WIDTH
        self.__height = BUTTON_HEIGHT
        self.__button_color = color
        self.__text_color = WHITE_COLOR

        self.__enable = enable

        self.__font = pygame.font.SysFont(None, BUTTON_HEIGHT*2 // 3)

        self.__rect = pygame.Rect(0, 0, self.__width, self.__height)
        self.__rect.topleft = (x, y)
        self.__text = text

        self.__msg_image = self.__font.render(self.__text, True, self.__text_color, None)
        self.__msg_image_rect = self.__msg_image.get_rect()
        self.__msg_image_rect.center = self.__rect.center

    def draw(self):
        self.__screen.fill(self.__button_color[0] if self.__enable else self.__button_color[1], self.__rect)
        self.__screen.blit(self.__msg_image, self.__msg_image_rect)

    def not_click(self):
        if not self.__enable:
            self.__msg_image = self.__font.render(self.__text, True, self.__text_color, self.__button_color[0])
            self.__enable = True

    @abc.abstractmethod
    def click(self, game):
        pass

    def get_enable(self):
        return self.__enable

    def set_enable(self, enable):
        self.__enable = enable

    def get_font(self):
        return self.__font

    def set_msg_image(self, msg_image):
        self.__msg_image = msg_image

    def get_rect(self):
        return self.__rect

    def get_text(self):
        return self.__text

    def get_text_color(self):
        return self.__text_color

    def get_button_color(self):
        return self.__button_color


class StartButton(Button):
    def __init__(self, screen, text, x, y, enable):
        super().__init__(screen, text, x, y, BUTTON_COLOR, enable)

    def click(self, game):
        if not game.get_is_play():
            game.set_is_play(True)
            game.start()
            game.set_winner(None)
            self.set_enable(False)
            return True
        return False


class GiveUpButton(Button):
    def __init__(self, screen, text, x, y, enable):
        super().__init__(screen, text, x, y, BUTTON_COLOR, enable)

    def click(self, game):
        if game.get_is_play():
            game.set_is_play(False)
            if game.get_winner() is None:
                game.set_winner(game.get_map().reverse_turn(game.get_player()))
        return False


class UseAIButton(Button):
    def __init__(self, screen, text, x, y):
        super().__init__(screen, text, x, y, AI_BUTTON_COLOR, True)
        self.__text = text

    def click(self, game):
        if self.get_enable():
            game.set_useAI(not game.get_useAI())
            self.__text = 'PVE' if self.__text == 'PVP' else 'PVP'
            self.set_msg(AI_BUTTON_COLOR[0])

    def set_msg(self, color):
        self.set_msg_image(self.get_font().render(self.__text, True,
                                                  self.get_text_color(), color))
