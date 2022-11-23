import random
import time

import pygame
from pygame.locals import *

SIZE = 40


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.apple_img = pygame.image.load("resources/apple.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        print('draw apple')
        self.parent_screen.blit(self.apple_img, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = SIZE * random.randint(1, 12)
        self.y = SIZE * random.randint(1, 12)


class Snake:
    def __init__(self, parent_screen):
        self.length = 1
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [40]
        self.y = [40]
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill((110, 110, 5))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(len(self.x) - 1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i - 1]
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((600, 600))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # collision with an apple
        if self.apple.x == self.snake.x[0] and self.apple.y == self.snake.y[0]:
            sound = pygame.mixer.Sound("resources/1_snake_game_resources_ding.mp3")
            pygame.mixer.Sound.play(sound)
            self.apple.move()
            self.snake.increase_length()

        # collision with itself
        for i in range(1, self.snake.length):
            if self.snake.x[0] == self.snake.x[i] and self.snake.y[0] == self.snake.y[i]:
                sound = pygame.mixer.Sound("resources/1_snake_game_resources_crash.mp3")
                pygame.mixer.Sound.play(sound)
                raise "Game Over"

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (10, 10))
        pygame.display.flip()

    def show_game_over(self):
        self.surface.fill((110, 110, 5))
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game over! Your score is: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (50, 10))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (50, 100))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset_game(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset_game()
            time.sleep(0.2)


if __name__ == '__main__':
    print('Welcome to my snake game')
    game = Game()
    game.run()
