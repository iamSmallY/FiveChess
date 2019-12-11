import pygame
from Settings import *
from Button import *
import abc


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

    @abc.abstractmethod
    def click_button(self, game, button):
        pass

    @abc.abstractmethod
    def get_button(self):
        pass


class StartMap(AbstractMap):
    def __init__(self, screen, width, height):
        super().__init__(screen, width, height)

        self.__back_img = pygame.image.load('./source/image/background.jpg')
        self.__back_img = pygame.transform.scale(self.__back_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.__title_font = pygame.font.Font(None, TITLE_HEIGHT)
        self.__title_image = self.__title_font.render('Five Chess', True, BLACK_COLOR)
        self.__title_image_rect = self.__title_image.get_rect()
        self.__title_image_rect.center = (TITLE_X, TITLE_Y)

        self.__start_button = StartButton(self.get_screen(), 'Start', TITLE_X-BUTTON_WIDTH//2, TITLE_Y+TITLE_HEIGHT)
        self.__model_button = UseAIButton(self.get_screen(), 'PVE', TITLE_X-BUTTON_WIDTH//2, TITLE_Y+TITLE_HEIGHT+60)

    def reset(self):
        self.__start_button = StartButton(self.get_screen(), 'Start', TITLE_X-BUTTON_WIDTH//2, TITLE_Y+TITLE_HEIGHT)
        self.__model_button = UseAIButton(self.get_screen(), 'PVE', TITLE_X-BUTTON_WIDTH//2, TITLE_Y+TITLE_HEIGHT+60)

    def draw_background(self):
        pygame.draw.rect(self.get_screen(), WHITE_COLOR, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.get_screen().blit(self.__back_img, (0, 0))
        self.get_screen().blit(self.__title_image, self.__title_image_rect)
        self.draw_button()

    def draw_button(self):
        self.__start_button.draw()
        self.__model_button.draw()

    def check_buttons(self, game, mouse_x, mouse_y):
        if self.__start_button.get_rect().collidepoint(mouse_x, mouse_y):
            self.click_button(game, self.__start_button)
            return True
        elif self.__model_button.get_rect().collidepoint(mouse_x, mouse_y):
            self.click_button(game, self.__model_button)
            return False

    def click_button(self, game, button):
        button.click(game)


class ChessMap(AbstractMap):
    def __init__(self, screen, width, height):
        super().__init__(screen, width, height)
        self.__map = [[0 for x in range(self.get_width())] for y in range(self.get_height())]
        self.__steps = []
        self.__buttons = []
        self.__buttons.append(StartButton(self.get_screen(), 'Start', MAP_WIDTH + 30, 15))
        self.__buttons.append(GiveUpButton(self.get_screen(), 'GiveUp', MAP_WIDTH + 30, BUTTON_HEIGHT + 45))
        self.__useAI_button = UseAIButton(self.get_screen(), 'PVE', MAP_WIDTH + 30, 2 * BUTTON_HEIGHT + 75)

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
        font = pygame.font.SysFont(None, REC_SIZE * 2 // 3)
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
            msg_image = font.render(str(i), True, player_color[op_turn - 1], player_color[turn - 1])
            msg_image_rect = msg_image.get_rect()
            msg_image_rect.center = pos
            screen.blit(msg_image, msg_image_rect)
        if len(self.__steps) > 0:
            last_pos = self.__steps[-1]
            map_x, map_y, width, height = ChessMap.get_map_unit_rect(last_pos[0], last_pos[1])
            line_list = [(map_x, map_y), (map_x + width, map_y),
                         (map_x + width, map_y + height), (map_x, map_y + height)]
            pygame.draw.lines(screen, PURPLE_COLOR, True, line_list, 1)

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

    def draw_button(self):
        for button in self.__buttons:
            button.draw()
        self.__useAI_button.draw()

    def click_button(self, game, button):
        if button.click(game, self.__useAI_button):
            for temp in self.__buttons:
                if temp != button:
                    temp.not_click()

    def check_buttons(self, game, mouse_x, mouse_y):
        for button in self.__buttons:
            if button.get_rect().collidepoint(mouse_x, mouse_y):
                self.click_button(game, button)
                break
        else:
            if self.__useAI_button.get_rect().collidepoint(mouse_x, mouse_y):
                self.__useAI_button.click(game)

    def get_button(self):
        return self.__buttons

    def get_map(self):
        return self.__map


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('test')
    mapp = StartMap(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    mapp.draw_background()
    while True:
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
