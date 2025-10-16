import pygame
import random
pygame.init()
screen = pygame.display.set_mode((800,600))

pygame.display.set_caption("Noah Menezes")
icon=pygame.image.load('Python-games/spaceInvaders/ufo.png')
pygame.display.set_icon(icon)

player=pygame.image.load('Python-games/spaceInvaders/space-invaders.png')
playerX=370
playerY=470
playerX_counter=0
playerY_counter=0
enemy =pygame.image.load('Python-games/spaceInvaders/alien.png')
enemyX=200
enemyY=100
background=pygame.image.load('Python-games/spaceInvaders/background1.jpg')

bullet=pygame.image.load('Python-games/spaceInvaders/bullet.png')
bulletX=0
bulletY=470
bulletY_change=1
bullet_state="ready"


enemyX_counter=1
def playerFunction(X,Y):
    screen.blit(player, (X,Y))
def enemyFunction(X,Y):
    screen.blit(enemy, (X,Y))
def fire_bullet(X, Y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (X + 16, Y + 16))  # Center bullet on player

running=True
while running:
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type ==pygame.KEYDOWN:
            if event.key ==pygame.K_LEFT or event.key == pygame.K_a:
                playerX_counter=-0.2
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_counter=0.2
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                playerY_counter=-0.2
            if event.key ==pygame.K_DOWN or event.key == pygame.K_s:
                playerY_counter=0.2
            if event.key == pygame.K_SPACE :
                if bullet_state=="ready":
                    bulletX=playerX
                    fire_bullet(bulletX, bulletY)
                    
        if event.type == pygame.KEYUP:
            if (event.key ==pygame.K_LEFT or event.key ==pygame.K_a) or (event.key == pygame.K_RIGHT or event.key ==pygame.K_d) or (event.key == pygame.K_UP or event.key ==pygame.K_w) or (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                playerX_counter=0
                playerY_counter=0
    playerX+=playerX_counter
    playerY+=playerY_counter
    if playerX<=0:
        playerX=0
    if playerX>=736:
        playerX=736
    if playerY<=0:
        playerY=0
    if playerY>=534:
        playerY=534
    
    if enemyX<=0:
        enemyX=0
        enemyX_counter=0.7
    if enemyX>=736:
        enemyX=736
        enemyX_counter=-0.7
    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"
    enemyX+=enemyX_counter
    playerFunction(playerX, playerY)
    enemyFunction(enemyX, enemyY)
    pygame.display.update()