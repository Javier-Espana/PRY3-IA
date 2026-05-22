import time
from src.constants import *

def expectimax(engine, depth, maximizing_player, player, start_time=None, stats=None):
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

    best_move = None
    if maximizing_player:
        max_eval = -float('inf')
        for move in all_moves:
            engine_copy = engine.copy()
            engine_copy.make_move(move)
            eval_score, _ = expectimax(engine_copy, depth - 1, False, player, start_time, stats)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        # Chance node - opponent moves randomly
        expected_eval = 0
        for move in all_moves:
            engine_copy = engine.copy()
            engine_copy.make_move(move)
            eval_score, _ = expectimax(engine_copy, depth - 1, True, player, start_time, stats)
            expected_eval += eval_score
        if len(all_moves) > 0:
            expected_eval /= len(all_moves)
        return expected_eval, all_moves[0] if all_moves else None

def get_ai_move_expectimax(engine, depth=4):
    start_time = time.time()
    stats = {'nodes': 0}
    best_move = None
    best_score = 0
    d = 1
    
    for d in range(1, depth + 1):
        if time.time() - start_time > TIME_LIMIT - 0.05:
            break
        score, move = expectimax(engine, d, True, engine.current_player, start_time, stats)
        if move is not None:
            best_move = move
            best_score = score
            
    time_taken = time.time() - start_time
    return best_move, {'nodes': stats['nodes'], 'time': time_taken, 'depth_reached': d, 'eval': best_score}
