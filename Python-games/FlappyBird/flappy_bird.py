import random
import sys

import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GROUND_BROWN = (222, 184, 135)
PIPE_GREEN = (34, 139, 34)
BUTTON_COLOR = (255, 215, 0)
BUTTON_HOVER = (255, 235, 50)
TEXT_SHADOW = (50, 50, 50)

# Game variables
gravity = 0.5
bird_movement = 0
game_active = False
score = 0
high_score = 0
can_score = True

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)
menu_font = pygame.font.Font(None, 35)


# Bird class
class Bird:
    def __init__(self):
        self.x = 80
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.radius = 15
        self.color = (255, 255, 0)
        self.outline_color = (255, 140, 0)
        self.rotation = 0

    def jump(self):
        self.velocity = -10

    def update(self):
        self.velocity += gravity
        self.y += self.velocity

        # Rotation based on velocity
        self.rotation = max(-25, min(25, -self.velocity * 3))

    def draw(self, surface):
        # Draw bird body
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(
            surface, self.outline_color, (int(self.x), int(self.y)), self.radius, 3
        )

        # Draw eye
        eye_x = int(self.x + 5)
        eye_y = int(self.y - 3)
        pygame.draw.circle(surface, WHITE, (eye_x, eye_y), 5)
        pygame.draw.circle(surface, BLACK, (eye_x + 2, eye_y), 3)

        # Draw beak
        beak_points = [
            (int(self.x + self.radius), int(self.y)),
            (int(self.x + self.radius + 8), int(self.y - 3)),
            (int(self.x + self.radius + 8), int(self.y + 3)),
        ]
        pygame.draw.polygon(surface, (255, 165, 0), beak_points)

    def check_collision(self, pipes):
        # Check if bird hits ground or ceiling
        if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_HEIGHT - 100:
            return True

        # Check pipe collision
        for pipe in pipes:
            if (
                pipe.x < self.x + self.radius < pipe.x + pipe.width
                or pipe.x < self.x - self.radius < pipe.x + pipe.width
            ):
                if (
                    self.y - self.radius < pipe.top_height
                    or self.y + self.radius > pipe.top_height + pipe.gap
                ):
                    return True
        return False


# Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.width = 70
        self.gap = 180
        self.top_height = random.randint(100, SCREEN_HEIGHT - 250)
        self.speed = 3
        self.scored = False

    def update(self):
        self.x -= self.speed

    def draw(self, surface):
        # Top pipe
        pygame.draw.rect(surface, PIPE_GREEN, (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(
            surface, (20, 100, 20), (self.x, 0, self.width, self.top_height), 3
        )

        # Top pipe cap
        pygame.draw.rect(
            surface,
            (50, 150, 50),
            (self.x - 5, self.top_height - 20, self.width + 10, 20),
        )

        # Bottom pipe
        bottom_y = self.top_height + self.gap
        pygame.draw.rect(
            surface,
            PIPE_GREEN,
            (self.x, bottom_y, self.width, SCREEN_HEIGHT - bottom_y),
        )
        pygame.draw.rect(
            surface,
            (20, 100, 20),
            (self.x, bottom_y, self.width, SCREEN_HEIGHT - bottom_y),
            3,
        )

        # Bottom pipe cap
        pygame.draw.rect(
            surface, (50, 150, 50), (self.x - 5, bottom_y, self.width + 10, 20)
        )

    def off_screen(self):
        return self.x < -self.width


# Button class
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = BUTTON_COLOR
        self.hover = False

    def draw(self, surface):
        color = BUTTON_HOVER if self.hover else BUTTON_COLOR

        # Draw button shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(surface, TEXT_SHADOW, shadow_rect, border_radius=10)

        # Draw button
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=10)

        # Draw text
        text_surf = menu_font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# Draw functions
def draw_background():
    # Sky gradient
    for i in range(SCREEN_HEIGHT - 100):
        color = (135, 206 - i // 20, 235)
        pygame.draw.line(screen, color, (0, i), (SCREEN_WIDTH, i))

    # Ground
    pygame.draw.rect(screen, GROUND_BROWN, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
    pygame.draw.rect(screen, (180, 140, 100), (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 5))

    # Draw grass on ground
    for i in range(0, SCREEN_WIDTH, 20):
        pygame.draw.line(
            screen,
            (34, 139, 34),
            (i, SCREEN_HEIGHT - 100),
            (i + 5, SCREEN_HEIGHT - 95),
            2,
        )


def draw_clouds():
    cloud_positions = [(80, 100), (250, 80), (350, 120), (150, 180)]
    for pos in cloud_positions:
        pygame.draw.circle(screen, WHITE, pos, 20)
        pygame.draw.circle(screen, WHITE, (pos[0] + 15, pos[1]), 25)
        pygame.draw.circle(screen, WHITE, (pos[0] + 30, pos[1]), 20)
        pygame.draw.circle(screen, WHITE, (pos[0] + 15, pos[1] + 10), 20)


def draw_score():
    # Draw current score (top right)
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    score_shadow = score_font.render(f"Score: {score}", True, TEXT_SHADOW)
    score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
    shadow_rect = score_rect.copy()
    shadow_rect.x += 2
    shadow_rect.y += 2

    screen.blit(score_shadow, shadow_rect)
    screen.blit(score_text, score_rect)


def draw_menu():
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(SKY_BLUE)
    screen.blit(overlay, (0, 0))

    # Title
    title_text = title_font.render("FLAPPY BIRD", True, (255, 215, 0))
    title_shadow = title_font.render("FLAPPY BIRD", True, TEXT_SHADOW)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
    shadow_rect = title_rect.copy()
    shadow_rect.x += 3
    shadow_rect.y += 3

    screen.blit(title_shadow, shadow_rect)
    screen.blit(title_text, title_rect)

    # High score
    high_score_text = menu_font.render(f"High Score: {high_score}", True, WHITE)
    high_score_shadow = menu_font.render(f"High Score: {high_score}", True, TEXT_SHADOW)
    high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
    shadow_rect = high_score_rect.copy()
    shadow_rect.x += 2
    shadow_rect.y += 2

    screen.blit(high_score_shadow, shadow_rect)
    screen.blit(high_score_text, high_score_rect)

    # Instructions
    if not game_active and score == 0:
        inst_text = menu_font.render("Click to Start!", True, WHITE)
        inst_shadow = menu_font.render("Click to Start!", True, TEXT_SHADOW)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
        shadow_rect = inst_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2

        screen.blit(inst_shadow, shadow_rect)
        screen.blit(inst_text, inst_rect)

        control_text = menu_font.render("SPACE or CLICK to Flap", True, WHITE)
        control_shadow = menu_font.render("SPACE or CLICK to Flap", True, TEXT_SHADOW)
        control_rect = control_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        shadow_rect = control_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2

        screen.blit(control_shadow, shadow_rect)
        screen.blit(control_text, control_rect)


def draw_game_over():
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Game Over text
    game_over_text = title_font.render("GAME OVER", True, (255, 50, 50))
    game_over_shadow = title_font.render("GAME OVER", True, TEXT_SHADOW)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
    shadow_rect = game_over_rect.copy()
    shadow_rect.x += 3
    shadow_rect.y += 3

    screen.blit(game_over_shadow, shadow_rect)
    screen.blit(game_over_text, game_over_rect)

    # Final score
    final_score_text = score_font.render(f"Score: {score}", True, WHITE)
    final_score_shadow = score_font.render(f"Score: {score}", True, TEXT_SHADOW)
    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
    shadow_rect = final_score_rect.copy()
    shadow_rect.x += 2
    shadow_rect.y += 2

    screen.blit(final_score_shadow, shadow_rect)
    screen.blit(final_score_text, final_score_rect)

    # High score
    high_score_text = score_font.render(f"Best: {high_score}", True, (255, 215, 0))
    high_score_shadow = score_font.render(f"Best: {high_score}", True, TEXT_SHADOW)
    high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
    shadow_rect = high_score_rect.copy()
    shadow_rect.x += 2
    shadow_rect.y += 2

    screen.blit(high_score_shadow, shadow_rect)
    screen.blit(high_score_text, high_score_rect)

    # Restart button
    restart_button.draw(screen)


# Initialize game objects
bird = Bird()
pipes = []
pipe_spawn_timer = 0
restart_button = Button(SCREEN_WIDTH // 2 - 100, 400, 200, 60, "RESTART")

# Main game loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird.jump()
                else:
                    # Start/restart game
                    game_active = True
                    bird = Bird()
                    pipes = []
                    score = 0
                    can_score = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_active:
                bird.jump()
            else:
                if score > 0:  # Game over state
                    if restart_button.is_clicked(mouse_pos):
                        game_active = True
                        bird = Bird()
                        pipes = []
                        score = 0
                        can_score = True
                else:  # Initial menu state
                    game_active = True
                    bird = Bird()
                    pipes = []
                    score = 0
                    can_score = True

    # Update game state
    if game_active:
        bird.update()

        # Spawn pipes
        pipe_spawn_timer += 1
        if pipe_spawn_timer > 90:  # Spawn every 1.5 seconds
            pipes.append(Pipe())
            pipe_spawn_timer = 0

        # Update pipes
        for pipe in pipes[:]:
            pipe.update()
            if pipe.off_screen():
                pipes.remove(pipe)

            # Score when bird passes pipe
            if not pipe.scored and pipe.x + pipe.width < bird.x:
                pipe.scored = True
                score += 1
                if score > high_score:
                    high_score = score

        # Check collisions
        if bird.check_collision(pipes):
            game_active = False

    # Drawing
    draw_background()
    draw_clouds()

    # Draw pipes
    for pipe in pipes:
        pipe.draw(screen)

    # Draw bird
    bird.draw(screen)

    # Draw UI
    if game_active:
        draw_score()
    else:
        if score == 0:
            draw_menu()
        else:
            draw_score()
            restart_button.check_hover(mouse_pos)
            draw_game_over()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
