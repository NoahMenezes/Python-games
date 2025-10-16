import pygame
from pygame.locals import *
import time
import random
import os

# --- Constants ---
SIZE = 40
# The solid background color is no longer needed, but we keep it as a fallback.
BACKGROUND_COLOR = (110, 110, 5) 
BG_MUSIC_PATH = "resources/bg_music_1.mp3" 

# NEW CONSTANT: Use the provided relative path for the background image
BG_IMAGE_PATH = "resources/background.jpg" 

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self, max_x, max_y):
        grid_width = max_x // SIZE
        grid_height = max_y // SIZE
        self.x = random.randint(0, grid_width - 1) * SIZE
        self.y = random.randint(0, grid_height - 1) * SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'
        self.last_direction = 'down'

        self.length = length
        self.x = [SIZE] * length
        self.y = [SIZE] * length

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
        
    def move_left(self):
        if self.last_direction != 'right':
            self.direction = 'left'

    def move_right(self):
        if self.last_direction != 'left':
            self.direction = 'right'

    def move_up(self):
        if self.last_direction != 'down':
            self.direction = 'up'

    def move_down(self):
        if self.last_direction != 'up':
            self.direction = 'down'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE
        elif self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'down':
            self.y[0] += SIZE
        
        self.last_direction = self.direction 

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init() 
        pygame.display.set_caption("Snake Game") 
        
        pygame.mixer.init()
        
        self.surface = pygame.display.set_mode((1000, 800))
        self.screen_width, self.screen_height = self.surface.get_size()
        
        # NEW: Load the background image
        try:
            self.background = pygame.image.load(BG_IMAGE_PATH).convert()
            # Scale the background image to fit the screen size
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            print("Falling back to solid color.")
            self.background = None

        self.sound_ding = pygame.mixer.Sound("resources/ding.mp3") 
        self.sound_crash = pygame.mixer.Sound("resources/crash.mp3") 
        
        try:
            pygame.mixer.music.load(BG_MUSIC_PATH)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
             print(f"Error loading background music: {e}")
        
        self.snake = Snake(self.surface, 1) 
        self.apple = Apple(self.surface)
        self.is_running = True
        self.clock = pygame.time.Clock() # Ensure clock is initialized once here

    def is_collision(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return True
        return False

    def reset(self):
        self.snake = Snake(self.surface, 1) 
        self.apple = Apple(self.surface)
        self.is_running = True
        pygame.mixer.music.play(-1)

    def play(self):
        self.snake.walk()
        
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            pygame.mixer.Sound.play(self.sound_ding)
            self.snake.increase_length()
            self.apple.move(self.screen_width, self.screen_height)
            
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(self.sound_crash)
                self.is_running = False 
                break
                
        if not (0 <= self.snake.x[0] < self.screen_width and 0 <= self.snake.y[0] < self.screen_height):
             pygame.mixer.music.stop()
             pygame.mixer.Sound.play(self.sound_crash)
             self.is_running = False

    def show_game_over(self) :
        # Use background image if loaded, otherwise fill
        if self.background:
            self.surface.blit(self.background, (0, 0))
        else:
            self.surface.fill(BACKGROUND_COLOR)
            
        font=pygame.font.SysFont('arial',30)
        
        score_text = f"Game is over! Your score is {self.snake.length - 1}"
        line1=font.render(score_text, True, (255,255,255)) 
        self.surface.blit(line1, (200,300))
        
        line2=font.render("To play again press Enter. To exit press Escape!", True, (255,255,255))
        self.surface.blit(line2, (200,350))
        
        pygame.display.flip()
        
    def render(self):
        # NEW: Draw the background image first
        if self.background:
            self.surface.blit(self.background, (0, 0))
        else:
            self.surface.fill(BACKGROUND_COLOR)
            
        self.apple.draw()
        self.snake.draw()
        self.display_score()
        pygame.display.flip()
            
    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length - 1}", True, (255, 255, 255))
        self.surface.blit(score, (850, 10))
        
    def run(self):
        running = True
        FPS = 10 
        
        while running:
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    if not self.is_running and event.key == K_RETURN:
                        self.reset()
                    
                    if self.is_running:
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        elif event.key == K_RIGHT:
                            self.snake.move_right()
                        elif event.key == K_UP:
                            self.snake.move_up()
                        elif event.key == K_DOWN:
                            self.snake.move_down()

            if self.is_running:
                self.play()
                self.render()
            else:
                self.show_game_over() 
                
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()