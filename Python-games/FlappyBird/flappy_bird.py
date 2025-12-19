import random
import sys

import pygame

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 600
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
SETTINGS_BG = (70, 130, 180)

# Game variables
gravity = 0.5
bird_movement = 0
game_active = False
score = 0
high_score = 0
can_score = True
game_speed = 3.0
base_speed = 3.0
speed_increase_rate = 3
game_state = "menu"  # menu, playing, game_over, settings

# Settings variables
difficulty = "medium"  # easy, medium, hard
sound_enabled = True

# Difficulty settings
DIFFICULTY_SETTINGS = {
    "easy": {"gravity": 0.4, "gap": 200, "speed_increase": 0.015, "base_speed": 2.5},
    "medium": {"gravity": 0.5, "gap": 180, "speed_increase": 0.02, "base_speed": 3.0},
    "hard": {"gravity": 0.6, "gap": 160, "speed_increase": 0.03, "base_speed": 3.5},
}

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)
menu_font = pygame.font.Font(None, 35)
small_font = pygame.font.Font(None, 25)

# Load sounds
try:
    crash_sound = pygame.mixer.Sound("sounds/crash.wav")
    jump_sound = pygame.mixer.Sound("sounds/jump.wav")
    score_sound = pygame.mixer.Sound("sounds/score.wav")
    sounds_loaded = True
except (pygame.error, FileNotFoundError) as e:
    print(
        f"Warning: Could not load sound files. Game will run without sound. Error: {e}"
    )
    sounds_loaded = False
    crash_sound = None
    jump_sound = None
    score_sound = None


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
        self.velocity = -8
        # Play jump sound
        if sound_enabled and sounds_loaded and jump_sound:
            jump_sound.play()

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
        self.gap = DIFFICULTY_SETTINGS[difficulty]["gap"]
        self.top_height = random.randint(100, SCREEN_HEIGHT - 250)
        self.speed = game_speed
        self.scored = False

    def update(self):
        self.speed = game_speed  # Update speed dynamically
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


# Toggle Button class for settings
class ToggleButton:
    def __init__(self, x, y, width, height, options, default_index=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.current_index = default_index
        self.hover = False

    def draw(self, surface):
        color = BUTTON_HOVER if self.hover else BUTTON_COLOR

        # Draw button
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=8)

        # Draw current option text
        text_surf = small_font.render(self.options[self.current_index], True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def toggle(self):
        self.current_index = (self.current_index + 1) % len(self.options)
        return self.options[self.current_index]

    def get_value(self):
        return self.options[self.current_index]


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

    # Draw speed indicator
    speed_text = small_font.render(f"Speed: {game_speed:.1f}x", True, WHITE)
    speed_shadow = small_font.render(f"Speed: {game_speed:.1f}x", True, TEXT_SHADOW)
    speed_rect = speed_text.get_rect(topright=(SCREEN_WIDTH - 20, 65))
    shadow_rect = speed_rect.copy()
    shadow_rect.x += 2
    shadow_rect.y += 2

    screen.blit(speed_shadow, shadow_rect)
    screen.blit(speed_text, speed_rect)


def draw_menu():
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(SKY_BLUE)
    screen.blit(overlay, (0, 0))

    # Title
    title_text = title_font.render("FLAPPY BIRD", True, (255, 215, 0))
    title_shadow = title_font.render("FLAPPY BIRD", True, TEXT_SHADOW)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
    shadow_rect = title_rect.copy()
    shadow_rect.x += 3
    shadow_rect.y += 3

    screen.blit(title_shadow, shadow_rect)
    screen.blit(title_text, title_rect)

    # High score
    high_score_text = menu_font.render(f"High Score: {high_score}", True, WHITE)
    high_score_shadow = menu_font.render(f"High Score: {high_score}", True, TEXT_SHADOW)
    high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
    shadow_rect = high_score_rect.copy()

    shadow_rect.x += 2
    shadow_rect.y += 2

    screen.blit(high_score_shadow, shadow_rect)
    screen.blit(high_score_text, high_score_rect)

    # Instructions
    inst_text = small_font.render("SPACE or CLICK to Flap", True, WHITE)
    inst_shadow = small_font.render("SPACE or CLICK to Flap", True, TEXT_SHADOW)
    inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, 270))
    shadow_rect = inst_rect.copy()
    shadow_rect.x += 2
    shadow_rect.y += 2

    screen.blit(inst_shadow, shadow_rect)
    screen.blit(inst_text, inst_rect)

    # Draw buttons
    play_button.draw(screen)
    settings_button.draw(screen)


def draw_settings():
    # Background
    screen.fill(SETTINGS_BG)

    # Title
    title_text = title_font.render("SETTINGS", True, WHITE)
    title_shadow = title_font.render("SETTINGS", True, TEXT_SHADOW)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
    shadow_rect = title_rect.copy()
    shadow_rect.x += 3
    shadow_rect.y += 3

    screen.blit(title_shadow, shadow_rect)
    screen.blit(title_text, title_rect)

    # Difficulty label
    diff_label = menu_font.render("Difficulty:", True, WHITE)
    screen.blit(diff_label, (50, 170))

    # Sound label
    sound_label = menu_font.render("Sound:", True, WHITE)
    screen.blit(sound_label, (50, 250))

    # Info text
    info_lines = [
        "Easy: Slower speed, bigger gaps",
        "Medium: Balanced gameplay",
        "Hard: Faster speed, smaller gaps",
        "",
        "Speed increases as you play!",
    ]
    y_offset = 350
    for line in info_lines:
        info_text = small_font.render(line, True, WHITE)
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(info_text, info_rect)
        y_offset += 25

    # Draw toggle buttons
    difficulty_toggle.draw(screen)
    sound_toggle.draw(screen)

    # Draw back button
    back_button.draw(screen)


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
    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, 230))
    shadow_rect = final_score_rect.copy()
    shadow_rect.x += 2
    shadow_rect.y += 2

    screen.blit(final_score_shadow, shadow_rect)
    screen.blit(final_score_text, final_score_rect)

    # High score
    high_score_text = score_font.render(f"Best: {high_score}", True, (255, 215, 0))
    high_score_shadow = score_font.render(f"Best: {high_score}", True, TEXT_SHADOW)
    high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
    shadow_rect = high_score_rect.copy()
    shadow_rect.x += 2
    shadow_rect.y += 2

    screen.blit(high_score_shadow, shadow_rect)
    screen.blit(high_score_text, high_score_rect)

    # Max speed reached
    max_speed_text = small_font.render(f"Max Speed: {game_speed:.1f}x", True, WHITE)
    max_speed_rect = max_speed_text.get_rect(center=(SCREEN_WIDTH // 2, 330))
    screen.blit(max_speed_text, max_speed_rect)

    # Restart button
    restart_button.draw(screen)
    menu_button.draw(screen)


def reset_game():
    global \
        bird, \
        pipes, \
        score, \
        game_speed, \
        game_active, \
        pipe_spawn_timer, \
        gravity, \
        base_speed, \
        speed_increase_rate
    game_active = True
    bird = Bird()
    pipes = []
    score = 0
    pipe_spawn_timer = 0

    # Apply difficulty settings
    settings = DIFFICULTY_SETTINGS[difficulty]
    gravity = settings["gravity"]
    base_speed = settings["base_speed"]
    speed_increase_rate = settings["speed_increase"]
    game_speed = base_speed


# Initialize game objects
bird = Bird()
pipes = []
pipe_spawn_timer = 0

# Initialize buttons
play_button = Button(SCREEN_WIDTH // 2 - 100, 330, 200, 60, "PLAY")
settings_button = Button(SCREEN_WIDTH // 2 - 100, 410, 200, 60, "SETTINGS")
restart_button = Button(SCREEN_WIDTH // 2 - 100, 390, 200, 50, "RESTART")
menu_button = Button(SCREEN_WIDTH // 2 - 100, 460, 200, 50, "MENU")
back_button = Button(SCREEN_WIDTH // 2 - 100, 500, 200, 50, "BACK")

# Initialize toggle buttons
difficulty_toggle = ToggleButton(220, 165, 130, 40, ["Easy", "Medium", "Hard"], 1)
sound_toggle = ToggleButton(220, 245, 130, 40, ["ON", "OFF"], 0)

# Main game loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == "playing":
                    bird.jump()
                elif game_state == "menu":
                    game_state = "playing"
                    reset_game()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu":
                if play_button.is_clicked(mouse_pos):
                    game_state = "playing"
                    reset_game()
                elif settings_button.is_clicked(mouse_pos):
                    game_state = "settings"

            elif game_state == "settings":
                if back_button.is_clicked(mouse_pos):
                    game_state = "menu"
                elif difficulty_toggle.is_clicked(mouse_pos):
                    difficulty = difficulty_toggle.toggle().lower()
                elif sound_toggle.is_clicked(mouse_pos):
                    sound_status = sound_toggle.toggle()
                    sound_enabled = sound_status == "ON"

            elif game_state == "playing":
                bird.jump()

            elif game_state == "game_over":
                if restart_button.is_clicked(mouse_pos):
                    game_state = "playing"
                    reset_game()
                elif menu_button.is_clicked(mouse_pos):
                    game_state = "menu"

    # Update game state
    if game_state == "playing":
        bird.update()

        # Increase speed progressively
        game_speed = base_speed + (score * speed_increase_rate)
        game_speed = min(game_speed, base_speed * 2.5)  # Cap at 2.5x base speed

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
                # Play score sound
                if sound_enabled and sounds_loaded and score_sound:
                    score_sound.play()
                if score > high_score:
                    high_score = score

        # Check collisions
        if bird.check_collision(pipes):
            game_state = "game_over"
            # Play crash sound
            if sound_enabled and sounds_loaded and crash_sound:
                crash_sound.play()

    # Drawing
    draw_background()
    draw_clouds()

    # Draw pipes
    for pipe in pipes:
        pipe.draw(screen)

    # Draw bird
    bird.draw(screen)

    # Draw UI based on game state
    if game_state == "menu":
        play_button.check_hover(mouse_pos)
        settings_button.check_hover(mouse_pos)
        draw_menu()

    elif game_state == "settings":
        difficulty_toggle.check_hover(mouse_pos)
        sound_toggle.check_hover(mouse_pos)
        back_button.check_hover(mouse_pos)
        draw_settings()

    elif game_state == "playing":
        draw_score()

    elif game_state == "game_over":
        draw_score()
        restart_button.check_hover(mouse_pos)
        menu_button.check_hover(mouse_pos)
        draw_game_over()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
