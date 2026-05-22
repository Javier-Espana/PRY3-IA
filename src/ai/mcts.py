import time
import math
import random
from src.constants import *

class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state  # GameEngine instance
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = self.state.get_legal_moves()  # dict
        # Flatten untried moves into a list
        self.untried_moves_list = []
        for start_pos, paths in self.untried_moves.items():
            for path in paths:
                self.untried_moves_list.append(path)

    def uct_select_child(self, c=MCTS_EXPLORATION_CONSTANT):
        best_score = -float('inf')
        best_child = None
        for child in self.children:
            if child.visits == 0:
                return child
            score = (child.wins / child.visits) + c * math.sqrt(math.log(self.visits) / child.visits)
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def expand(self):
        if not self.untried_moves_list:
            return None
        move = self.untried_moves_list.pop()
        new_state = self.state.copy()
        new_state.make_move(move)
        child_node = MCTSNode(new_state, parent=self, move=move)
        self.children.append(child_node)
        return child_node

    def update(self, result):
        self.visits += 1
        self.wins += result


def get_ai_move_mcts(engine, time_limit=None, C=MCTS_EXPLORATION_CONSTANT):
    if time_limit is None: 
        time_limit = TIME_LIMIT
        
    start_time = time.time()
    root = MCTSNode(engine.copy())
    
    iters = 0
    while True:
        if time_limit and time.time() - start_time > time_limit - 0.05: 
            break
        
        node = root
        # Selection
        while node.untried_moves_list == [] and node.children != []:
            node = node.uct_select_child(C)
            
        # Expansion
        if node.untried_moves_list:
            node = node.expand()
            
        # Simulation
        state = node.state.copy()
        while not state.is_game_over():
            moves_dict = state.get_legal_moves()
            if not moves_dict:
                break
            all_moves = []
            for paths in moves_dict.values():
                all_moves.extend(paths)
            
            # Semi-random policy: prefer captures
            captures = [m for m in all_moves if len(m) >= 2 and abs(m[0][0] - m[1][0]) == 2]
            if captures:
                move = random.choice(captures)
            else:
                move = random.choice(all_moves)
                
            state.make_move(move)
            
        # Backpropagation
        winner = state.get_winner()
        result = 0
        if winner == root.state.current_player:
            result = 1
        elif winner is None:
            result = 0.5
            
        while node is not None:
            node.update(result)
            result = 1 - result  # flip result for opponent
            node = node.parent
            
        iters += 1
        
    best_child = max(root.children, key=lambda c: c.visits) if root.children else None
    time_taken = time.time() - start_time
    best_move = best_child.move if best_child else None
    eval_score = best_child.wins / best_child.visits if best_child and best_child.visits > 0 else 0
    return best_move, {'iterations': iters, 'time': time_taken, 'eval': eval_score}
