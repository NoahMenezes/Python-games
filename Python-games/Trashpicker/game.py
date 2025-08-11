import pygame
import random

pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Dodge the Falling Blocks")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)

# Player
player_size = 50
player_x = 375
player_y = 550
player_speed = 5

# Block
block_size = 50
block_x = random.randint(0, 750)
block_y = -50
block_speed = 3

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < 800 - player_size:
        player_x += player_speed

    # Move block
    block_y += block_speed

    # Check for collision
    if (
        block_y + block_size > player_y and
        block_x < player_x + player_size and
        block_x + block_size > player_x
    ):
        print("Game Over!")
        running = False

    # Reset block and increase score
    if block_y > 600:
        block_y = -50
        block_x = random.randint(0, 750)
        score += 1
        block_speed += 0.2  # Increase difficulty

    # Draw player and block
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
    pygame.draw.rect(screen, RED, (block_x, block_y, block_size, block_size))

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    pygame.time.Clock().tick(60)