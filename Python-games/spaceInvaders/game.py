import pygame
import math
import random
from pygame import mixer

# Initialize
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Game development')

icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
background = pygame.image.load('background2.jpg')

# Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 460
playerX_change = 0
playerY_change = 0

# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.8)
    enemyY_change.append(20)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 0.8
bullet_state = "ready"

# Score
pygame.font.init()
font = pygame.font.Font(None, 32)
score = 0

# Functions
def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    screen.blit(bulletImg, (x + 16, y + 10))

def show_score(x, y):
    score_text = font.render("Score: " + str(score), True, (0, 255, 0))
    screen.blit(score_text, (x, y))

def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    return distance < 27

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.8
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.8
            if event.key == pygame.K_UP:
                playerY_change = -0.8
            if event.key == pygame.K_DOWN:
                playerY_change = 0.8
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    bullet_state = "fire"

        # Key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # Player movement
    playerX += playerX_change
    playerY += playerY_change
    playerX = max(0, min(playerX, 736))
    playerY = max(0, min(playerY, 536))

    # Enemy movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0 or enemyX[i] >= 736:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]

        # Collision
        if bullet_state == "fire":
            if is_collision(enemyX[i], enemyY[i], bulletX, bulletY):
                explosion = mixer.Sound('explosion.wav')
                explosion.play()
                bulletY = playerY
                bullet_state = "ready"
                score += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        if bulletY <= 0:
            bullet_state = "ready"
            bulletY = playerY

    # Draw player and score
    player(playerX, playerY)
    show_score(10, 10)

    pygame.display.update()
