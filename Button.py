import pygame
from Settings import *


class Button(object):
    def __init__(self, screen, text, x, y, color, enable):
        self.screen = screen
        self.width = BUTTON_WIDTH
        self.height = BUTTON_HEIGHT
        self.button_color = color
        self.text_color = TEXT_COLOR
        self.enable = enable
        self.font = pygame.font.SysFont(None, BUTTON_HEIGHT * 2 // 3)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topleft = (x, y)
        self.text = text

        self.msg_image = self.font.render(self.text, True, self.text_color,
                                          self.button_color[0] if self.enable else self.button_color[1])
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        self.screen.fill(self.button_color[0] if self.enable else self.button_color[1], self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def get_rect(self):
        return self.rect


class StartButton(Button):
    def __init__(self, screen, text, x, y):
        super().__init__(screen, text, x, y, BUTTON_COLOR, True)

    def click(self, game):
        if self.enable:
            game.start()
            game.set_winner(None)
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[1])
            self.enable = False
            return True
        return False

    def not_click(self):
        if not self.enable:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[0])
            self.enable = True


class GiveUpButton(Button):
    def __init__(self, screen, text, x, y):
        super().__init__(screen, text, x, y, BUTTON_COLOR, False)

    def click(self, game):
        if self.enable:
            game.set_is_play(False)
            if game.get_winner() is None:
                game.set_winner(game.get_map().reverse_turn(game.get_player()))
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[1])
            self.enable = False
            return True
        return False

    def not_click(self):
        if not self.enable:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[0])
            self.enable = True
