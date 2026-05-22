import time
from src.constants import *

def alpha_beta(engine, depth, alpha, beta, maximizing_player, player, start_time=None, stats=None):
    if stats is not None:
        stats['nodes'] += 1
    
    if start_time and time.time() - start_time > TIME_LIMIT - 0.05:
        return engine.evaluate(player), None

    if depth == 0 or engine.is_game_over():
        return engine.evaluate(player), None

    moves_dict = engine.get_legal_moves(engine.current_player)
    all_moves = []
    for paths in moves_dict.values():
        all_moves.extend(paths)

    # Move ordering: captures first
    all_moves.sort(key=lambda m: len(m), reverse=True)

    best_move = None
    if maximizing_player:
        max_eval = -float('inf')
        for move in all_moves:
            engine_copy = engine.copy()
            engine_copy.make_move(move)
            eval_score, _ = alpha_beta(engine_copy, depth - 1, alpha, beta, False, player, start_time, stats)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in all_moves:
            engine_copy = engine.copy()
            engine_copy.make_move(move)
            eval_score, _ = alpha_beta(engine_copy, depth - 1, alpha, beta, True, player, start_time, stats)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def get_ai_move_alpha_beta(engine, depth=5):
    start_time = time.time()
    stats = {'nodes': 0}
    best_move = None
    best_score = 0
    d = 1
    
    # Iterative deepening
    for d in range(1, depth + 1):
        if time.time() - start_time > TIME_LIMIT - 0.05:
            break
        score, move = alpha_beta(engine, d, -float('inf'), float('inf'), True, engine.current_player, start_time, stats)
        if move is not None:
            best_move = move
            best_score = score
            
    time_taken = time.time() - start_time
    return best_move, {'nodes': stats['nodes'], 'time': time_taken, 'depth_reached': d, 'eval': best_score}

def minimax(engine, depth, maximizing_player, player, stats=None):
    if stats is not None:
        stats['nodes'] += 1

    if depth == 0 or engine.is_game_over():
        return engine.evaluate(player), None

    moves_dict = engine.get_legal_moves(engine.current_player)
    all_moves = []
    for paths in moves_dict.values():
        all_moves.extend(paths)

    best_move = None
    if maximizing_player:
        max_eval = -float('inf')
        for move in all_moves:
            engine_copy = engine.copy()
            engine_copy.make_move(move)
            eval_score, _ = minimax(engine_copy, depth - 1, False, player, stats)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in all_moves:
            engine_copy = engine.copy()
            engine_copy.make_move(move)
            eval_score, _ = minimax(engine_copy, depth - 1, True, player, stats)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move

