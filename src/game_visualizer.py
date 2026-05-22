import pygame
from src.constants import *
from src.gui.board import draw_board, draw_pieces, draw_highlights, draw_single_piece
from src.gui.menu import draw_menu, handle_menu_click
from src.gui.panel import draw_info_panel

class GameVisualizer:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.SysFont('Arial', 36, bold=True)
        self.font_medium = pygame.font.SysFont('Arial', 24)
        self.font_small = pygame.font.SysFont('Arial', 18)
        self.font_tiny = pygame.font.SysFont('Arial', 14)
        
        self.animating = False
        self.anim_piece = None
        self.anim_start = None
        self.anim_end = None
        self.anim_progress = 0.0
        self.anim_speed = 5.0
        self.anim_path = []
        self.anim_path_idx = 0
        
        self.selected_piece = None
        self.valid_moves = {}
        self.last_move = None
        self.ai_stats = {}
        
        self.menu_state = {
            'mode': None,
            'algorithm': AI_ALPHA_BETA,
            'difficulty': DIFFICULTY_MEDIUM,
            'show_ai_options': False
        }
        self.menu_buttons = {}

    def draw_board(self, engine):
        draw_board(self.screen, engine, self.font_tiny)

    def draw_pieces(self, engine):
        draw_pieces(self.screen, engine, self.font_small, self.animating, self.anim_start)

    def draw_highlights(self, engine):
        draw_highlights(self.screen, self.last_move, self.selected_piece, self.valid_moves)

    def draw_info_panel(self, engine, game_mode, ai_algorithm):
        draw_info_panel(self.screen, engine, game_mode, ai_algorithm, self.ai_stats,
                        self.font_large, self.font_medium, self.font_small, self.font_tiny)

    def draw_game_over(self, winner):
        surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surface, (0, 0, 0, 180), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        
        if winner == WHITE:
            text_str = "¡BLANCAS GANAN!"
            color = COLOR_WHITE_PIECE
        elif winner == BLACK:
            text_str = "¡NEGRAS GANAN!"
            color = COLOR_TEXT_ACCENT
        else:
            text_str = "¡EMPATE!"
            color = COLOR_TEXT
            
        text = self.font_large.render(text_str, True, color)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        surface.blit(text, text_rect)
        
        sub = self.font_medium.render("Click en la pantalla para volver al menú", True, COLOR_TEXT_DIM)
        sub_rect = sub.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
        surface.blit(sub, sub_rect)
        
        self.screen.blit(surface, (0, 0))

    def draw_menu(self):
        draw_menu(self.screen, self.menu_state, self.font_large, self.font_medium, self.font_small, self.menu_buttons)

    def handle_menu_click(self, pos):
        return handle_menu_click(pos, self.menu_state, self.menu_buttons)

    def get_board_pos(self, mouse_pos):
        x, y = mouse_pos
        if x < BOARD_PIXEL and y < BOARD_PIXEL:
            return y // SQUARE_SIZE, x // SQUARE_SIZE
        return None

    def start_animation(self, move, piece):
        self.animating = True
        self.anim_piece = piece
        self.anim_path = move
        self.anim_path_idx = 0
        self.anim_start = move[0]
        self.anim_end = move[1]
        self.anim_progress = 0.0

    def update_animation(self, dt):
        if not self.animating:
            return True
            
        self.anim_progress += dt * self.anim_speed
        
        if self.anim_progress >= 1.0:
            self.anim_path_idx += 1
            if self.anim_path_idx >= len(self.anim_path) - 1:
                self.animating = False
                return True
            else:
                self.anim_start = self.anim_path[self.anim_path_idx]
                self.anim_end = self.anim_path[self.anim_path_idx + 1]
                self.anim_progress = 0.0
                
        return False

    def draw_animation(self, engine):
        if not self.animating:
            return
            
        start_x = self.anim_start[1] * SQUARE_SIZE + SQUARE_SIZE // 2
        start_y = self.anim_start[0] * SQUARE_SIZE + SQUARE_SIZE // 2
        
        end_x = self.anim_end[1] * SQUARE_SIZE + SQUARE_SIZE // 2
        end_y = self.anim_end[0] * SQUARE_SIZE + SQUARE_SIZE // 2
        
        # Interpolate
        curr_x = start_x + (end_x - start_x) * self.anim_progress
        curr_y = start_y + (end_y - start_y) * self.anim_progress
        
        draw_single_piece(self.screen, curr_x, curr_y, self.anim_piece, self.font_small)
