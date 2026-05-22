import pygame
from src.constants import *

def draw_buttons_row(screen, mouse_pos, font_medium, font_small, label_text, buttons_info, current_val, y_offset, buttons_dict):
    label = font_medium.render(label_text, True, COLOR_TEXT_DIM)
    screen.blit(label, label.get_rect(centerx=WINDOW_WIDTH // 2, top=y_offset))
    
    y_offset += 40
    num_buttons = len(buttons_info)
    btn_width = 180
    spacing = 20
    total_width = (btn_width * num_buttons) + (spacing * (num_buttons - 1))
    start_x = (WINDOW_WIDTH - total_width) // 2
    
    for i, (text, val) in enumerate(buttons_info):
        rect = pygame.Rect(start_x + i * (btn_width + spacing), y_offset, btn_width, 40)
        
        is_selected = (val == current_val)
        is_hovered = rect.collidepoint(mouse_pos)
        
        if is_selected:
            bg_color = COLOR_BUTTON_ACCENT
        elif is_hovered:
            bg_color = COLOR_BUTTON_HOVER
        else:
            bg_color = COLOR_BUTTON
            
        pygame.draw.rect(screen, bg_color, rect, border_radius=8)
        
        btn_text = font_small.render(text, True, COLOR_BUTTON_TEXT)
        screen.blit(btn_text, btn_text.get_rect(center=rect.center))
        
        buttons_dict[val] = rect

def draw_menu(screen, menu_state, font_large, font_medium, font_small, buttons_dict):
    screen.fill(COLOR_MENU_BG)
    
    for i in range(0, WINDOW_WIDTH, 40):
        pygame.draw.line(screen, (30, 32, 38), (i, 0), (i, WINDOW_HEIGHT))
        
    card_rect = pygame.Rect((WINDOW_WIDTH - MENU_WIDTH) // 2, 
                            (WINDOW_HEIGHT - MENU_HEIGHT) // 2, 
                            MENU_WIDTH, MENU_HEIGHT)
    pygame.draw.rect(screen, COLOR_MENU_CARD, card_rect, border_radius=15)
    
    y_offset = card_rect.top + 30
    title = font_large.render("DAMAS - PROYECTO 3", True, COLOR_MENU_TITLE)
    screen.blit(title, title.get_rect(centerx=WINDOW_WIDTH // 2, top=y_offset))
    
    mouse_pos = pygame.mouse.get_pos()
    
    y_offset += 60
    draw_buttons_row(screen, mouse_pos, font_medium, font_small, "Modo de Juego", 
                     [("Humano vs Humano", MODE_HVH), 
                      ("Humano vs IA", MODE_HVAI), 
                      ("IA vs IA", MODE_AIVAI)], 
                     menu_state['mode'], y_offset, buttons_dict)
                     
    y_offset += 100
    if menu_state['mode'] in (MODE_HVAI, MODE_AIVAI):
        draw_buttons_row(screen, mouse_pos, font_medium, font_small, "Algoritmo IA", 
                         [("Alpha-Beta", AI_ALPHA_BETA), 
                          ("MCTS", AI_MCTS), 
                          ("Expectimax", AI_EXPECTIMAX)], 
                         menu_state['algorithm'], y_offset, buttons_dict)
                         
        y_offset += 100
        draw_buttons_row(screen, mouse_pos, font_medium, font_small, "Dificultad (Profundidad)", 
                         [("Fácil (3)", DIFFICULTY_EASY), 
                          ("Medio (5)", DIFFICULTY_MEDIUM), 
                          ("Difícil (7)", DIFFICULTY_HARD)], 
                         menu_state['difficulty'], y_offset, buttons_dict)
                         
    y_offset += 120
    # Play button
    play_rect = pygame.Rect(0, 0, 200, 50)
    play_rect.centerx = WINDOW_WIDTH // 2
    play_rect.top = y_offset
    
    color = COLOR_BUTTON_ACCENT_HOVER if play_rect.collidepoint(mouse_pos) else COLOR_BUTTON_ACCENT
    pygame.draw.rect(screen, color, play_rect, border_radius=10)
    
    play_text = font_medium.render("JUGAR", True, COLOR_BUTTON_TEXT)
    screen.blit(play_text, play_text.get_rect(center=play_rect.center))
    
    buttons_dict['play'] = play_rect

def handle_menu_click(pos, menu_state, buttons_dict):
    for val, rect in buttons_dict.items():
        if rect.collidepoint(pos):
            if val in (MODE_HVH, MODE_HVAI, MODE_AIVAI):
                menu_state['mode'] = val
            elif val in (AI_ALPHA_BETA, AI_MCTS, AI_EXPECTIMAX):
                menu_state['algorithm'] = val
            elif val in (DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_HARD):
                menu_state['difficulty'] = val
                
    if 'play' in buttons_dict and buttons_dict['play'].collidepoint(pos):
        if menu_state['mode'] is not None:
            return menu_state.copy()
            
    return None
