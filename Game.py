from Button import *
from ChessAI import *


class Game(object):
    def __init__(self, caption):
        self.__screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption(caption)
        self.__clock = pygame.time.Clock()

        self.__start_map = StartMap(self.__screen, CHESS_LEN, CHESS_LEN)
        self.__chess_map = ChessMap(self.__screen, CHESS_LEN, CHESS_LEN)
        self.__is_in_start_map = True

        self.__action = None
        self.__is_play = False
        self.__player = None
        self.__winner = None

        self.__AI = ChessAI(CHESS_LEN)
        self.__isAI = True
        self.__useAI = False

    def start(self):
        self.__is_play = True
        self.__player = MapEntryType.MAP_PLAYER_ONE
        self.__chess_map.reset()
        # self.__start_map.reset()

    def play(self):
        if self.__is_in_start_map:
            self.__start_map.draw_background()
        else:
            self.__clock.tick(60)

            pygame.draw.rect(self.__screen, LIGHT_YELLOW, pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT))
            pygame.draw.rect(self.__screen, (255, 255, 255), pygame.Rect(MAP_WIDTH, 0, INFO_WIDTH, SCREEN_HEIGHT))
            # for button in self.__buttons:
            #     button.draw()
            # self.__useAI_button.draw()
            self.__chess_map.draw_button()

            if self.__is_play and not self.is_over():
                if self.__useAI and self.__isAI:
                    x, y = self.__AI.find_best_chess(self.__chess_map.get_map(), self.__player)
                    self.chess_map_check_click(x, y)
                    self.__isAI = False

                if self.__action is not None:
                    self.chess_map_check_click(self.__action[0], self.__action[1])
                    self.__action = None

                if not self.is_over():
                    self.change_mouse_show()

            if self.is_over():
                self.show_winner()

            self.__chess_map.draw_background()
            self.__chess_map.draw_chess(self.__screen)

    def change_mouse_show(self):
        map_x, map_y = pygame.mouse.get_pos()
        x, y = self.__chess_map.map_pos_to_index(map_x, map_y)
        if self.__chess_map.is_in_map(map_x, map_y) and self.__chess_map.is_empty(x, y):
            pygame.mouse.set_visible(False)
            pos, radius = (map_x, map_y), CHESS_RADIUS
            pygame.draw.circle(self.__screen, LIGHT_RED, pos, radius)
        else:
            pygame.mouse.set_visible(True)

    def chess_map_check_click(self, x, y):
        self.__chess_map.click(x, y, self.__player)
        if self.__AI.is_win(self.__chess_map.get_map(), self.__player):
            self.__winner = self.__player
            self.get_map().click_button(self, self.__chess_map.get_button()[1])
        else:
            self.__player = self.__chess_map.reverse_turn(self.__player)
            if self.__useAI and not self.__is_AI:
                self.__isAI = True

    def mouse_click(self, mouse_x, mouse_y):
        if self.__is_in_start_map:
            if self.__start_map.check_buttons(self, mouse_x, mouse_y):
                self.__is_in_start_map = False
                self.play()
        else:
            if self.__is_play and self.__chess_map.is_in_map(mouse_x, mouse_y) and not self.is_over():
                x, y = self.__chess_map.map_pos_to_index(mouse_x, mouse_y)
                if self.__chess_map.is_empty(x, y):
                    self.__action = (x, y)

    def is_over(self):
        return self.__winner is not None

    def show_winner(self):
        def show_font(screen, text, location_x, location_y, height):
            font = pygame.font.SysFont(None, height)
            font_image = font.render(text, True, (0, 0, 255), None)
            font_image_rect = font_image.get_rect()
            font_image_rect.x = location_x
            font_image_rect.y = location_y
            screen.blit(font_image, font_image_rect)
        if self.__winner is None:
            return
        if self.__winner == MapEntryType.MAP_PLAYER_ONE:
            string = 'Winner is White'
        else:
            string = 'Winner is Black'
        show_font(self.__screen, string, MAP_WIDTH+25, SCREEN_HEIGHT-60, 30)
        pygame.mouse.set_visible(True)

    def get_is_play(self):
        return self.__is_play

    def set_is_play(self, is_play):
        self.__is_play = is_play

    def get_map(self):
        return self.__chess_map

    def get_player(self):
        return self.__player

    def get_winner(self):
        return self.__winner

    def set_winner(self, winner):
        self.__winner = winner

    def get_useAI(self):
        return self.__useAI

    def set_useAI(self, useAI):
        self.__useAI = useAI


if __name__ == '__main__':
    pygame.init()
    game = Game('Hololive'+GAME_VERSION)
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

# if __name__ == '__main__':
#     game = Game('FIVE CHESS' + GAME_VERSION)
#     while True:
#         game.play()
#         pygame.display.update()
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 mouse_x, mouse_y = pygame.mouse.get_pos()
#                 game.mouse_click(mouse_x, mouse_y)
#                 game.get_map().check_buttons(game, mouse_x, mouse_y)
