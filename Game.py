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
        self.__isAI = False
        self.__useAI = True

    def start(self):
        self.__is_play = True
        self.__player = MapEntryType.MAP_PLAYER_ONE
        self.__chess_map.reset()

    def play(self):
        if self.__is_in_start_map:
            self.__start_map.draw_background()
        else:
            self.__clock.tick(60)

            pygame.draw.rect(self.__screen, LIGHT_YELLOW, pygame.Rect(0, 0, MAP_WIDTH, MAP_HEIGHT))
            pygame.draw.rect(self.__screen, WHITE_COLOR, pygame.Rect(MAP_WIDTH, 0, INFO_WIDTH, SCREEN_HEIGHT))
            self.__chess_map.draw_button()

            if self.__is_play and not self.is_over():
                if self.__useAI:
                    self.__chess_map.draw_yagoo()
                if self.__useAI and self.__isAI:
                    x, y = self.__AI.find_best_chess(self.__chess_map.get_map(), self.__player)
                    self.chess_map_check_click(x, y)
                    self.__isAI = False

                if self.__action is not None:
                    self.chess_map_check_click(self.__action[0], self.__action[1])
                    self.__action = None

                if not self.is_over():
                    self.__chess_map.change_mouse_show()

            if self.is_over():
                self.__chess_map.show_winner(self.__winner)

            self.__chess_map.draw_background()
            self.__chess_map.draw_chess(self.__screen)

    def chess_map_check_click(self, x, y):
        self.__chess_map.click(x, y, self.__player)
        if self.__AI.is_win(self.__chess_map.get_map(), self.__player):
            self.__winner = self.__player
            self.__chess_map.click_giveup_button(self)
        else:
            self.__player = self.__chess_map.reverse_turn(self.__player)
            if self.__useAI and not self.__isAI:
                self.__isAI = True

    def mouse_click(self, mouse_x, mouse_y):
        if self.__is_in_start_map:
            if self.__start_map.check_buttons(self, mouse_x, mouse_y):
                self.__is_in_start_map = False
                self.play()
        else:
            if self.__is_play and not self.is_over() and self.__chess_map.is_in_map(mouse_x, mouse_y):
                x, y = self.__chess_map.map_pos_to_index(mouse_x, mouse_y)
                if self.__chess_map.is_empty(x, y):
                    self.__action = (x, y)
            if self.__chess_map.check_buttons(self, mouse_x, mouse_y):
                self.start()

    def is_over(self):
        return self.__winner is not None

    def reset(self):
        self.__start_map.reset()
        self.__is_in_start_map = True
        self.__useAI = True
        self.__isAI = False
        self.__chess_map.click_restart_button(self)

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
