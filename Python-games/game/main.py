import pygame
import time

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = 100    
        self.y = 100
        
    def draw(self):
        self.parent_screen.fill((91, 21, 176))
        self.parent_screen.blit(self.block, (self.x, self.y))
        pygame.display.flip()
        
    def move(self, x, y):
        self.x += x
        self.y += y
        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((500, 500))
        self.snake = Snake(self.surface)
        self.snake.draw()
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_LEFT:
                        self.snake.move(-10, 0)
                    if event.key == pygame.K_RIGHT:
                        self.snake.move(10, 0)
                    if event.key == pygame.K_UP:
                        self.snake.move(0, -10)
                    if event.key == pygame.K_DOWN:
                        self.snake.move(0, 10)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()