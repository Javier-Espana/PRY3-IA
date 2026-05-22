import copy
import time
import math
import random
from src.constants import *
from src.ai.minimax import get_ai_move_alpha_beta, minimax
from src.ai.mcts import get_ai_move_mcts
from src.ai.expectimax import get_ai_move_expectimax

class GameEngine:
    def __init__(self):
        self.board = create_initial_board()
        self.current_player = WHITE
        self.move_history = []
        self.move_count = 0
        self.nodes_explored = 0
        self.last_eval_score = 0
        self.game_over = False
        self.winner = None
        self.no_capture_count = 0

    def get_player_pieces(self, player):
        pieces = []
        target_pawn = WHITE_PAWN if player == WHITE else BLACK_PAWN
        target_king = WHITE_KING if player == WHITE else BLACK_KING
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] in (target_pawn, target_king):
                    pieces.append((r, c))
        return pieces

    def get_legal_moves(self, player=None):
        if player is None:
            player = self.current_player

        moves = {}
        all_captures = {}
        has_captures = False

        pieces = self.get_player_pieces(player)
        for r, c in pieces:
            captures = self._get_captures(r, c, self.board[r][c], self.board, set())
            if captures:
                all_captures[(r, c)] = captures
                has_captures = True

        if has_captures:
            return all_captures

        for r, c in pieces:
            simple_moves = self._get_simple_moves(r, c, self.board[r][c])
            if simple_moves:
                moves[(r, c)] = [[(r, c), move] for move in simple_moves]

        return moves

    def _get_simple_moves(self, row, col, piece):
        moves = []
        directions = []
        if piece in (WHITE_PAWN, WHITE_KING):
            directions.extend([(-1, -1), (-1, 1)])
        if piece in (BLACK_PAWN, BLACK_KING, WHITE_KING):
            if piece == BLACK_PAWN or piece == BLACK_KING:
                directions.extend([(1, -1), (1, 1)])
            elif piece == WHITE_KING:
                directions.extend([(1, -1), (1, 1)])

        directions = list(set(directions))

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if self.board[r][c] == EMPTY:
                    moves.append((r, c))
        return moves

    def _get_captures(self, row, col, piece, board, visited):
        captures = []
        directions = []
        if piece in (WHITE_PAWN, WHITE_KING):
            directions.extend([(-1, -1), (-1, 1)])
        if piece in (BLACK_PAWN, BLACK_KING):
            directions.extend([(1, -1), (1, 1)])
        if piece in (WHITE_KING, BLACK_KING):
            directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])
        
        directions = list(set(directions))
        
        target_pawn = BLACK_PAWN if piece in (WHITE_PAWN, WHITE_KING) else WHITE_PAWN
        target_king = BLACK_KING if piece in (WHITE_PAWN, WHITE_KING) else WHITE_KING

        for dr, dc in directions:
            mid_r, mid_c = row + dr, col + dc
            end_r, end_c = row + 2 * dr, col + 2 * dc

            if 0 <= end_r < BOARD_SIZE and 0 <= end_c < BOARD_SIZE:
                if board[mid_r][mid_c] in (target_pawn, target_king) and (mid_r, mid_c) not in visited:
                    if board[end_r][end_c] == EMPTY or (end_r == row and end_c == col):
                        temp_board = [r[:] for r in board]
                        temp_board[row][col] = EMPTY
                        temp_board[end_r][end_c] = piece
                        
                        new_visited = visited.copy()
                        new_visited.add((mid_r, mid_c))
                        
                        next_captures = self._get_captures(end_r, end_c, piece, temp_board, new_visited)
                        
                        if not next_captures:
                            captures.append([(row, col), (end_r, end_c)])
                        else:
                            for cap in next_captures:
                                captures.append([(row, col)] + cap[1:])

        return captures

    def make_move(self, path):
        start_r, start_c = path[0]
        end_r, end_c = path[-1]
        piece = self.board[start_r][start_c]
        
        captured = 0
        promoted = False
        
        if len(path) >= 2 and abs(path[0][0] - path[1][0]) == 2:
            for i in range(len(path) - 1):
                r1, c1 = path[i]
                r2, c2 = path[i+1]
                mid_r, mid_c = (r1 + r2) // 2, (c1 + c2) // 2
                self.board[mid_r][mid_c] = EMPTY
                captured += 1
                
        self.board[start_r][start_c] = EMPTY
        self.board[end_r][end_c] = piece
        
        if piece == WHITE_PAWN and end_r == 0:
            self.board[end_r][end_c] = WHITE_KING
            promoted = True
        elif piece == BLACK_PAWN and end_r == BOARD_SIZE - 1:
            self.board[end_r][end_c] = BLACK_KING
            promoted = True
            
        self.move_history.append({'player': self.current_player, 'path': path, 'captured': captured})
        self.move_count += 1
        
        if captured > 0:
            self.no_capture_count = 0
        else:
            self.no_capture_count += 1
            
        self.current_player = BLACK if self.current_player == WHITE else WHITE
        self.is_game_over()
        
        return {'captured': captured, 'promoted': promoted}

    def copy(self):
        new_engine = GameEngine()
        new_engine.board = [r[:] for r in self.board]
        new_engine.current_player = self.current_player
        new_engine.move_history = list(self.move_history)
        new_engine.move_count = self.move_count
        new_engine.no_capture_count = self.no_capture_count
        new_engine.game_over = self.game_over
        new_engine.winner = self.winner
        return new_engine

    def is_game_over(self):
        if self.game_over:
            return True
            
        if self.no_capture_count >= 40:
            self.game_over = True
            self.winner = None
            return True
            
        white_moves = self.get_legal_moves(WHITE)
        black_moves = self.get_legal_moves(BLACK)
        
        white_has_moves = len(white_moves) > 0
        black_has_moves = len(black_moves) > 0
        
        if not white_has_moves and not black_has_moves:
            self.game_over = True
            self.winner = None
        elif not white_has_moves:
            self.game_over = True
            self.winner = BLACK
        elif not black_has_moves:
            self.game_over = True
            self.winner = WHITE
            
        return self.game_over

    def get_winner(self):
        return self.winner

    def _get_game_phase(self):
        pieces = 0
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] != EMPTY:
                    pieces += 1
        if pieces > 20:
            return 'opening'
        elif pieces > 10:
            return 'midgame'
        else:
            return 'endgame'

    def evaluate(self, player=None):
        if player is None:
            player = self.current_player
            
        if self.game_over:
            if self.winner == player:
                return 1000000
            elif self.winner is None:
                return 0
            else:
                return -1000000
                
        phase = self._get_game_phase()
        w_mat, w_mob, w_cen, w_back, w_adv, w_cap, w_edge = HEURISTIC_WEIGHTS[phase]
        
        score = 0
        
        white_moves = self.get_legal_moves(WHITE)
        black_moves = self.get_legal_moves(BLACK)
        
        white_mob = sum(len(m) for m in white_moves.values())
        black_mob = sum(len(m) for m in black_moves.values())
        
        white_caps = sum(1 for m in white_moves.values() if m and len(m[0]) >= 2 and abs(m[0][0][0] - m[0][1][0]) == 2)
        black_caps = sum(1 for m in black_moves.values() if m and len(m[0]) >= 2 and abs(m[0][0][0] - m[0][1][0]) == 2)
        
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                p = self.board[r][c]
                if p == EMPTY:
                    continue
                    
                is_white = (p == WHITE_PAWN or p == WHITE_KING)
                is_king = (p == WHITE_KING or p == BLACK_KING)
                
                mat_val = PIECE_VALUE_KING if is_king else PIECE_VALUE_PAWN
                cen_val = 1 if (r, c) in CENTER_SQUARES else 0
                edge_val = 1 if c == 0 or c == BOARD_SIZE - 1 else 0
                
                back_val = 0
                if is_white and r == BOARD_SIZE - 1: back_val = 1
                elif not is_white and r == 0: back_val = 1
                
                adv_val = 0
                if not is_king:
                    if is_white: adv_val = (BOARD_SIZE - 1 - r)
                    else: adv_val = r
                    
                piece_score = (mat_val * w_mat + cen_val * w_cen + edge_val * w_edge + 
                               back_val * w_back + adv_val * w_adv)
                               
                if is_white:
                    score += piece_score
                else:
                    score -= piece_score
                    
        score += (white_mob * w_mob) - (black_mob * w_mob)
        score += (white_caps * w_cap) - (black_caps * w_cap)
        
        if player == BLACK:
            score = -score
            
        return score

    def get_ai_move(self, algorithm, depth=5, time_limit=None):
        if algorithm == AI_ALPHA_BETA:
            best_move, stats = get_ai_move_alpha_beta(self, depth)
            self.nodes_explored = stats.get('nodes', 0)
            self.last_eval_score = stats.get('eval', 0)
            return best_move, stats
        elif algorithm == AI_MCTS:
            best_move, stats = get_ai_move_mcts(self, time_limit)
            self.nodes_explored = stats.get('iterations', 0)
            self.last_eval_score = stats.get('eval', 0)
            return best_move, stats
        elif algorithm == AI_EXPECTIMAX:
            best_move, stats = get_ai_move_expectimax(self, depth)
            self.nodes_explored = stats.get('nodes', 0)
            self.last_eval_score = stats.get('eval', 0)
            return best_move, stats
        else:
            return get_ai_move_alpha_beta(self, depth)

    def run_minimax_pure(self, depth):
        # Wrapper for pure minimax search for combinatorial explosion testing
        stats = {'nodes': 0}
        score, move = minimax(self, depth, True, self.current_player, stats)
        return score, move, stats['nodes']

