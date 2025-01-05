# Snake Game
import pygame
import random
import os
import sys

# Initialize Pygame
pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Game settings
screen_width = 800
screen_height = 600
snake_block = 10
snake_speed = 15

# Set up display
game_screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

# Clock
clock = pygame.time.Clock()

# Font styles
score_font = pygame.font.SysFont("monospace", 35)
game_over_font = pygame.font.SysFont("monospace", 32)
font_style = pygame.font.SysFont("monospace", 35)


class Button:
    def __init__(self, x, y, width, height, color, text="", action=None, text_color=black):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action
        self.text_color = text_color

    def draw(self, screen):  # Draw the screen
        pygame.draw.rect(screen, self.color, self.rect)
        if self.text:
            font_surface = font_style.render(self.text, 1, self.text_color)
            text_rect = font_surface.get_rect(center=self.rect.center)
            screen.blit(font_surface, text_rect)

    def clicked(self, position):  # Click the button
        return self.rect.collidepoint(position)


def main_menu():  # Main menu function
    logo_path = os.path.join("Images", "Snake_game_logo.png")
    logo_image = pygame.image.load(logo_path)
    resized_image = pygame.transform.scale(logo_image, (600, 250))
    play_button = Button(300, 450, 200, 50, black, "PLAY", game_loop, white)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.clicked(pygame.mouse.get_pos()):
                    play_button.action()
        game_screen.fill(black)
        game_screen.blit(resized_image, (70, 55))
        play_button.draw(game_screen)
        pygame.display.update()


def game_score(score):
    value = score_font.render("Score: " + str(score), True, black)
    game_screen.blit(value, [10, 10])


def our_snake(block, snake_list):
    for x in snake_list:
        pygame.draw.rect(game_screen, black, [x[0], x[1], block, snake_block])


def message(msg, color):  # Display Game Over Message
    mess = game_over_font.render(msg, True, color)
    mess_rect = mess.get_rect(center=(screen_width / 2, screen_height / 2))  # Center of the screen
    game_screen.blit(mess, mess_rect)


def game_loop():  # Main Game
    game_over = False
    game_close = False

    x1 = screen_width / 2
    y1 = screen_height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    food_x = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            game_screen.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            game_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        game_screen.fill(blue)
        pygame.draw.rect(game_screen, green, [food_x, food_y, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(snake_block, snake_list)
        game_score(length_of_snake - 1)

        pygame.display.update()

        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, screen_width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, screen_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


def main():
    main_menu()


main()
