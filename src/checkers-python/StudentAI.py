from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and existing functions and variables.
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
        self.max_depth = 3
        self.color_map = {2:'W', 1:'B'}

    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        move = self.mini_max_search()
        return move

    def mini_max_search(self):
        res, best_move = self.max_val(0, float('-inf'), float('inf'))
        return best_move

    def max_val(self, curr_depth, alpha, beta):
        if curr_depth == self.max_depth:
            return self.board_score(self.color), None
        moves = self.board.get_all_possible_moves(self.color)
        if len(moves) == 0:
            return self.board_score(self.color), None
        res = float('-inf')
        best_move = None
        for move_seq in moves:
            for move in move_seq:
                self.board.make_move(move, self.color)
                res = max(res, self.min_val(curr_depth + 1, alpha, beta)[0])
                if res > alpha:
                    alpha = res
                    best_move = move
                if alpha >= beta:
                    return res, best_move
                self.board.undo()
        return res, best_move

    def min_val(self, curr_depth, alpha, beta):
        if curr_depth == self.max_depth:
            return self.board_score(self.opponent[self.color]), None
        moves = self.board.get_all_possible_moves(self.opponent[self.color])
        if len(moves) == 0:
            return self.board_score(self.opponent[self.color]), None
        res = float('inf')
        best_move = None
        for move_seq in moves:
            for move in move_seq:
                self.board.make_move(move, self.opponent[self.color])
                res = min(res, self.max_val(curr_depth + 1, alpha, beta)[0])
                if res < beta:
                    beta = res
                    best_move = move
                if alpha >= beta:
                    return res, best_move
                self.board.undo()
        return res, best_move

    def board_score(self, turn):
        win = self.board.is_win(self.color_map[turn])
        if win == self.color:
            return float('inf')
        elif win == self.opponent[self.color]:
            return float('-inf')
        else:
            score = 0
            for c in range(self.col):
                for r in range(self.row):
                    piece = self.board.board[c][r]
                    if piece.get_color() == self.color:
                        if piece.is_king:
                            score += 2
                        else:
                            score += 1
                    elif piece.get_color() == self.opponent[self.color]:
                        if piece.is_king:
                            score -= 2
                        else:
                            score -= 1
            return score


