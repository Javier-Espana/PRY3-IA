import pygame
import sys
import threading
from src.constants import *
from src.game_engine import GameEngine
from src.game_visualizer import GameVisualizer

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Damas - Proyecto 3 IA")
    clock = pygame.time.Clock()
    
    visualizer = GameVisualizer(screen)
    engine = None
    
    state = 'menu'
    game_mode = None
    ai_algorithm = None
    ai_difficulty = None
    
    ai_thinking = False
    ai_move_result = None
    ai_thread = None

    def ai_worker(engine_copy, algo, depth):
        nonlocal ai_move_result, ai_thinking
        move, stats = engine_copy.get_ai_move(algo, depth=depth)
        ai_move_result = (move, stats)
        ai_thinking = False

    while True:
        dt = clock.tick(FPS) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                
                if state == 'menu':
                    config = visualizer.handle_menu_click(pos)
                    if config:
                        game_mode = config['mode']
                        ai_algorithm = config['algorithm']
                        ai_difficulty = config['difficulty']
                        engine = GameEngine()
                        state = 'playing'
                        
                elif state == 'playing' and not visualizer.animating and not ai_thinking:
                    # Determine if it's a human turn
                    is_human_turn = False
                    if game_mode == MODE_HVH:
                        is_human_turn = True
                    elif game_mode == MODE_HVAI and engine.current_player == WHITE:
                        is_human_turn = True
                        
                    if is_human_turn:
                        board_pos = visualizer.get_board_pos(pos)
                        if board_pos:
                            r, c = board_pos
                            legal_moves = engine.get_legal_moves()
                            
                            # If a piece is already selected, try to move
                            if visualizer.selected_piece and visualizer.selected_piece in legal_moves:
                                moved = False
                                for path in legal_moves[visualizer.selected_piece]:
                                    if path[-1] == (r, c):
                                        visualizer.last_move = path
                                        visualizer.start_animation(path, engine.board[visualizer.selected_piece[0]][visualizer.selected_piece[1]])
                                        engine.make_move(path)
                                        visualizer.selected_piece = None
                                        visualizer.valid_moves = {}
                                        moved = True
                                        break
                                if moved:
                                    continue
                            
                            # Select piece
                            if (r, c) in legal_moves:
                                visualizer.selected_piece = (r, c)
                                visualizer.valid_moves = legal_moves
                            else:
                                visualizer.selected_piece = None
                                visualizer.valid_moves = {}
                                
                elif state == 'game_over':
                    state = 'menu'
                    engine = None
                    visualizer.ai_stats = {}
                    visualizer.last_move = None
        
        # Game logic updates
        if state == 'playing':
            if visualizer.animating:
                if visualizer.update_animation(dt):
                    # Animation finished, check game over
                    if engine.is_game_over():
                        state = 'game_over'
            else:
                if engine.is_game_over():
                    state = 'game_over'
                else:
                    is_ai_turn = False
                    if game_mode == MODE_HVAI and engine.current_player == BLACK:
                        is_ai_turn = True
                    elif game_mode == MODE_AIVAI:
                        is_ai_turn = True
                        
                    if is_ai_turn and not ai_thinking:
                        if ai_move_result:
                            # Apply the result from the thread
                            move, stats = ai_move_result
                            visualizer.ai_stats = stats
                            if move:
                                visualizer.last_move = move
                                visualizer.start_animation(move, engine.board[move[0][0]][move[0][1]])
                                engine.make_move(move)
                            else:
                                engine.game_over = True
                                engine.winner = WHITE if engine.current_player == BLACK else BLACK
                            ai_move_result = None
                        else:
                            # Start AI thinking thread
                            ai_thinking = True
                            engine_copy = engine.copy()
                            # For AI vs AI, we could alternate algorithms, but for simplicity use the selected one
                            ai_thread = threading.Thread(target=ai_worker, args=(engine_copy, ai_algorithm, ai_difficulty))
                            ai_thread.start()

        # Rendering
        if state == 'menu':
            visualizer.draw_menu()
        else:
            visualizer.draw_board(engine)
            visualizer.draw_highlights(engine)
            visualizer.draw_pieces(engine)
            if visualizer.animating:
                visualizer.draw_animation(engine)
            visualizer.draw_info_panel(engine, game_mode, ai_algorithm)
            
            if state == 'game_over':
                visualizer.draw_game_over(engine.get_winner())
                
            if ai_thinking:
                text = visualizer.font_medium.render("IA Pensando...", True, COLOR_TEXT_ACCENT)
                screen.blit(text, (BOARD_PIXEL // 2 - 80, 10))
                
        pygame.display.flip()

if __name__ == '__main__':
    main()
