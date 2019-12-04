from Game import *
from Map import *
import copy
import time


class ChessAI(object):
    def __init__(self, chess_len):
        self.__len = chess_len

        self.__record = [[[0, 0, 0, 0] for x in range(chess_len)] for y in range(chess_len)]
        self.__count = [[0 for x in range(CHESS_TYPE_NUM)] for y in range(2)]
        self.__pos_score = [[7-max(abs(x-7), abs(y-7)) for x in range(chess_len)] for y in range(chess_len)]
        self.__save_count = 0

    def reset(self):
        for y in range(self.__len):
            for x in range(self.__len):
                for i in range(4):
                    self.__record[y][x][i] = 0
        for i in range(len(self.__count)):
            for j in range(len(self.__count[0])):
                self.__count[i][j] = 0
        self.__save_count = 0

    def is_win(self, board, turn):
        return self.evaluate(board, turn, True)

    def get_can_move(self, board):
        moves = []
        for y in range(self.__len):
            for x in range(self.__len):
                if board[y][x] == 0:
                    score = self.__pos_score[y][x]
                    moves.append((score, x, y))
        moves.sort(reverse=True)
        return moves

    def search(self, board, turn):
        moves = self.get_can_move(board)
        best_move = None
        max_score = -0x7fffffff
        for score, x, y in moves:
            board[y][x] = turn.value
            score = self.evaluate(board, turn)
            board[y][x] = 0

            if score > max_score:
                max_score = score
                best_move = (max_score, x, y)
        return best_move

    def find_best_chess(self, board, turn):
        score, x, y = self.search(board, turn)
        return x, y

    def get_score(self,  mine_count, opponent_count):
        m_score, o_score = 0, 0
        if mine_count[FIVE] > 0:
            return 10000, 0
        if opponent_count[FIVE] > 0:
            return 0, 10000

        if mine_count[SFOUR] >= 2:
            mine_count[FOUR] += 1

        if opponent_count[FOUR] > 0:
            return 0, 9050
        if opponent_count[SFOUR] > 0:
            return 0, 9040

        if mine_count[FOUR] > 0:
            return 9030, 0
        if mine_count[SFOUR] > 0 and mine_count[THREE] > 0:
            return 9020, 0

        if opponent_count[THREE] > 0 and mine_count[SFOUR] == 0:
            return 0, 9010

        if mine_count[THREE] > 1 and opponent_count[THREE] == 0 and opponent_count[STHREE] == 0:
            return 9000, 0

        if mine_count[SFOUR] > 0:
            m_score += 2000

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
            m_score += mine_count[TWO] * 4
        if opponent_count[TWO] > 0:
            o_score += opponent_count[STWO] * 4

        if mine_count[STWO] > 0:
            m_score += mine_count[STWO] * 4
        if opponent_count[STWO] > 0:
            o_score += opponent_count[STWO] * 4

        return m_score, o_score

    def evaluate(self, board, turn, check_win = False):
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

    def evaluate_point(self, board, x, y, mine, opponent):
        dir_offset = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for i in range(4):
            if self.__record[y][x][i] == 0:
                self.analysis_line(board, x, y, i, dir_offset[i], mine, opponent, self.__count[mine-1])
            else:
                self.__save_count += 1

    def get_line(self, board, x, y, dir_offset, mine, opponent):
        line = [0 for i in range(9)]

        temp_x = x + (-5 * dir_offset[0])
        temp_y = y + (-5 * dir_offset[1])
        for i in range(9):
            temp_x += dir_offset[0]
            temp_y += dir_offset[1]
            if temp_x < 0 or temp_x >= self.__len or temp_y < 0 or temp_y >= self.__len:
                line[i] = opponent
            else:
                line[i] = board[temp_y][temp_x]
        return line

    def analysis_line(self, board, x, y, dir_index, dir, mine, opponent, count):
        def set_record(_x, _y, _left, _right, _dir_index, _dir_offset):
            temp_x = x + (-5 + _left) * _dir_offset[0]
            temp_y = y + (-5 + _left) * _dir_offset[1]
            for i in range(_left, _right):
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
        if m_range == 5:
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
                if line[left_idx-2] == mine: # MXMMM
                    set_record(x, y, left_idx-2, left_idx-1, dir_index, dir)
                    count[SFOUR] += 1
                    left_four = True
                left_empty = True

            if line[right_idx+1] == empty:
                if line[right_idx+2] == mine: #MMMXM
                    set_record(x, y, right_idx+1, right_idx+2, dir_index, dir)
                    count[SFOUR] += 1
                    right_four = True
                right_empty = True

            if left_four or right_four:
                pass
            elif left_empty and right_empty:
                if chess_range > 5: # XMMMXX, XXMMMX
                    count[THREE] += 1
                else: # PXMMMXP
                    count[STHREE] += 1
            elif left_empty or right_empty: #PMMMX, XMMMP
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
                            if line[right_idx+1] ==empty: #XMXMMX
                                count[THREE] += 1
                            else: #XMXMMP
                                count[STHREE] += 1
                            left_three = True
                        elif line[left_idx-3] == opponent: # PMXMMX
                            if line[right_idx+1] == empty:
                                count[STHREE] += 1
                                left_three = True

                    left_empty = True

                if line[right_idx+1] == empty:
                    if line[right_idx+2] == mine:
                        if line[right_idx+3] == mine: # MMXMM
                            set_record(x, y, right_idx+1, right_idx+2, dir_index, dir)
                            count[SFOUR] += 1
                            right_three = True
                        elif line[right_idx+3] == empty:
                            if left_empty: # XMMXMX
                                count[THREE] += 1
                            else: # PMMXMX
                                count[STHREE] += 1
                            right_three = True
                        elif left_empty: # XMMXMP
                            count[STHREE] += 1
                            right_three = True

                    right_empty = True

                if left_three or right_three:
                    pass
                elif left_empty and right_empty: # XMMX
                    count[TWO] += 1
                elif left_empty or right_empty: # PMMX, XMMP
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
