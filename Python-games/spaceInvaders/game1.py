import pygame
import random
import math
from pygame import mixer
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background1.jpg')

mixer.music.load('background.wav')
mixer.music.play(-1)

pygame.display.set_caption("space-invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player setup
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy setup
enemyImg =[]
enemyX=[]
enemyY=[]
enemyX_change =[]
enemyY_change=[]
no_of_enemies=random.randint(1,6)
for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.5)
    enemyY_change.append(5)

# Bullet setup
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 1
bullet_state = "ready"  # 'ready' means you can fire; 'fire' means bullet is moving

# Score setup
score = 0
font = pygame.font.Font(None, 32)  # Default font with size 32

# Functions
def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX - bulletX), 2)) + (math.pow((enemyY - bulletY), 2)))
    return distance < 27
# Score
def show_score(x, y):
    score_text = font.render("Score : " + str(score), True, (0,255,0))  
    screen.blit(score_text, (x, y))


# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key press detection
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_Sound=mixer.Sound('laser.wav')
                    bullet_Sound.play()

        # Key release detection
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

        enemy(enemyX[i], enemyY[i],i)
    # Player movement
    playerX += playerX_change
    playerX = max(0, min(playerX, 736))  # Keep within screen bounds

    # Enemy movement
    for i in range(no_of_enemies):               
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]
    # Collision detection
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound=mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            print("Score:", score)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i],enemyY[i], i )
        # Bullet movement
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
            if bulletY <= 0:
                bulletY = 480
                bullet_state = "ready"

    # Drawing
    player(playerX, playerY)
    show_score(10, 10)

    pygame.display.update()
