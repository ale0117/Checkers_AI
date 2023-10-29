from random import randint
from BoardClasses import Move
from BoardClasses import Board
import Checker
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
        self.board.make_move(move, self.color)
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
        best_move = moves[0][0]
        for move_seq in moves:
            for move in move_seq:
                self.board.make_move(move, self.color)
                score = self.min_val(curr_depth + 1, alpha, beta)[0]
                if score >= res:
                    res = score
                    best_move = move
                alpha = max(alpha, res)
                if alpha >= beta:
                    self.board.undo()
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
        best_move = moves[0][0]
        for move_seq in moves:
            for move in move_seq:
                self.board.make_move(move, self.opponent[self.color])
                score = self.max_val(curr_depth + 1, alpha, beta)[0]
                if score <= res:
                    res = score
                    best_move = move
                alpha = min(alpha, res)
                if alpha >= beta:
                    self.board.undo()
                    return res, best_move
                self.board.undo()
        return res, best_move

    def board_score(self, turn):
        ai_score = 0
        opponent_score = 0
        tie_breaker = randint(0, 10)
        for r in range(self.row):
            for c in range(self.col):
                piece = self.board.board[r][c]
                if piece.get_color() == self.color_map[self.color]:
                    if piece.is_king:
                        ai_score += 2000
                        # encourage king to take space in mid
                        ai_score += ((self.row - 1) / 2 * 100) - (abs((self.row - 1)/ 2 - r) * 100)
                        ai_score += ((self.col - 1) / 2 * 50) - (abs((self.col -1)/ 2 - c) * 50)
                    else:
                        ai_score += 1000
                        # encourage normal pieces to move towards other end to become king
                        if self.color != 1:
                            ai_score += (self.row - r) / self.row * 1000
                        else:
                            ai_score += (r+1) / self.row * 1000
                    outside = 0
                    for x in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        if not(self.board.is_in_board(r + x[0], c + x[1])):
                            outside += 1
                            if outside == 2:
                                ai_score += 100 # add points for being at edge
                            if outside == 3:
                                ai_score -= 300 # subtract points for being at corner
                        else:
                            new_r = r+x[0]
                            new_c = c+x[1]
                            another_piece = self.board.board[new_r][new_c]
                            if another_piece.get_color() == self.color_map[self.color]:
                                ai_score += 20 # award points for having pieces together (strength in unity)
                            elif another_piece.get_color() == self.color_map[self.opponent[self.color]]:
                                #detract points for walking into capture
                                if self.board.is_in_board(r-x[0], c-x[1]) and self.board.board[r-x[0]][c-x[1]].color == '.' and turn == self.opponent[self.color]:
                                    if another_piece.is_king:
                                        ai_score -= 1500
                                    else:
                                        if self.color == 1 and new_r > r:
                                            ai_score -= 1500
                                        elif self.color == 2 and new_r < r:
                                            ai_score -= 1500           
                elif piece.get_color() == self.color_map[self.opponent[self.color]]:
                    if piece.is_king:
                        opponent_score += 2000
                        # encourage king to take space in mid
                        opponent_score += ((self.row - 1) / 2 * 100) - (abs((self.row - 1)/ 2 - r) * 100)
                        opponent_score += ((self.col - 1) / 2 * 50) - (abs((self.col -1)/ 2 - c) * 50)
                    else:
                        opponent_score += 1000
                        # encourage normal pieces to move towards other end to become king
                        if self.opponent[self.color] != 1:
                            opponent_score += (self.row - r) / self.row * 1000
                        else:
                            opponent_score += (r+1) / self.row * 1000
                        
                    outside = 0
                    for x in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        if not(self.board.is_in_board(r + x[0], c + x[1])):
                            outside += 1
                            if outside == 2:
                                opponent_score += 100 # add points for being at edge
                            if outside == 3:
                                opponent_score -= 300 # subtract points for being at corner
                        else:
                            new_r = r+x[0]
                            new_c = c+x[1]
                            another_piece = self.board.board[new_r][new_c]
                            if another_piece.get_color() == self.color_map[self.opponent[self.color]]:
                                opponent_score += 20 # award points for having pieces together (strength in unity)
                            elif another_piece.get_color() == self.color_map[self.color]:
                                #detract points for walking into capture
                                if self.board.is_in_board(r-x[0], c-x[1]) and self.board.board[r-x[0]][c-x[1]].color == '.' and turn == self.color:
                                    if another_piece.is_king:
                                        opponent_score -= 1500
                                    else:
                                        if self.opponent[self.color] == 1 and new_r > r:
                                            opponent_score -= 1500
                                        elif self.opponent[self.color] == 2 and new_r < r:
                                            opponent_score -= 1500
        # award points for having more amount of pieces (strength in numbers)
        if self.color == 1:
            opponent_score  += self.board.white_count / (self.col * self.p / 2) * 1000 
            ai_score += self.board.black_count / (self.col * self.p / 2) * 1000
        else:
            ai_score += self.board.white_count / (self.col * self.p / 2) * 1000
            opponent_score += self.board.black_count / (self.col * self.p / 2) * 1000
        return ai_score - opponent_score + tie_breaker


if __name__ == "__main__":
    pass