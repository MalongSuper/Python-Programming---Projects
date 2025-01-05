# Tank Destroyer Game
import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Destroyer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


# Tank
tank_path = os.path.join("Images", "tank.png")
tank_img = pygame.image.load(tank_path)
tank_img = pygame.transform.scale(tank_img, (150, 150))
tank_rect = tank_img.get_rect()
tank_rect.center = (WIDTH // 2, HEIGHT - 50)
tank_speed = 5


# Enemy
enemy_path = os.path.join("Images", "tank_enemy.png")
enemy_img = pygame.image.load(enemy_path)
enemy_img = pygame.transform.scale(enemy_img, (150, 150))
enemy_rect = enemy_img.get_rect()
enemy_rect.center = (random.randint(0, WIDTH), 0)
enemy_speed = 3


# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move tank
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        tank_rect.x -= tank_speed
    if keys[pygame.K_RIGHT]:
        tank_rect.x += tank_speed

    # Move enemy
    enemy_rect.y += enemy_speed
    if enemy_rect.y > HEIGHT:
        enemy_rect.y = 0
        enemy_rect.center = (random.randint(0, WIDTH), 0)

    # Collision detection
    if tank_rect.colliderect(enemy_rect):
        running = False

    # Draw tank and enemy
    screen.blit(tank_img, tank_rect)
    screen.blit(enemy_img, enemy_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
