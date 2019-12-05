from Game import *
from Map import *
import copy
import time


class ChessAI(object):
    def __init__(self, chess_len):
        self.__max_depth = AI_SEARCH_DEPTH
        self.__beta = 0
        self.__alpha = 0
        self.__best_move = None

        self.__len = chess_len

        self.__record = [[[0, 0, 0, 0] for x in range(chess_len)] for y in range(chess_len)]
        self.__count = [[0 for x in range(CHESS_TYPE_NUM)] for y in range(2)]
        # self.__pos_score = [[7-max(abs(x-7), abs(y-7)) for x in range(chess_len)] for y in range(chess_len)]
        # self.__save_count = 0

    def reset(self):
        for y in range(self.__len):
            for x in range(self.__len):
                for i in range(4):
                    self.__record[y][x][i] = 0
        for i in range(len(self.__count)):
            for j in range(len(self.__count[0])):
                self.__count[i][j] = 0
        # self.__save_count = 0

    @staticmethod
    def click(map, x, y, turn):
        map.click(x, y, turn)

    def is_win(self, board, turn):
        return self.evaluate(board, turn, True)

    def evaluate_point_score(self, board, x, y, mine, opponent):
        dir_offset = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for i in range(len(self.__count)):
            for j in range(len(self.__count[0])):
                self.__count[i][j] = 0

        board[y][x] = mine
        self.evaluate_point(board, x, y, mine, opponent, self.__count[mine-1])
        mine_count = self.__count[mine-1]
        board[y][x] = opponent
        self.evaluate_point(board, x, y, opponent, mine, self.__count[opponent-1])
        opponent_count = self.__count[opponent-1]
        board[y][x] = 0

        m_score = self.get_point_score(mine_count)
        o_score = self.get_point_score(opponent_count)

        return m_score, o_score

    def has_neighbor(self, board, x, y, radius):
        start_x, end_x = x-radius, x+radius
        start_y, end_y = y-radius, y+radius

        for i in range(start_y, end_y+1):
            for j in range(start_x, end_x+1):
                if 0 <= i < self.__len and 0 <= j < self.__len:
                    if board[i][j] != 0:
                        return True
        return False

    def get_can_move(self, board, turn):
        fives = []
        mfours, ofours = [], []
        msfours, osfours = [], []
        if turn == MapEntryType.MAP_PLAYER_ONE:
            mine, opponent = 1, 2
        else:
            mine, opponent = 2, 1

        moves = []
        radius = 1

        for y in range(self.__len):
            for x in range(self.__len):
                if board[y][x] == 0 and self.has_neighbor(board, x, y, radius):
                    m_score, o_score = self.evaluate_point_score(board, x, y, mine, opponent)
                    point = (max(m_score, o_score), x, y)

                    if m_score >= SCORE_FIVE or o_score >= SCORE_FIVE:
                        fives.append(point)
                    elif m_score >= SCORE_FOUR:
                        mfours.append(point)
                    elif o_score >= SCORE_FOUR:
                        ofours.append(point)
                    elif m_score >= SCORE_SFOUR:
                        msfours.append(point)
                    elif o_score >= SCORE_SFOUR:
                        osfours.append(point)

                    moves.append(point)

        if len(fives) > 0:
            return fives
        if len(mfours) > 0:
            return mfours
        if len(ofours) > 0:
            if len(msfours) > 0:
                return ofours
            else:
                return ofours+msfours

        moves.sort(reverse=True)

        if self.__max_depth > 2 and len(moves) > AI_LIMITED_MOVE_NUM:
            moves = moves[:AI_LIMITED_MOVE_NUM]
        return moves

    def cut_search(self, board, turn, depth, alpha=SCORE_MIN, beta=SCORE_MAX):
        score = self.evaluate(board, turn)
        if depth <= 0 or abs(score) >= SCORE_FIVE:
            return score

        moves = self.get_can_move(board, turn)
        if len(moves) == 0:
            return score

        best_move = None
        self.__alpha += len(moves)

        for _, x, y in moves:
            board[y][x] = turn

            op_turn = MapEntryType.MAP_PLAYER_TWO if turn == MapEntryType.MAP_PLAYER_ONE else MapEntryType.MAP_PLAYER_ONE

            score = -1 * self.cut_search(board, op_turn, depth-1, -beta, -alpha)

            board[y][x] = 0
            self.__beta += 1

            if score > alpha:
                alpha = score
                best_move = (x, y)
                if alpha >= beta:
                    break

        if depth == self.__max_depth and best_move:
            self.__best_move = best_move

        return alpha

    def search(self, board, turn, depth=4):
        self.__max_depth = depth
        self.__best_move = None
        score = self.cut_search(board, turn, depth)
        x, y = self.__best_move
        return score, x, y

    def find_best_chess(self, board, turn):
        self.__alpha = 0
        self.__beta = 0
        score, x, y = self.search(board, turn)
        return x, y

    @staticmethod
    def get_point_score(count):
        score = 0
        if count[FIVE] > 0:
            return SCORE_FIVE

        if count[FOUR] > 0:
            return SCORE_FOUR

        if count[SFOUR] > 1:
            score += count[SFOUR] * SCORE_SFOUR
        elif count[SFOUR] > 0 and count[THREE] > 0:
            score += count[SFOUR] * SCORE_SFOUR
        elif count[SFOUR] > 0:
            score += SCORE_THREE

        if count[THREE] > 1:
            score += 5 * SCORE_THREE
        elif count[THREE] > 0:
            score += SCORE_THREE

        if count[STHREE] > 0:
            score += count[STHREE] * SCORE_STHREE
        if count[TWO] > 0:
            score += count[TWO] * SCORE_TWO
        if count[STWO] > 0:
            score += count[STWO] * SCORE_STWO

        return score

    @staticmethod
    def get_score(mine_count, opponent_count):
        m_score, o_score = 0, 0
        if mine_count[FIVE] > 0:
            return SCORE_FIVE, 0
        if opponent_count[FIVE] > 0:
            return 0, SCORE_FIVE

        if mine_count[SFOUR] >= 2:
            mine_count[FOUR] += 1
        if opponent_count[SFOUR] >= 2:
            opponent_count[FOUR] += 1

        if mine_count[FOUR] > 0:
            return 9050, 0
        if mine_count[SFOUR] > 0:
            return 9040, 0

        if opponent_count[FOUR] > 0:
            return 0, 9030
        if opponent_count[SFOUR] > 0 and opponent_count[THREE] > 0:
            return 0, 9020

        if mine_count[THREE] > 0 and opponent_count[SFOUR] == 0:
            return 9010, 0

        if opponent_count[THREE] > 1 and mine_count[THREE] == 0 and mine_count[STHREE] == 0:
            return 0, 9000

        if opponent_count[SFOUR] > 0:
            m_score += 400

        if mine_count[THREE] > 1:
            m_score += 500
        elif mine_count[THREE] == 1:
            m_score += 100

        if opponent_count[THREE] > 1:
            o_score += 2000
        elif opponent_count[THREE] == 1:
            o_score += 400

        if mine_count[STHREE] > 0:
            m_score += mine_count[STHREE] * 10
        if opponent_count[STHREE] > 0:
            o_score += opponent_count[STHREE] * 10

        if mine_count[TWO] > 0:
            m_score += mine_count[TWO] * 6
        if opponent_count[TWO] > 0:
            o_score += opponent_count[STWO] * 6

        if mine_count[STWO] > 0:
            m_score += mine_count[STWO] * 2
        if opponent_count[STWO] > 0:
            o_score += opponent_count[STWO] * 2

        return m_score, o_score

    def evaluate(self, board, turn, check_win=False):
        self.reset()

        if turn == MapEntryType.MAP_PLAYER_ONE:
            mine, opponent = 1, 2
        else:
            mine, opponent = 2, 1

        for y in range(self.__len):
            for x in range(self.__len):
                if board[y][x] == mine:
                    self.evaluate_point(board, x, y, mine, opponent)
                elif board[y][x] == opponent:
                    self.evaluate_point(board, x, y, opponent, mine)

        mine_count = self.__count[mine-1]
        opponent_count = self.__count[opponent-1]
        if check_win:
            return mine_count[FIVE] > 0
        else:
            m_score, o_score = self.get_score(mine_count, opponent_count)
            return m_score-o_score

    def evaluate_point(self, board, x, y, mine, opponent, count=None):
        dir_offset = [(1, 0), (0, 1), (1, 1), (1, -1)]
        ignore_record = True
        if count is None:
            count = self.__count[mine-1]
            ignore_record = False
        for i in range(4):
            if self.__record[y][x][i] == 0 or ignore_record:
                self.analysis_line(board, x, y, i, dir_offset[i], mine, opponent, count)

    def get_line(self, board, x, y, dir_offset, mine, opponent):
        line = [0 for i in range(9)]

        temp_x = x + (-5 * dir_offset[0])
        temp_y = y + (-5 * dir_offset[1])
        for i in range(9):
            temp_x += dir_offset[0]
            temp_y += dir_offset[1]
            if temp_x < 0 or temp_x >= self.__len or\
               temp_y < 0 or temp_y >= self.__len:
                line[i] = opponent
            else:
                line[i] = board[temp_y][temp_x]
        return line

    def analysis_line(self, board, x, y, dir_index, dir, mine, opponent, count):
        def set_record(_x, _y, _left, _right, _dir_index, _dir_offset):
            temp_x = x + (-5 + _left) * _dir_offset[0]
            temp_y = y + (-5 + _left) * _dir_offset[1]
            for i in range(_left, _right+1):
                temp_x += _dir_offset[0]
                temp_y += _dir_offset[1]
                self.__record[temp_y][temp_x][_dir_index] = 1

        empty = MapEntryType.MAP_EMPTY.value
        left_idx, right_idx = 4, 4

        line = self.get_line(board, x, y, dir, mine, opponent)

        while right_idx < 8:
            if line[right_idx+1] != mine:
                break
            right_idx += 1
        while left_idx > 0:
            if line[left_idx-1] != mine:
                break
            left_idx -= 1

        left_range, right_range = left_idx, right_idx
        while right_range < 8:
            if line[right_range+1] == opponent:
                break
            right_range += 1
        while left_range > 0:
            if line[left_range-1] == opponent:
                break
            left_range -= 1

        chess_range = right_range - left_range + 1
        if chess_range < 5:
            set_record(x, y, left_range, right_range, dir_index, dir)
            return ChessType.NONE

        set_record(x, y, left_idx, right_idx, dir_index, dir)

        m_range = right_idx - left_idx + 1

        # M: mine, P: opponent, E: empty
        if m_range >= 5:
            count[FIVE] += 1

        # FOUR: XMMMMX
        # SFOUR: XMMMMP, PMMMMX
        if m_range == 4:
            left_empty = right_empty = False
            if line[left_idx-1] == empty:
                left_empty = True
            if line[right_idx+1] == empty:
                right_empty = True
            if left_empty and right_empty:
                count[FOUR] += 1
            elif left_empty or right_empty:
                count[SFOUR] += 1

        # SFOUR: MXMMM or MMMXM
        # THREE: XMMMXX, XXMMMX
        # STHREE: PMMMX, XMMMP, PXMMMXP
        if m_range == 3:
            left_empty = right_empty = False
            left_four = right_four = False
            if line[left_idx-1] == empty:
                if line[left_idx-2] == mine:  # MXMMM
                    set_record(x, y, left_idx-2, left_idx-1, dir_index, dir)
                    count[SFOUR] += 1
                    left_four = True
                left_empty = True

            if line[right_idx+1] == empty:
                if line[right_idx+2] == mine:  # MMMXM
                    set_record(x, y, right_idx+1, right_idx+2, dir_index, dir)
                    count[SFOUR] += 1
                    right_four = True
                right_empty = True

            if left_four or right_four:
                pass
            elif left_empty and right_empty:
                if chess_range > 5:  # XMMMXX, XXMMMX
                    count[THREE] += 1
                else:  # PXMMMXP
                    count[STHREE] += 1
            elif left_empty or right_empty:  # PMMMX, XMMMP
                count[STHREE] += 1

            # SFOUR: MMXMM
            # THREE: XMXMMX or XMMXMX
            # STHREE: PMXMMX, XMXMMP, PMMXMX, XMMXMP
            # TWO: XMMX
            # STWO: PMMX, XMMP
            if m_range == 2:
                left_empty = right_empty = False
                left_three = right_three = False
                if line[left_idx-1] == empty:
                    if line[left_idx-2] == mine:
                        set_record(x, y, left_idx-2, left_idx-1, dir_index, dir)
                        if line[left_idx-3] == empty:
                            if line[right_idx+1] == empty:  # XMXMMX
                                count[THREE] += 1
                            else:  # XMXMMP
                                count[STHREE] += 1
                            left_three = True
                        elif line[left_idx-3] == opponent:  # PMXMMX
                            if line[right_idx+1] == empty:
                                count[STHREE] += 1
                                left_three = True

                    left_empty = True

                if line[right_idx+1] == empty:
                    if line[right_idx+2] == mine:
                        if line[right_idx+3] == mine:  # MMXMM
                            set_record(x, y, right_idx+1, right_idx+2, dir_index, dir)
                            count[SFOUR] += 1
                            right_three = True
                        elif line[right_idx+3] == empty:
                            if left_empty:  # XMMXMX
                                count[THREE] += 1
                            else:  # PMMXMX
                                count[STHREE] += 1
                            right_three = True
                        elif left_empty:  # XMMXMP
                            count[STHREE] += 1
                            right_three = True

                    right_empty = True

                if left_three or right_three:
                    pass
                elif left_empty and right_empty:  # XMMX
                    count[TWO] += 1
                elif left_empty or right_empty:  # PMMX, XMMP
                    count[STWO] += 1

            # Live Two: XMXMX, XMXXMX only check right direction
            # Sleep Two: PMXMX, XMXMP
            if m_range == 1:
                left_empty = right_empty = False
                if line[left_idx - 1] == empty:
                    if line[left_idx - 2] == mine:
                        if line[left_idx - 3] == empty:
                            if line[right_idx + 1] == opponent:  # XMXMP
                                count[STWO] += 1
                    left_empty = True

                if line[right_idx + 1] == empty:
                    if line[right_idx + 2] == mine:
                        if line[right_idx + 3] == empty:
                            if left_empty:  # XMXMX
                                # setRecord(self, x, y, left_idx, right_idx+2, dir_index, dir)
                                count[TWO] += 1
                            else:  # PMXMX
                                count[STWO] += 1
                    elif line[right_idx + 2] == empty:
                        if line[right_idx + 3] == mine and line[right_idx + 4] == empty:  # XMXXMX
                            count[TWO] += 1

            return ChessType.NONE
