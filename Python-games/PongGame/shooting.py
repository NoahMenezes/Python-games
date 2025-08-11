import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Pong game')
icon = pygame.image.load('soccer-ball.png')
pygame.display.set_icon(icon)

# Load and play background music in a loop
pygame.mixer.music.load("background.mp3")  # or "background.ogg"
pygame.mixer.music.play(-1)  # -1 makes it loop forever

pongPaddle1 = pygame.image.load('line.png')
pongPaddleX1 = 736
pongPaddleY1 = 250
pongPaddleY_change1 = 0

pongPaddle2 = pygame.image.load('line.png')
pongPaddleX2 = 0
pongPaddleY2 = 250
pongPaddleY_change2 = 0

ball = pygame.image.load('basket-ball.png')
ballX = 400
ballY = 300
ballX_change = 0.15
ballY_change = 0.15

# Score
score1 = 0  # Right player
score2 = 0  # Left player
font = pygame.font.Font(None, 36)

# Ai padding movement
start_font = pygame.font.Font(None, 48)
# Game state
ball_active = False
ball_holder = random.choice([1, 2])

# Functions
def draw_paddle1(x, y):
    screen.blit(pongPaddle1, (x, y))

def draw_paddle2(x, y):
    screen.blit(pongPaddle2, (x, y))

def ball_paddle(x, y):
    screen.blit(ball, (x, y))

def show_score():
    score_text = font.render(f"{score2} : {score1}", True, (0, 0, 0))
    screen.blit(score_text, (370, 10))

def draw_center_line():
    for y in range(0, 600, 30):
        pygame.draw.line(screen, (0, 0, 0), (400, y), (400, y + 15), 2)
def show_start_screen_with_button():
    screen.fill((100, 235, 52))
    title = start_font.render("Welcome to Pong Game!", True, (0, 0, 0))
    screen.blit(title, (220, 200))

    # Button setup
    button_rect = pygame.Rect(300, 300, 200, 50)
    pygame.draw.rect(screen, (0,0,0), button_rect)  # Black button
    button_text = font.render("Start Game", True, (255, 255, 255))
    screen.blit(button_text, (button_rect.x + 35, button_rect.y + 10))

    pygame.display.update()
    return button_rect
button_rect = show_start_screen_with_button()
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                waiting = False
# Game loop
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(2000)  # Limit to 60 FPS
    screen.fill((100, 235, 52))
    draw_center_line()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Launch the ball
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not ball_active:
                ball_active = True
                angle = random.uniform(-0.3, 0.3)
                speed = 0.3
                if ball_holder == 1:
                    ballX_change = -speed
                else:
                    ballX_change = speed
                ballY_change = speed * math.sin(angle)

    # Controls for player 1 (Right)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        pongPaddleY1 -= 0.3
    if keys[pygame.K_DOWN]:
        pongPaddleY1 += 0.3

    # Controls for player 2 (Left)
    if keys[pygame.K_w]:
        pongPaddleY2 -= 0.3
    if keys[pygame.K_s]:
        pongPaddleY2 += 0.3

    # Limit paddles within screen
    pongPaddleY1 = max(0, min(600 - pongPaddle1.get_height(), pongPaddleY1))
    pongPaddleY2 = max(0, min(600 - pongPaddle2.get_height(), pongPaddleY2))

    # Update ball position only if active
    if ball_active:
        ballX += ballX_change
        ballY += ballY_change

        # Bounce off top and bottom
        if ballY <= 0 or ballY >= 600 - ball.get_height():
            ballY_change *= -1

        # Paddle collisions
        paddle_height = pongPaddle1.get_height()

        # Right paddle
        if ballX >= pongPaddleX1 - ball.get_width():
            if pongPaddleY1 <= ballY <= pongPaddleY1 + paddle_height:
                ballX = pongPaddleX1 - ball.get_width()
                ballX_change *= -1
                offset = (ballY - (pongPaddleY1 + paddle_height / 2)) / (paddle_height / 2)
                ballY_change = offset * 0.3

        # Left paddle
        if ballX <= pongPaddleX2 + pongPaddle2.get_width():
            if pongPaddleY2 <= ballY <= pongPaddleY2 + paddle_height:
                ballX = pongPaddleX2 + pongPaddle2.get_width()
                ballX_change *= -1
                offset = (ballY - (pongPaddleY2 + paddle_height / 2)) / (paddle_height / 2)
                ballY_change = offset * 0.3

        # Scoring
        if ballX < 0:
            score1 += 1
            ball_active = False
            ball_holder = 2
        elif ballX > 800 - ball.get_width():
            score2 += 1
            ball_active = False
            ball_holder = 1

    else:
        # Ball stays on paddle if inactive
        if ball_holder == 1:
            ballX = pongPaddleX1 - 16
            ballY = pongPaddleY1 + 16
        else:
            ballX = pongPaddleX2 + 16
            ballY = pongPaddleY2 + 16

    draw_paddle1(pongPaddleX1, pongPaddleY1)
    draw_paddle2(pongPaddleX2, pongPaddleY2)
    ball_paddle(ballX, ballY)
    show_score()
    pygame.display.update()
