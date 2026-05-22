import pygame
from src.constants import *

def draw_info_panel(screen, engine, game_mode, ai_algorithm, ai_stats, font_large, font_medium, font_small, font_tiny):
    panel_rect = pygame.Rect(BOARD_PIXEL, 0, INFO_PANEL_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(screen, COLOR_PANEL_BG, panel_rect)
    pygame.draw.line(screen, COLOR_PANEL_BORDER, (BOARD_PIXEL, 0), (BOARD_PIXEL, WINDOW_HEIGHT), 2)
    
    y_offset = 20
    x_offset = BOARD_PIXEL + 20
    
    # Title
    title = font_large.render("DAMAS", True, COLOR_TEXT)
    screen.blit(title, (x_offset, y_offset))
    y_offset += 50
    
    # Turn indicator
    turn_text = font_medium.render("Turno Actual:", True, COLOR_TEXT_DIM)
    screen.blit(turn_text, (x_offset, y_offset))
    
    turn_color = COLOR_WHITE_PIECE if engine.current_player == WHITE else COLOR_BLACK_PIECE
    turn_edge = COLOR_WHITE_PIECE_EDGE if engine.current_player == WHITE else COLOR_BLACK_PIECE_EDGE
    circle_x = x_offset + 180
    circle_y = y_offset + 15
    pygame.draw.circle(screen, turn_edge, (int(circle_x), int(circle_y + 2)), 15)
    pygame.draw.circle(screen, turn_color, (int(circle_x), int(circle_y)), 15)
    
    y_offset += 40
    
    # Game Mode
    mode_str = "Humano vs Humano"
    if game_mode == MODE_HVH: mode_str = "Humano vs Humano"
    elif game_mode == MODE_HVAI: mode_str = "Humano vs IA"
    elif game_mode == MODE_AIVAI: mode_str = "IA vs IA"
    
    mode_text = font_small.render(f"Modo: {mode_str}", True, COLOR_TEXT)
    screen.blit(mode_text, (x_offset, y_offset))
    y_offset += 25
    
    if game_mode in (MODE_HVAI, MODE_AIVAI):
        algo_str = "Alpha-Beta" if ai_algorithm == AI_ALPHA_BETA else ("MCTS" if ai_algorithm == AI_MCTS else "Expectimax")
        algo_text = font_small.render(f"Algoritmo: {algo_str}", True, COLOR_TEXT_ACCENT)
        screen.blit(algo_text, (x_offset, y_offset))
    y_offset += 30
    
    pygame.draw.line(screen, COLOR_PANEL_BORDER, (x_offset, y_offset), (WINDOW_WIDTH - 20, y_offset))
    y_offset += 20
    
    # AI Stats
    stats_title = font_medium.render("Rendimiento IA:", True, COLOR_TEXT)
    screen.blit(stats_title, (x_offset, y_offset))
    y_offset += 30
    
    nodes = ai_stats.get('nodes', engine.nodes_explored)
    time_ms = ai_stats.get('time', 0) * 1000
    depth = ai_stats.get('depth_reached', ai_stats.get('iterations', 0))
    eval_score = ai_stats.get('eval', engine.last_eval_score)
    
    stats = [
        f"Nodos/Iters: {nodes}",
        f"Profundidad: {depth}",
        f"Tiempo: {time_ms:.0f} ms",
        f"Evaluación: {eval_score:.2f}"
    ]
    
    for stat in stats:
        stat_text = font_small.render(stat, True, COLOR_TEXT_DIM)
        screen.blit(stat_text, (x_offset, y_offset))
        y_offset += 25
        
    y_offset += 10
    pygame.draw.line(screen, COLOR_PANEL_BORDER, (x_offset, y_offset), (WINDOW_WIDTH - 20, y_offset))
    y_offset += 20
    
    # Pieces count
    w_pieces = len(engine.get_player_pieces(WHITE))
    b_pieces = len(engine.get_player_pieces(BLACK))
    
    pcount_text = font_small.render(f"Piezas: Blancas {w_pieces} | Negras {b_pieces}", True, COLOR_TEXT)
    screen.blit(pcount_text, (x_offset, y_offset))
    y_offset += 25
    
    moves_text = font_small.render(f"Movimiento: {engine.move_count}", True, COLOR_TEXT)
    screen.blit(moves_text, (x_offset, y_offset))
    y_offset += 30
    
    pygame.draw.line(screen, COLOR_PANEL_BORDER, (x_offset, y_offset), (WINDOW_WIDTH - 20, y_offset))
    y_offset += 20
    
    # History
    hist_title = font_medium.render("Últimos Movimientos:", True, COLOR_TEXT)
    screen.blit(hist_title, (x_offset, y_offset))
    y_offset += 30
    
    recent_moves = engine.move_history[-5:]
    for m in recent_moves:
        p_str = "B" if m['player'] == WHITE else "N"
        path = m['path']
        s_str = f"{chr(path[0][1] + ord('a'))}{BOARD_SIZE - path[0][0]}"
        e_str = f"{chr(path[-1][1] + ord('a'))}{BOARD_SIZE - path[-1][0]}"
        cap_str = f"(x{m['captured']})" if m['captured'] > 0 else ""
        hist_text = font_small.render(f"{p_str}: {s_str} -> {e_str} {cap_str}", True, COLOR_TEXT_DIM)
        screen.blit(hist_text, (x_offset, y_offset))
        y_offset += 25
