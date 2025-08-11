import pygame
import random
pygame.init()
screen=pygame.display.set_mode((800,600))

pygame.display.set_caption('Trash collector')
icon=pygame.image.load('battery.png')
pygame.display.set_icon(icon)

pygame.mixer.music.load('asthetic-music.mp3')
pygame.mixer.music.play(-1)
background_img = pygame.image.load('eco-friendly.jpeg')
background_img = pygame.transform.scale(background_img, (800, 600))  # Match this to your screen size
trash_img = pygame.image.load('trash2.png')
trashX=random.randint(50,750)
trashY=0
trashX_change=0
trashY_change=0

dustbin_img = pygame.image.load('waste.png')
dustbinX=100
dustbinY=500
font = pygame.font.Font(None, 36)
large_font=pygame.font.Font(None, 64)

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 64)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Create multiple trash objects
num_trash = 5
trash_list = []
for _ in range(num_trash):
    trash_list.append({
        "x": random.randint(50, 750),
        "y": 0,
        "held": False
    })
# Score
score=0
# Negative Score
missed=0
game_over=False
game_started=False

def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    label = font.render(text, True, BLACK)
    screen.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))
    return pygame.Rect(x, y, w, h)

def trashFunc(x,y):
    screen.blit(trash_img, (x,y))
    
def dustbinFunc(x,y):
    screen.blit(dustbin_img, (x,y))
def show_score():
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
def show_negative_score():
    negative_score_text=font.render(f'Missed: {missed}', True, (0,0,0))
    screen.blit(negative_score_text, (600,10))
def show_game_over():
    screen.blit(background_img, (0,0))
    over_text = big_font.render("Game Over", True, BLACK)
    screen.blit(over_text, (250, 200))
    restart_btn = draw_button("Restart", 270, 300, 120, 50, GRAY)
    quit_btn = draw_button("Quit", 420, 300, 120, 50, GRAY)
    pygame.display.update()
    return restart_btn, quit_btn
running =True
holding_trash = False
while running:
    
    if game_over:
        restart_button, quit_button = show_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(pygame.mouse.get_pos()):
                    # Reset game state
                    score = 0
                    missed = 0
                    for trash in trash_list:
                        trash["x"] = random.randint(50, 750)
                        trash["y"] = 0
                        trash["held"] = False
                    game_over = False
                elif quit_button.collidepoint(pygame.mouse.get_pos()):
                    running = False
        continue

    screen.blit(background_img, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for trash in trash_list:
                trash_rect = pygame.Rect(trash["x"], trash["y"], trash_img.get_width(), trash_img.get_height())
                if trash_rect.collidepoint(mouse_x, mouse_y):
                    trash["held"] = True

        elif event.type == pygame.MOUSEBUTTONUP:
            for trash in trash_list:
                trash["held"] = False

    # Update trash
    for trash in trash_list:
        if trash["held"]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            trash["x"] = mouse_x - trash_img.get_width() // 2
            trash["y"] = mouse_y - trash_img.get_height() // 2
        else:
            trash["y"] += 0.05

        trash_rect = pygame.Rect(trash["x"], trash["y"], trash_img.get_width(), trash_img.get_height())
        dustbin_rect = pygame.Rect(dustbinX, dustbinY, dustbin_img.get_width(), dustbin_img.get_height())

        if trash_rect.colliderect(dustbin_rect) and not trash["held"]:
            score += 1
            trash["x"] = random.randint(50, 750)
            trash["y"] = 0

        if trash["y"] >= 600:
            missed += 1
            trash["x"] = random.randint(50, 750)
            trash["y"] = 0

        trashFunc(trash["x"], trash["y"])

    # Check game over
    if missed >= 3:
        game_over = True
        continue

    dustbinFunc(dustbinX, dustbinY)
    show_score()
    show_negative_score()
    pygame.display.update()