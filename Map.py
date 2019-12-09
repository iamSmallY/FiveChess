import pygame
from Settings import *


class Map(object):
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__map = [[0for x in range(self.__width)] for y in range(self.__height)]
        self.__steps = []

    def reset(self):
        for y in range(self.__height):
            for x in range(self.__width):
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
        return map_x//REC_SIZE, map_y//REC_SIZE

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
        font = pygame.font.SysFont(None, REC_SIZE*2//3)
        for i in range(len(self.__steps)):
            x, y = self.__steps[i]
            map_x, map_y, width, height = Map.get_map_unit_rect(x, y)
            pos, radius = (map_x + width//2, map_y + height//2), CHESS_RADIUS
            turn = self.__map[y][x]
            if turn == 1:
                op_turn = 2
            else:
                op_turn = 1
            pygame.draw.circle(screen, player_color[turn-1], pos, radius)
            msg_image = font.render(str(i), True, player_color[op_turn-1], player_color[turn-1])
            msg_image_rect = msg_image.get_rect()
            msg_image_rect.center = pos
            screen.blit(msg_image, msg_image_rect)
        if len(self.__steps) > 0:
            last_pos = self.__steps[-1]
            map_x, map_y, width, height = Map.get_map_unit_rect(last_pos[0], last_pos[1])
            line_list = [(map_x, map_y), (map_x + width, map_y),
                          (map_x + width, map_y + height), (map_x, map_y + height)]
            pygame.draw.lines(screen, PURPLE_COLOR, True, line_list, 1)

    def draw_background(self, screen):
        color = (0, 0, 0)
        for y in range(self.__height):
            # 画横线
            start_pos, end_pos = (REC_SIZE//2, REC_SIZE//2 + REC_SIZE*y),\
                                 (MAP_WIDTH - REC_SIZE//2, REC_SIZE//2 + REC_SIZE*y)
            if y == self.__height // 2:
                width = 2
            else:
                width = 1
            pygame.draw.line(screen, color, start_pos, end_pos, width)
        for x in range(self.__width):
            # 画竖线
            start_pos, end_pos = (REC_SIZE//2 + REC_SIZE*x, REC_SIZE//2),\
                                 (REC_SIZE//2 + REC_SIZE*x, MAP_HEIGHT - REC_SIZE//2)
            if x == self.__width // 2:
                width = 2
            else:
                width = 1
            pygame.draw.line(screen, color, start_pos, end_pos, width)

        rec_size = 8
        pos = [(3, 3), (11, 3), (3, 11), (11, 11), (7, 7)]
        for x, y in pos:
            pygame.draw.rect(screen, color, (REC_SIZE//2 + REC_SIZE*x - rec_size//2, REC_SIZE//2 + REC_SIZE*y - rec_size//2, rec_size, rec_size))

    def get_map(self):
        return self.__map
