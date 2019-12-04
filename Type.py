from enum import IntEnum


class MapEntryType(IntEnum):
    MAP_EMPTY = 0,
    MAP_PLAYER_ONE = 1,
    MAP_PLAYER_TWO = 2,
    MAP_NONE = 3,


class ChessType(IntEnum):
    NONE = 0,
    SLEEP_TWO = 1,
    LIVE_TWO = 2,
    SLEEP_THREE = 3,
    LIVE_THREE = 4,
    CHONG_FOUR = 5,
    LIVE_FOUR = 6,
    LIVE_FIVE = 7,
