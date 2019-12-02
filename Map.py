from Map_Entry_Type import *
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

    def click(self, x, y, type):
        self.__map[y][x] = type.value()
        self.__steps.append((x, y))

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
