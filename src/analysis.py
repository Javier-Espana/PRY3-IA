import time
import math
import random
import matplotlib.pyplot as plt
import numpy as np
from src.constants import *
from src.game_engine import GameEngine

def run_combinatorial_analysis():
    print("Iniciando análisis de explosión combinatoria...")
    depths = list(range(1, 5)) # pure minimax is slow beyond depth 4
    minimax_nodes = []
    ab_nodes = []
    
    # Calculate averages over a few initial positions or a single start position
    for d in depths:
        print(f"Probando profundidad {d}...")
        # Minimax Puro
        engine = GameEngine()
        _, _, nodes_m = engine.run_minimax_pure(d)
        minimax_nodes.append(nodes_m)
        
        # Alpha-Beta
        engine = GameEngine()
        _, stats = engine.get_ai_move(AI_ALPHA_BETA, depth=d)
        nodes_ab = stats['nodes']
        ab_nodes.append(nodes_ab)
        
    print("Calculando factor de ramificación efectivo...")
    # beff = nodes ^ (1/depth)
    beff_m = [nodes ** (1/d) if nodes > 0 else 0 for d, nodes in zip(depths, minimax_nodes)]
    beff_ab = [nodes ** (1/d) if nodes > 0 else 0 for d, nodes in zip(depths, ab_nodes)]
    
    # Plotting
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Nodes comparison
    ax1.plot(depths, minimax_nodes, marker='o', color='red', label='Minimax Puro')
    ax1.plot(depths, ab_nodes, marker='s', color='cyan', label='Alpha-Beta')
    ax1.set_yscale('log')
    ax1.set_xlabel('Profundidad')
    ax1.set_ylabel('Nodos Explorados (Escala Logarítmica)')
    ax1.set_title('Explosión Combinatoria: Nodos Visitados')
    ax1.grid(True, which="both", ls="--", color='gray', alpha=0.5)
    ax1.legend()
    
    # Branching factor
    ax2.plot(depths, beff_m, marker='o', color='red', label='Minimax Puro')
    ax2.plot(depths, beff_ab, marker='s', color='cyan', label='Alpha-Beta')
    ax2.set_xlabel('Profundidad')
    ax2.set_ylabel('Factor de Ramificación Efectivo (b_eff)')
    ax2.set_title('Factor de Ramificación Efectivo por Profundidad')
    ax2.grid(True, ls="--", color='gray', alpha=0.5)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('combinatorial_analysis.png')
    print("Gráfica guardada como combinatorial_analysis.png")
    plt.close()

def run_tournament():
    print("Iniciando torneo IA vs IA (20 partidas)...")
    wins_ab = 0
    wins_mcts = 0
    draws = 0
    
    ab_times = []
    mcts_times = []
    
    # 20 games
    num_games = 20
    for game in range(num_games):
        engine = GameEngine()
        # Alternate who plays White
        ab_plays_white = (game % 2 == 0)
        
        print(f"Partida {game + 1}/{num_games} (AB es {'Blancas' if ab_plays_white else 'Negras'})")
        
        move_limit = 100
        moves = 0
        while not engine.is_game_over() and moves < move_limit:
            current = engine.current_player
            
            # Determine current player's algorithm
            if (current == WHITE and ab_plays_white) or (current == BLACK and not ab_plays_white):
                # Alpha-Beta turn
                start = time.time()
                move, stats = engine.get_ai_move(AI_ALPHA_BETA, depth=5)
                duration = time.time() - start
                ab_times.append(duration)
            else:
                # MCTS turn
                start = time.time()
                move, stats = engine.get_ai_move(AI_MCTS, time_limit=2.0)
                duration = time.time() - start
                mcts_times.append(duration)
                
            if move:
                engine.make_move(move)
            else:
                break
            moves += 1
            
        winner = engine.get_winner()
        if winner == WHITE:
            if ab_plays_white:
                wins_ab += 1
                print("Ganador: Alpha-Beta (Blancas)")
            else:
                wins_mcts += 1
                print("Ganador: MCTS (Blancas)")
        elif winner == BLACK:
            if not ab_plays_white:
                wins_ab += 1
                print("Ganador: Alpha-Beta (Negras)")
            else:
                wins_mcts += 1
                print("Ganador: MCTS (Negras)")
        else:
            draws += 1
            print("Resultado: Empate")
            
    print("\n--- Resultados del Torneo ---")
    print(f"Alpha-Beta victorias: {wins_ab}")
    print(f"MCTS victorias: {wins_mcts}")
    print(f"Empates: {draws}")
    print(f"Tiempo promedio AB por jugada: {np.mean(ab_times):.4f}s")
    print(f"Tiempo promedio MCTS por jugada: {np.mean(mcts_times):.4f}s")
    
    # Plotting
    plt.style.use('dark_background')
    labels = ['Alpha-Beta', 'MCTS', 'Empates']
    results = [wins_ab, wins_mcts, draws]
    colors = ['cyan', 'orange', 'gray']
    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(labels, results, color=colors, edgecolor='white')
    plt.ylabel('Cantidad de Partidas')
    plt.title('Duelo de Algoritmos (Torneo de 20 Partidas)')
    
    # Add values on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.3, str(yval), ha='center', va='bottom', fontsize=12)
        
    plt.tight_layout()
    plt.savefig('tournament_results.png')
    print("Gráfica guardada como tournament_results.png")
    plt.close()

if __name__ == '__main__':
    run_combinatorial_analysis()
    run_tournament()
