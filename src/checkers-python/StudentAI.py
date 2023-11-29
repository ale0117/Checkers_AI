#MOST UPDATED & COMMENTED
from random import randint
from BoardClasses import Move
from BoardClasses import Board
from collections import deque
import math
#The following part should be completed by students.
#Students can modify anything except the class name and existing functions and variables.
class MCSTNode():
    def __init__(self, move):
        self.move = move
        self.children = []
        self.children_map = {}
        self.simulations = 0
        self.wins = 0

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
        #added
        self.max_depth = 3
        self.color_map = {2:'W', 1:'B'}
        
    #get_move function called from the gameloop in the main module.
    #@param move: A Move object describing the move.

    #update board with the opponents move, then make our move and return it.
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        #create a move and use mini_max_search to find the best next move
        moves = self.mini_max_search()
        chosen_move = self.best_mcst_move(moves)
        self.board.make_move(chosen_move, self.color)
        return chosen_move
    
    def best_mcst_move(self, moves):
        if len(moves) == 1:
            return moves[0]
        else:
            root_node = MCSTNode(None)
            for move in moves:
                temp_node = MCSTNode(move)
                root_node.children.append(temp_node)
                root_node.children_map[move] = temp_node
            for _ in range(25):
                self.mcts(root_node, self.color)
            highest_uct = float('-inf')
            index = 0
            for i, child in enumerate(root_node.children):
                if child.simulations != 0:
                    curr_uct = (child.wins / child.simulations) + math.sqrt(2) * math.sqrt(math.log(root_node.simulations) / child.simulations)
                    if curr_uct > highest_uct:
                        highest_uct = curr_uct
                        index = i
            chosen_move = root_node.children[index].move
            return chosen_move
    
    def mcts(self, node, turn):
        winner = self.board.is_win(turn)
        if winner != 0:
            return winner
        random_num = randint(1, 10)
        if random_num < 4 or len(node.children) == 0:
            if node.move == None:
                index = randint(0, len(node.children) - 1)
                chosen_move = node.children[index].move
                self.board.make_move(chosen_move, turn)
                winner = self.mcts(node.children[index], self.opponent[turn])
            else:
                moves = self.board.get_all_possible_moves(turn)
                if len(moves) == 0:
                    return self.opponent[turn]
                index = randint(0, len(moves)-1)
                inner_index = randint(0, len(moves[index])-1)
                move = moves[index][inner_index]
                self.board.make_move(move, turn)
                if move not in node.children_map:
                    temp_node = MCSTNode(move)
                    node.children.append(temp_node)
                    node.children_map[move] = temp_node
                winner = self.mcts(node.children_map[move], self.opponent[turn])
            node.simulations += 1
            if winner == turn:
                node.wins += 1
            self.board.undo()
            return winner
        else:
            highest_uct = float('-inf')
            index = 0
            for i, child in enumerate(node.children):
                if child.simulations != 0:
                    curr_uct = (child.wins / child.simulations) + math.sqrt(2) * math.sqrt(math.log(node.simulations) / child.simulations)
                    if curr_uct > highest_uct:
                        highest_uct = curr_uct
                        index = i
            chosen_move = node.children[index].move
            self.board.make_move(chosen_move, turn)
            winner = self.mcts(node.children[index], self.opponent[turn])
            node.simulations += 1
            if winner == turn:
                node.wins += 1
            self.board.undo()
            return winner

    #returns optimal move using minimax search
    def mini_max_search(self):
        res, best_move = self.max_val(0, float('-inf'), float('inf'))
        return best_move

    #recursion for max_val
    def max_val(self, curr_depth, alpha, beta):
        if curr_depth == self.max_depth:
            return self.board_score(self.color), None
        moves = self.board.get_all_possible_moves(self.color)
        if len(moves) == 0:
            return self.board_score(self.color), None
        res = float('-inf')
        best_move = [moves[0][0]]
        for move_seq in moves:
            for move in move_seq:
                self.board.make_move(move, self.color)
                score = self.min_val(curr_depth + 1, alpha, beta)[0]
                if score >= res:
                    res = score
                    best_move = [move]
                if score == res:
                    best_move.append(move)
                alpha = max(alpha, res)
                if alpha >= beta:
                    self.board.undo()
                    return res, best_move
                self.board.undo()
        return res, best_move

    #recursion for min_val
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

    #determines score of the current state of the board
    #called by max_val and min_val
    def board_score(self, turn):
        ai_score = 0
        opponent_score = 0
        #loop through every piece on the board and award points
        for r in range(self.row):
            for c in range(self.col):
                piece = self.board.board[r][c]
                #if our AI's piece...
                if piece.get_color() == self.color_map[self.color]:
                    if piece.is_king:
                        ai_score += 2000
                        #ai_score += ((self.row - 1) / 2 * 100) - (abs((self.row - 1)/ 2 - r) * 100)
                        #ai_score += ((self.col - 1) / 2 * 50) - (abs((self.col -1)/ 2 - c) * 50)
                        #encourage king pieces to go towards enemy pieces
                        if turn == self.opponent[self.color]:
                            closest_enemy_piece = None
                            queue = deque([(r-1, c-1, 1), (r+1, c-1, 1), (r-1, c+1, 1), (r+1, c+1, 1)])
                            checked = {(r, c), (r-1, c-1), (r+1, c-1), (r-1, c+1), (r+1, c+1)}
                            while closest_enemy_piece == None and queue:
                                coords = queue.popleft()
                                if self.board.is_in_board(coords[0], coords[1]):
                                    if self.board.board[coords[0]][coords[1]].get_color() == self.color_map[self.opponent[self.color]]:
                                        closest_enemy_piece = coords
                                    for m in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                                        if (coords[0]+m[0], coords[1]+m[1]) not in checked:
                                            queue.append((coords[0]+m[0], coords[1]+m[1], coords[2]+1))
                                            checked.add((coords[0]+m[0], coords[1]+m[1]))
                            if closest_enemy_piece:
                                ai_score += max(self.row-1, self.col-1) * 100 - closest_enemy_piece[2] * 100
                    else:
                        ai_score += 1000
                        #for a normal piece, encourage moving pieces already closer to opponent side (closer to becoming a king)
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
                #if the opponent's piece...
                elif piece.get_color() == self.color_map[self.opponent[self.color]]:
                    if piece.is_king:
                        opponent_score += 2000
                        #opponent_score += ((self.row - 1) / 2 * 100) - (abs((self.row - 1)/ 2 - r) * 100)
                        #opponent_score += ((self.col - 1) / 2 * 50) - (abs((self.col -1)/ 2 - c) * 50)
                        #encourage king pieces to go towards enemy pieces
                        if turn == self.color:
                            closest_enemy_piece = None
                            queue = deque([(r-1, c-1, 1), (r+1, c-1, 1), (r-1, c+1, 1), (r+1, c+1, 1)])
                            checked = {(r, c), (r-1, c-1), (r+1, c-1), (r-1, c+1), (r+1, c+1)}
                            while closest_enemy_piece == None and queue:
                                coords = queue.popleft()
                                if self.board.is_in_board(coords[0], coords[1]):
                                    if self.board.board[coords[0]][coords[1]].get_color() == self.color_map[self.color]:
                                        closest_enemy_piece = coords
                                    for m in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                                        if (coords[0]+m[0], coords[1]+m[1]) not in checked:
                                            queue.append((coords[0]+m[0], coords[1]+m[1], coords[2]+1))
                                            checked.add((coords[0]+m[0], coords[1]+m[1]))
                            if closest_enemy_piece:
                                opponent_score += max(self.row-1, self.col-1) * 100 - closest_enemy_piece[2] * 100
                    else:
                        opponent_score += 1000
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
        return ai_score - opponent_score


if __name__ == "__main__":
    pass