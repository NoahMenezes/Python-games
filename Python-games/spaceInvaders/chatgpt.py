import pygame
import random

pygame.init()

# Screen
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background1.jpg')
pygame.display.set_caption("space-invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480

# Enemy
enemyImg = pygame.image.load('alien.png')
enemyX = random.randint(64, 736)
enemyY = 100
enemyX_change = 1
enemyY_change = 10

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 3
bullet_state = "ready"

# Functions
def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movement keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX -= 5
            if event.key == pygame.K_RIGHT:
                playerX += 5
            if event.key == pygame.K_UP:
                playerY -= 5
            if event.key == pygame.K_DOWN:
                playerY += 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX  # Set bullet start X to player X
                    fire_bullet(bulletX, bulletY)

    # Keep player on screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # Enemy movement
    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change = 1
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -1
        enemyY += enemyY_change

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

    # Draw everything
    player(playerX, playerY)
    enemy(enemyX, enemyY)

    pygame.display.update()
