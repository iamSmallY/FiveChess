from Type import *

GAME_VERSION = '1.0'

REC_SIZE = 50
CHESS_RADIUS = REC_SIZE//2 - 2
CHESS_LEN = 15
MAP_WIDTH = CHESS_LEN * REC_SIZE
MAP_HEIGHT = CHESS_LEN * REC_SIZE

INFO_WIDTH = 200
BUTTON_WIDTH = 140
BUTTON_HEIGHT = 50
BUTTON_COLOR = [(26, 173, 25), (158, 217, 157)]

SCREEN_WIDTH = MAP_WIDTH + INFO_WIDTH
SCREEN_HEIGHT = MAP_HEIGHT

PLAYER_ONE_COLOR = (255, 251, 240)
PLAYER_TWO_COLOR = (88, 87, 86)
PURPLE_COLOR = (255, 0, 255)
LIGHT_YELLOW = (247, 238, 214)
LIGHT_RED = (213, 90, 107)
TEXT_COLOR = (255, 255, 255)

CHESS_TYPE_NUM = 8
FIVE = ChessType.LIVE_FIVE.value
FOUR = ChessType.LIVE_FOUR.value
THREE = ChessType.LIVE_THREE.value
TWO = ChessType.LIVE_TWO.value

SFOUR = ChessType.CHONG_FOUR.value
STHREE = ChessType.SLEEP_THREE.value
STWO = ChessType.SLEEP_TWO.value
