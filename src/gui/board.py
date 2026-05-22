import pygame
from src.constants import *

def draw_board(screen, engine, font_tiny):
    screen.fill(COLOR_BG)
    # Draw board background
    pygame.draw.rect(screen, COLOR_BOARD_BORDER, (0, 0, BOARD_PIXEL, BOARD_PIXEL))
                     
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            color = COLOR_DARK_SQUARE if (row + col) % 2 == 1 else COLOR_LIGHT_SQUARE
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            
            # Coordinate labels
            if col == 0:
                text = font_tiny.render(str(BOARD_SIZE - row), True, COLOR_BOARD_BORDER)
                screen.blit(text, (x + 2, y + 2))
            if row == BOARD_SIZE - 1:
                text = font_tiny.render(chr(ord('a') + col), True, COLOR_BOARD_BORDER)
                screen.blit(text, (x + SQUARE_SIZE - 12, y + SQUARE_SIZE - 18))

def draw_single_piece(screen, x, y, piece, font_small):
    is_white = piece in (WHITE_PAWN, WHITE_KING)
    is_king = piece in (WHITE_KING, BLACK_KING)
    
    color = COLOR_WHITE_PIECE if is_white else COLOR_BLACK_PIECE
    edge_color = COLOR_WHITE_PIECE_EDGE if is_white else COLOR_BLACK_PIECE_EDGE
    
    # Draw main piece with edge
    pygame.draw.circle(screen, edge_color, (int(x), int(y + 2)), SQUARE_SIZE // 2 - 8)
    pygame.draw.circle(screen, color, (int(x), int(y)), SQUARE_SIZE // 2 - 8)
    
    # Draw concentric circle for depth
    pygame.draw.circle(screen, edge_color, (int(x), int(y)), SQUARE_SIZE // 2 - 14, 2)
    
    if is_king:
        crown_color = COLOR_WHITE_KING_CROWN if is_white else COLOR_BLACK_KING_CROWN
        pygame.draw.circle(screen, crown_color, (int(x), int(y)), SQUARE_SIZE // 4)
        text = font_small.render("K", True, color)
        text_rect = text.get_rect(center=(int(x), int(y)))
        screen.blit(text, text_rect)

def draw_pieces(screen, engine, font_small, animating, anim_start):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if animating and (row, col) == anim_start:
                continue
                
            piece = engine.board[row][col]
            if piece != EMPTY:
                x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                draw_single_piece(screen, x, y, piece, font_small)

def draw_highlights(screen, last_move, selected_piece, valid_moves):
    surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    
    if last_move:
        start_r, start_c = last_move[0]
        end_r, end_c = last_move[-1]
        pygame.draw.rect(surface, COLOR_HIGHLIGHT_LAST_MOVE, 
                         (start_c * SQUARE_SIZE, start_r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(surface, COLOR_HIGHLIGHT_LAST_MOVE, 
                         (end_c * SQUARE_SIZE, end_r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                         
    if selected_piece:
        r, c = selected_piece
        pygame.draw.rect(surface, COLOR_HIGHLIGHT_SELECTED, 
                         (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                         
        if selected_piece in valid_moves:
            for path in valid_moves[selected_piece]:
                end_r, end_c = path[-1]
                is_cap = len(path) >= 2 and abs(path[0][0] - path[1][0]) == 2
                color = COLOR_HIGHLIGHT_CAPTURE if is_cap else COLOR_HIGHLIGHT_MOVE
                pygame.draw.rect(surface, color, (end_c * SQUARE_SIZE, end_r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                                 
    screen.blit(surface, (0, 0))
