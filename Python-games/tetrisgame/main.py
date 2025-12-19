import pygame
from pygame.locals import *
from copy import deepcopy
from random import choice, randrange

W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
SIDEBAR_WIDTH = 300
RES = GAME_RES[0] + SIDEBAR_WIDTH, GAME_RES[1]
FPS = 60

# --- Theme Configuration ---
THEME_STATE = "DARK"

def get_theme_colors(state):
    """Returns the current color palette based on the theme state."""
    if state == "DARK":
        return {
            'BG': pygame.Color('#1A1C2C'),
            'SIDEBAR': pygame.Color('#2C2E43'),
            'GRID_LINE': pygame.Color('#4F6D7A'),
            'TEXT': pygame.Color('#F0F7F4'),
            'NEON_PRIMARY': pygame.Color('#FF00FF'),
            'NEON_SECONDARY': pygame.Color('#00FFFF'),
            'TITLE_SHADOW': pygame.Color('#00FFFF'),
            'BUTTON_BG': pygame.Color('#FF00FF'),
        }
    else:
        return {
            'BG': pygame.Color('#E8E8E8'),
            'SIDEBAR': pygame.Color('#FFFFFF'),
            'GRID_LINE': pygame.Color('#A0A0A0'),
            'TEXT': pygame.Color('#1A1C2C'),
            'NEON_PRIMARY': pygame.Color('#A020F0'),
            'NEON_SECONDARY': pygame.Color('#008080'),
            'TITLE_SHADOW': pygame.Color('#333333'),
            'BUTTON_BG': pygame.Color('#008080'),
        }

COLORS = get_theme_colors(THEME_STATE)

pygame.init()
pygame.font.init()

title_font = pygame.font.SysFont('Arial Black', 72, bold=True)
subtitle_font = pygame.font.SysFont('Arial', 36, italic=True)
button_font = pygame.font.SysFont('Arial', 40, bold=True)
game_font = pygame.font.SysFont('Consolas', 24) 

sc = pygame.display.set_mode(RES)
pygame.display.set_caption("Cyber-TETRIS")
clock = pygame.time.Clock()

game_surface = pygame.Surface(GAME_RES)
game_surface.set_alpha(240) 

GAME_STATE = "START_SCREEN" 

score = 0
lines_cleared = 0

start_button_rect = pygame.Rect(0, 0, 280, 70)
start_button_rect.center = RES[0] // 2, RES[1] // 2 + 100 

EXIT_BUTTON_SIZE = 40
EXIT_RECT = pygame.Rect(RES[0] - EXIT_BUTTON_SIZE - 10, 10, EXIT_BUTTON_SIZE, EXIT_BUTTON_SIZE)

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

all_figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]

figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(W)] for j in range(H)]

anim_count = 0
side_anim_count, side_anim_limit = 0, 150
side_move_speed = 30
fall_speed_normal = 1000
fall_speed_fast = 50
anim_limit = fall_speed_normal

current_figure = deepcopy(choice(all_figures))
figure_color = choice([c for c in pygame.color.THECOLORS.keys() if c not in ('black', 'gray', 'darkgray', 'white')])


def check_borders():
    for block in current_figure:
        if block.x < 0 or block.x >= W:
            return False
        if block.y >= H:
            return False
        if block.y >= 0 and field[block.y][block.x] != 0:
            return False
    return True

def draw_exit_icon(surface):
    pygame.draw.rect(surface, COLORS['NEON_PRIMARY'], EXIT_RECT, border_radius=5)
    
    pad = 8
    x, y, w, h = EXIT_RECT
    
    pygame.draw.line(surface, COLORS['NEON_SECONDARY'], (x + pad, y + pad), (x + w - pad, y + h - pad), 3)
    pygame.draw.line(surface, COLORS['NEON_SECONDARY'], (x + w - pad, y + pad), (x + pad, y + h - pad), 3)


def draw_elements():
    global score, lines_cleared
    
    sc.fill(COLORS['BG'])

    sidebar_rect = pygame.Rect(GAME_RES[0], 0, SIDEBAR_WIDTH, RES[1])
    pygame.draw.rect(sc, COLORS['SIDEBAR'], sidebar_rect)
    pygame.draw.line(sc, COLORS['NEON_SECONDARY'], (GAME_RES[0], 0), (GAME_RES[0], RES[1]), 3) 

    game_surface.fill(COLORS['BG'])

    for y, row in enumerate(field):
        for x, color_key in enumerate(row):
            if color_key != 0:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_surface, color_key, figure_rect, border_radius=3)
                pygame.draw.rect(game_surface, pygame.Color('black'), figure_rect, 1, border_radius=3)

    [pygame.draw.rect(game_surface, COLORS['GRID_LINE'], i_rect, 1) for i_rect in grid]

    for i in range(4):
        figure_rect.x = current_figure[i].x * TILE
        figure_rect.y = current_figure[i].y * TILE
        pygame.draw.rect(game_surface, figure_color, figure_rect, border_radius=3)
        pygame.draw.rect(game_surface, COLORS['NEON_PRIMARY'], figure_rect, 2, border_radius=3) 

    sc.blit(game_surface, (0, 0))

    score_title = game_font.render("SCORE", True, COLORS['TEXT'])
    sc.blit(score_title, (GAME_RES[0] + 30, 50))
    
    score_value = title_font.render(str(score), True, COLORS['NEON_SECONDARY']) 
    sc.blit(score_value, (GAME_RES[0] + 30, 80))
    
    lines_title = game_font.render("LINES", True, COLORS['TEXT'])
    sc.blit(lines_title, (GAME_RES[0] + 30, 200))
    
    lines_value = title_font.render(str(lines_cleared), True, COLORS['NEON_PRIMARY']) 
    sc.blit(lines_value, (GAME_RES[0] + 30, 230))
    
    draw_exit_icon(sc)

    pygame.display.flip()

def draw_start_screen():
    sc.fill(COLORS['BG'])

    title_shadow = title_font.render("TETRIS", True, COLORS['TITLE_SHADOW'])
    title_text = title_font.render("TETRIS", True, COLORS['NEON_PRIMARY'])
    title_rect = title_text.get_rect(center=(RES[0] // 2, RES[1] // 2 - 100))
    
    sc.blit(title_shadow, (title_rect.x + 4, title_rect.y + 4))
    sc.blit(title_text, title_rect)

    subtitle_render = subtitle_font.render("CYBER EDITION", True, COLORS['TEXT'])
    subtitle_rect = subtitle_render.get_rect(center=(RES[0] // 2, RES[1] // 2 - 30))
    sc.blit(subtitle_render, subtitle_rect)

    button_color = COLORS['BUTTON_BG']
    pygame.draw.rect(sc, button_color, start_button_rect, border_radius=15)
    
    pygame.draw.rect(sc, COLORS['NEON_SECONDARY'], start_button_rect, 3, border_radius=15) 
    
    button_text = button_font.render("S T A R T", True, COLORS['TEXT'])
    button_text_rect = button_text.get_rect(center=start_button_rect.center)
    sc.blit(button_text, button_text_rect)
    
    draw_exit_icon(sc)

    pygame.display.flip()


# --- Main Game Loop ---
while True:
    timer = clock.tick(FPS)
    
    # NEW: Initialize movement/rotation flags BEFORE event handling
    dx = 0
    rotate = False 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                THEME_STATE = "LIGHT" if THEME_STATE == "DARK" else "DARK"
                COLORS = get_theme_colors(THEME_STATE)
            
            # FIX 1: Capture rotation and movement flags inside KEYDOWN event
            if GAME_STATE == "PLAYING":
                if event.key == pygame.K_UP:
                    rotate = True # Set flag to True only when key is pressed
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                if EXIT_RECT.collidepoint(event.pos):
                    exit()
                    
                if GAME_STATE == "START_SCREEN":
                    if start_button_rect.collidepoint(event.pos):
                        GAME_STATE = "PLAYING"
                        field = [[0 for _ in range(W)] for _ in range(H)]
                        score = 0
                        lines_cleared = 0
                        current_figure = deepcopy(choice(all_figures))
                        figure_color = choice([c for c in pygame.color.THECOLORS.keys() if c not in ('black', 'gray', 'darkgray', 'white')])

    if GAME_STATE == "START_SCREEN":
        draw_start_screen()

    elif GAME_STATE == "PLAYING":
        
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_DOWN]:
            anim_limit = fall_speed_fast
        else:
            anim_limit = fall_speed_normal

        # --- Continuous Horizontal Movement (ARR) ---
        if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_RIGHT]:
            side_anim_count += timer
            if key_pressed[pygame.K_LEFT]:
                side_move = -1
            else:
                side_move = 1
            if side_anim_count > side_anim_limit:
                if side_anim_count % side_move_speed < timer:
                    dx = side_move
        else:
            side_anim_count = 0

        figure_old = deepcopy(current_figure)
        
        # Apply horizontal movement (dx set by event or ARR)
        for i in range(4):
            current_figure[i].x += dx

        if not check_borders():
            current_figure = deepcopy(figure_old)

        # FIX 2: Rotation Execution Block (Execute immediately when flag is set)
        if rotate:
            center = current_figure[0]
            figure_old = deepcopy(current_figure)
            for i in range(4):
                x = current_figure[i].y - center.y
                y = current_figure[i].x - center.x
                current_figure[i].x = center.x - x
                current_figure[i].y = center.y + y
            if not check_borders():
                current_figure = deepcopy(figure_old)
        
        # --- Vertical Gravity Update ---
        anim_count += timer
        if anim_count > anim_limit:
            anim_count = 0
            figure_old = deepcopy(current_figure)
            for i in range(4):
                current_figure[i].y += 1

            if not check_borders():
                current_figure = deepcopy(figure_old)
                for i in range(4):
                    if figure_old[i].y < H:
                        field[figure_old[i].y][figure_old[i].x] = figure_color
                
                # Line clearing logic
                full_lines = []
                for y in range(H):
                    if all(field[y]):
                        full_lines.append(y)
                
                line_clear_count = len(full_lines)
                
                if line_clear_count > 0:
                    lines_cleared += line_clear_count
                    if line_clear_count == 1:
                        score += 100
                    elif line_clear_count == 2:
                        score += 300
                    elif line_clear_count == 3:
                        score += 500
                    elif line_clear_count == 4:
                        score += 800
                        
                    y = H - 1
                    while y >= 0:
                        if field[y] == [0 for _ in range(W)]:
                            break
                        if y in full_lines:
                            del field[y]
                            field.insert(0, [0 for _ in range(W)])
                        else:
                            y -= 1
                
                current_figure = deepcopy(choice(all_figures))
                figure_color = choice([c for c in pygame.color.THECOLORS.keys() if c not in ('black', 'gray', 'darkgray', 'white')])
                anim_limit = fall_speed_normal 

                if not check_borders():
                    GAME_STATE = "START_SCREEN"
                    print("Game Over!")

        draw_elements()