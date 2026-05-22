"""
constants.py
Constantes y configuración global para el juego de Damas (Checkers).
"""

# =============================================
#  Dimensiones de la ventana y tablero
# =============================================
BOARD_SIZE = 8                 # 8x8
SQUARE_SIZE = 80               # Tamaño de cada casilla en píxeles
BOARD_PIXEL = BOARD_SIZE * SQUARE_SIZE  # 640px para el tablero
INFO_PANEL_WIDTH = 320         # Panel derecho de información
WINDOW_WIDTH = BOARD_PIXEL + INFO_PANEL_WIDTH  # 960
WINDOW_HEIGHT = BOARD_PIXEL    # 640
MENU_WIDTH = 700
MENU_HEIGHT = 550
FPS = 60

# =============================================
#  Piezas
# =============================================
EMPTY = 0
WHITE_PAWN = 1
BLACK_PAWN = 2
WHITE_KING = 3
BLACK_KING = 4

WHITE = 'white'
BLACK = 'black'

# =============================================
#  Colores (RGB)
# =============================================
# Tablero
COLOR_LIGHT_SQUARE = (240, 217, 181)    # Crema cálido
COLOR_DARK_SQUARE = (181, 136, 99)      # Madera oscura
COLOR_BOARD_BORDER = (101, 67, 33)      # Borde marrón oscuro

# Piezas
COLOR_WHITE_PIECE = (255, 248, 240)     # Blanco cálido
COLOR_WHITE_PIECE_EDGE = (200, 190, 175)
COLOR_WHITE_KING_CROWN = (255, 215, 0)  # Dorado
COLOR_BLACK_PIECE = (40, 40, 40)        # Negro suave
COLOR_BLACK_PIECE_EDGE = (80, 80, 80)
COLOR_BLACK_KING_CROWN = (255, 215, 0)

# UI
COLOR_BG = (30, 30, 35)                 # Fondo general
COLOR_PANEL_BG = (38, 40, 48)           # Panel de info
COLOR_PANEL_BORDER = (60, 65, 80)
COLOR_TEXT = (230, 230, 235)             # Texto principal
COLOR_TEXT_DIM = (150, 155, 165)         # Texto secundario
COLOR_TEXT_ACCENT = (100, 180, 255)      # Texto destacado (azul)
COLOR_HIGHLIGHT_SELECTED = (100, 200, 100, 150)  # Verde semi-transparente
COLOR_HIGHLIGHT_MOVE = (255, 255, 100, 120)       # Amarillo semi-transparente
COLOR_HIGHLIGHT_CAPTURE = (255, 80, 80, 120)      # Rojo semi-transparente
COLOR_HIGHLIGHT_LAST_MOVE = (180, 180, 255, 80)   # Azul semi-transparente
COLOR_BUTTON = (55, 60, 75)
COLOR_BUTTON_HOVER = (75, 80, 100)
COLOR_BUTTON_TEXT = (230, 230, 235)
COLOR_BUTTON_ACCENT = (70, 130, 220)
COLOR_BUTTON_ACCENT_HOVER = (90, 150, 240)

# Menú
COLOR_MENU_BG = (25, 27, 32)
COLOR_MENU_CARD = (38, 42, 55)
COLOR_MENU_TITLE = (255, 255, 255)

# =============================================
#  Modos de juego
# =============================================
MODE_HVH = 'human_vs_human'
MODE_HVAI = 'human_vs_ai'
MODE_AIVAI = 'ai_vs_ai'

# =============================================
#  Algoritmos de IA
# =============================================
AI_ALPHA_BETA = 'alpha_beta'
AI_MCTS = 'mcts'
AI_EXPECTIMAX = 'expectimax'

# Dificultad (profundidad para Alpha-Beta / Expectimax)
DIFFICULTY_EASY = 3
DIFFICULTY_MEDIUM = 5
DIFFICULTY_HARD = 7

# Límite de tiempo por jugada (segundos)
TIME_LIMIT = 2.0

# MCTS
MCTS_EXPLORATION_CONSTANT = 1.41  # sqrt(2)

# =============================================
#  Tablero inicial
# =============================================
def create_initial_board():
    """
    Crea el tablero inicial de damas.
    Negro (BLACK_PAWN=2) en filas 0-2 (arriba).
    Blanco (WHITE_PAWN=1) en filas 5-7 (abajo).
    Piezas solo en casillas oscuras (donde (row+col) % 2 == 1).
    """
    board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:  # Solo casillas oscuras
                if row < 3:
                    board[row][col] = BLACK_PAWN
                elif row > 4:
                    board[row][col] = WHITE_PAWN
    return board


# =============================================
#  Pesos heurísticos por fase
# =============================================
# Formato: (material, movilidad, centro, defensa_trasera, avance, capturas, bordes)
HEURISTIC_WEIGHTS = {
    'opening':  (5, 3, 4, 4, 2, 1, 2),
    'midgame':  (7, 4, 3, 2, 3, 2, 2),
    'endgame':  (10, 2, 1, 0, 6, 3, 1),
}

# Valor de las piezas
PIECE_VALUE_PAWN = 1
PIECE_VALUE_KING = 3

# Bonus posicional para casillas centrales
CENTER_SQUARES = {(3, 2), (3, 4), (4, 3), (4, 5),
                  (3, 6), (4, 1), (2, 3), (2, 5),
                  (5, 2), (5, 4)}
