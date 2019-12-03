import pygame
from pygame.locals import *
from Map_Entry_Type import *
from Map import *
# from Settings import *
from Button import *


class Game(object):
    def __init__(self,caption):
        pygame.init()
        self.__screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption(caption)
        self.__clock = pygame.time.Clock()
        self.__buttons = []
        self.__buttons.append(StartButton(self.__screen, 'Start', MAP_WIDTH+30, 15))
        self.__buttons.append(GiveUpButton(self.__screen, 'GiveUp', MAP_WIDTH+30, BUTTON_HEIGHT+45))
        self.__action = None

        self.__is_play = False
        self.__map = Map(CHESS_LEN, CHESS_LEN)
        self.__player = None
        self.__winner = None

    def start(self):
        self.__is_play = True
        self.__player = MapEntryType.MAP_PLAYER_ONE
        self.__map.reset()

    def play(self):
        self.__clock.tick(60)
        pygame.draw.rect(self.__screen, LIGHT_YELLOW, pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT))
        pygame.draw.rect(self.__screen, (255, 255, 255), pygame.Rect(MAP_WIDTH, 0, INFO_WIDTH, SCREEN_HEIGHT))

        for button in self.__buttons:
            button.draw()

        if self.__is_play and not self.is_over():
            if self.__action is not None:
                self.check_click(self.__action[0], self.__action[1])
                self.__action = None

            if not self.is_over():
                self.show_winner()

        if self.is_over():
            self.show_winner()

        self.__map.draw_background(self.__screen)
        self.__map.draw_chess(self.__screen)

    def check_click(self, x, y, is_AI = False):
        self.__map.click(x, y, self.__player)
        self.__player = self.__map.reverse_turn(self.__player)

    def mouse_click(self, map_x, map_y):
        if self.__is_play and self.__map.is_in_map(map_x, map_y) and not self.is_over():
            x, y = self.__map.map_pos_in_index(map_x, map_y)
            if self.__map.is_empty(x, y):
                self.__action = (x, y)

    def is_over(self):
        return self.__winner is not None

    def show_winner(self):
        def show_font(screen, text, location_x, location_y, height):
            font = pygame.font.SysFont(None, height)
            font_image = font.render(text, True, (0, 0, 255), (255, 255, 255))
            font_image_rect = font_image.get_rect()
            font_image_rect.x = location_x
            font_image_rect.y = location_y
            screen.blit(font_image, font_image_rect)
        if self.__winner == MapEntryType.MAP_PLAYER_ONE:
            string = 'Winner is White'
        else:
            string = 'Winner is Black'
        show_font(self.__screen, string, MAP_WIDTH+25, SCREEN_HEIGHT-60, 30)
        pygame.mouse.set_visible(True)

    def click_button(self, button):
        if button.click(self):
            for temp in self.__buttons:
                if temp != button:
                    temp.not_click()

    def check_buttons(self, mouse_x, mouse_y):
        for button in self.__buttons:
            if button.get_rect().collidepoint(mouse_x, mouse_y):
                self.click_button(button)
                break

    def get_is_play(self):
        return self.__is_play

    def set_is_play(self, is_play):
        self.__is_play = is_play

    def get_map(self):
        return self.__map

    def get_player(self):
        return self.__player

    def get_winner(self):
        return self.__winner

    def set_winner(self, winner):
        self.__winner = winner


if __name__ == '__main__':
    game = Game('FIVE CHESS' + GAME_VERSION)
    while True:
        game.play()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                game.mouse_click(mouse_x, mouse_y)
                game.check_buttons(mouse_x, mouse_y)