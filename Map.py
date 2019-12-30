from Button import *
from Text import *
from Type import *
import abc
import sys


class AbstractMap(object):
    def __init__(self, screen, width, height):
        self.__screen = screen
        self.__width = width
        self.__height = height

    def get_screen(self):
        return self.__screen

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    @abc.abstractmethod
    def reset(self):
        pass

    @abc.abstractmethod
    def draw_background(self):
        pass

    @abc.abstractmethod
    def draw_button(self):
        pass

    @abc.abstractmethod
    def check_buttons(self, game, mouse_x, mouse_y):
        pass


class StartMap(AbstractMap):
    def __init__(self, screen, width, height):
        super().__init__(screen, width, height)

        self.__back_img = pygame.image.load('./source/image/background.jpg')
        self.__back_img = pygame.transform.scale(self.__back_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.__title = Text(screen, None, TITLE_HEIGHT, 'Five Chess', BLACK_COLOR, TITLE_X, TITLE_Y)

        self.__start_button = Button(self.get_screen(), 'Start',
                                     TITLE_X - BUTTON_WIDTH // 2, TITLE_Y + TITLE_HEIGHT, BUTTON_COLOR, True)
        self.__model_button = Button(self.get_screen(), 'PVE',
                                     TITLE_X - BUTTON_WIDTH // 2, TITLE_Y + TITLE_HEIGHT + 60, AI_BUTTON_COLOR, True)
        self.__exit_button = Button(self.get_screen(), 'Exit',
                                    TITLE_X - BUTTON_WIDTH // 2, TITLE_Y + TITLE_HEIGHT + 120, BUTTON_COLOR, True)

    def reset(self):
        self.__start_button = Button(self.get_screen(), 'Start',
                                     TITLE_X - BUTTON_WIDTH // 2, TITLE_Y + TITLE_HEIGHT, BUTTON_COLOR, True)
        self.__model_button = Button(self.get_screen(), 'PVE',
                                     TITLE_X - BUTTON_WIDTH // 2, TITLE_Y + TITLE_HEIGHT + 60, AI_BUTTON_COLOR, True)
        self.__exit_button = Button(self.get_screen(), 'Exit',
                                    TITLE_X - BUTTON_WIDTH // 2, TITLE_Y + TITLE_HEIGHT + 120, BUTTON_COLOR, True)

    def draw_background(self):
        pygame.draw.rect(self.get_screen(), WHITE_COLOR, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.get_screen().blit(self.__back_img, (0, 0))
        self.get_screen().blit(*self.__title.get_text_element())
        self.draw_button()

    def draw_button(self):
        self.__start_button.draw()
        self.__model_button.draw()
        self.__exit_button.draw()

    def check_buttons(self, game, mouse_x, mouse_y):
        if self.__start_button.get_rect().collidepoint(mouse_x, mouse_y):
            self.click_start_button(game)
            return True
        elif self.__model_button.get_rect().collidepoint(mouse_x, mouse_y):
            self.click_model_button(game)
            return False
        elif self.__exit_button.get_rect().collidepoint(mouse_x, mouse_y):
            self.click_exit_button()

    @staticmethod
    def click_start_button(game):
        if not game.get_is_play():
            game.set_is_play(True)
            game.start()
            game.set_winner(None)
        game.start()

    def click_model_button(self, game):
        game.set_useAI(not game.get_useAI())
        self.__model_button.set_text('PVE' if self.__model_button.get_text() == 'PVP' else 'PVP')
        self.__model_button.set_msg_image(self.__model_button.get_text())
        self.__model_button.set_enable(not self.__model_button.get_enable())

    @staticmethod
    def click_exit_button():
        pygame.quit()
        sys.exit('GoodBye~')


class ChessMap(AbstractMap):
    def __init__(self, screen, width, height):
        super().__init__(screen, width, height)
        self.__map = [[0 for x in range(self.get_width())] for y in range(self.get_height())]
        self.__steps = []

        self.__restart_button = Button(self.get_screen(), 'Restart', MAP_WIDTH + 30, 130, BUTTON_COLOR, False)
        self.__giveup_button = Button(self.get_screen(), 'GiveUp', MAP_WIDTH + 30, BUTTON_HEIGHT + 160, BUTTON_COLOR,
                                      True)
        self.__return_button = Button(self.get_screen(), 'Menu',
                                      MAP_WIDTH + 30, 2 * BUTTON_HEIGHT + 190, BUTTON_COLOR, True)

    def reset(self):
        for y in range(self.get_height()):
            for x in range(self.get_width()):
                self.__map[y][x] = 0
        self.__steps = []

    @staticmethod
    def reverse_turn(turn):
        if turn == MapEntryType.MAP_PLAYER_ONE:
            return MapEntryType.MAP_PLAYER_TWO
        else:
            return MapEntryType.MAP_PLAYER_ONE

    @staticmethod
    def get_map_unit_rect(x, y):
        map_x = x * REC_SIZE
        map_y = y * REC_SIZE
        return map_x, map_y, REC_SIZE, REC_SIZE

    @staticmethod
    def map_pos_to_index(map_x, map_y):
        return map_x // REC_SIZE, map_y // REC_SIZE

    @staticmethod
    def is_in_map(map_x, map_y):
        return 0 < map_x < MAP_WIDTH and 0 < map_y < MAP_HEIGHT

    def is_empty(self, x, y):
        return self.__map[y][x] == 0

    def click(self, x, y, type):
        self.__map[y][x] = type
        self.__steps.append((x, y))

    def draw_chess(self, screen):
        player_color = [PLAYER_ONE_COLOR, PLAYER_TWO_COLOR]
        for i in range(len(self.__steps)):
            x, y = self.__steps[i]
            map_x, map_y, width, height = ChessMap.get_map_unit_rect(x, y)
            pos, radius = (map_x + width // 2, map_y + height // 2), CHESS_RADIUS
            turn = self.__map[y][x]
            if turn == 1:
                op_turn = 2
            else:
                op_turn = 1
            pygame.draw.circle(screen, player_color[turn - 1], pos, radius)
            font = Text(self.get_screen(), None, REC_SIZE * 2 // 3, str(i), player_color[op_turn - 1], *pos)
            screen.blit(*font.get_text_element())
        if len(self.__steps) > 0:
            last_pos = self.__steps[-1]
            map_x, map_y, width, height = ChessMap.get_map_unit_rect(last_pos[0], last_pos[1])
            line_list = [(map_x, map_y), (map_x + width, map_y),
                         (map_x + width, map_y + height), (map_x, map_y + height)]
            pygame.draw.lines(screen, PURPLE_COLOR, True, line_list, 1)

    def change_mouse_show(self):
        map_x, map_y = pygame.mouse.get_pos()
        x, y = self.map_pos_to_index(map_x, map_y)
        if self.is_in_map(map_x, map_y) and self.is_empty(x, y):
            pygame.mouse.set_visible(False)
            pos, radius = (map_x, map_y), CHESS_RADIUS
            pygame.draw.circle(self.get_screen(), LIGHT_RED, pos, radius)
        else:
            pygame.mouse.set_visible(True)

    def draw_background(self):
        color = (0, 0, 0)
        for y in range(self.get_height()):
            # 画横线
            start_pos, end_pos = (REC_SIZE // 2, REC_SIZE // 2 + REC_SIZE * y), \
                                 (MAP_WIDTH - REC_SIZE // 2, REC_SIZE // 2 + REC_SIZE * y)
            if y == self.get_height() // 2:
                width = 2
            else:
                width = 1
            pygame.draw.line(self.get_screen(), color, start_pos, end_pos, width)
        for x in range(self.get_width()):
            # 画竖线
            start_pos, end_pos = (REC_SIZE // 2 + REC_SIZE * x, REC_SIZE // 2), \
                                 (REC_SIZE // 2 + REC_SIZE * x, MAP_HEIGHT - REC_SIZE // 2)
            if x == self.get_width() // 2:
                width = 2
            else:
                width = 1
            pygame.draw.line(self.get_screen(), color, start_pos, end_pos, width)

        rec_size = 8
        pos = [(3, 3), (11, 3), (3, 11), (11, 11), (7, 7)]
        for x, y in pos:
            pygame.draw.rect(self.get_screen(), color,
                             (REC_SIZE // 2 + REC_SIZE * x - rec_size // 2,
                              REC_SIZE // 2 + REC_SIZE * y - rec_size // 2,
                              rec_size, rec_size))
        self.draw_button()

    def show_winner(self, winner):
        def show_font(screen, text, location_x, location_y, height):
            font = Text(screen, None, height, text, (0, 0, 255), location_x, location_y)
            screen.blit(*font.get_text_element())

        if winner is None:
            return
        if winner == MapEntryType.MAP_PLAYER_ONE:
            string = 'Winner is Black'
        else:
            string = 'Winner is White'
        show_font(self.get_screen(), string, MAP_WIDTH + 100, SCREEN_HEIGHT - 45, 30)
        pygame.mouse.set_visible(True)

    def draw_button(self):
        self.__restart_button.draw()
        self.__giveup_button.draw()
        self.__return_button.draw()

    def draw_yagoo(self):
        yagoo = pygame.image.load('./source/image/yagoo.jpg')
        yagoo = pygame.transform.scale(yagoo, (100, 100))
        self.get_screen().blit(yagoo, (MAP_WIDTH + 30, 15))

    def check_buttons(self, game, mouse_x, mouse_y):
        if self.__restart_button.get_rect().collidepoint(mouse_x, mouse_y):
            self.click_restart_button(game)
        elif self.__giveup_button.get_rect().collidepoint(mouse_x, mouse_y):
            self.click_giveup_button(game)
        elif self.__return_button.get_rect().collidepoint(mouse_x, mouse_y):
            self.click_return_button(game)

    @staticmethod
    def click_return_button(game):
        game.reset()

    def click_restart_button(self, game):
        if not game.get_is_play():
            game.set_is_play(True)
            game.start()
            game.set_winner(None)
        self.__restart_button.set_enable(False)
        self.__giveup_button.set_enable(True)

    def click_giveup_button(self, game):
        if game.get_is_play():
            game.set_is_play(False)
            if game.get_winner() is None:
                game.set_winner(game.get_map().reverse_turn(game.get_player()))
        self.__giveup_button.set_enable(False)
        self.__restart_button.set_enable(True)

    def get_map(self):
        return self.__map
