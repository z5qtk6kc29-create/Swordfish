#Swordfish Beta

#I would like this game to maybe have inspiration from wordle and my work on it, but be its own game outright.

#I think that I would like to use pygame on this one somehow

#Next steps
#Make the shark be able to move
#Make there be multiple sharks
#Make the shark/swordfish have collision points
#Make the shark die if it is the tip of the sword, have the swordfish die if anything else
#Make a counter that keeps track of how many sharks you killed
#Make orange, yellow, and red fish that follow shark principles that you do not want to kill (the fish cannot kill swordfish though)
#-3 points for killing a fish
#Make a bomb button that kills everything, could help your score, could hurt
#End the game/maybe restart when a shark kills you

import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
FPS = 60

original_image = pygame.image.load('player_swordfish.png')
original_image = pygame.transform.scale(original_image, (100, 100))
player_image = original_image.copy()
player_rect = player_image.get_rect()
player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

numberx = [50, 700]
numbery = [50, 700]

original_image2 = pygame.image.load('computer_shark.png')
original_image2 = pygame.transform.scale(original_image2, (125, 125))
computer_image = original_image2.copy()
computer_rect = computer_image.get_rect()
computer_rect.center = (random.uniform(50, 700), random.uniform(50, 700))

velocity_x = 0
velocity_y = 0
change_direction_timer = 0
change_direction_interval = 60

player_speed = 5

running = True
while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        player_rect.y -= player_speed
        player_image = pygame.transform.rotate(original_image, 270)
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed
        player_image = pygame.transform.rotate(original_image, 90)
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
        player_image = pygame.transform.rotate(original_image, 0)
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
        player_image = pygame.transform.rotate(original_image, 180)

    if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
        player_image = pygame.transform.rotate(original_image, 225)
    if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
        player_image = pygame.transform.rotate(original_image, 135)
    if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
        player_image = pygame.transform.rotate(original_image, 45)
    if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
        player_image = pygame.transform.rotate(original_image, 315)

    change_direction_timer +=1
    if change_direction_timer >= change_direction_interval:
        velocity_x = random.uniform(-4, 4)
        velocity_y = random.uniform(-4, 4)
        change_direction_timer = 0

    computer_rect.x += velocity_x
    computer_rect.y += velocity_y

    if computer_rect.left < -50 or computer_rect.right > SCREEN_WIDTH:
        velocity_x *= -1.5
    if computer_rect.top < -50 or computer_rect.bottom > SCREEN_WIDTH:
        velocity_y *= -1.5

    if velocity_y > 0 and velocity_x == 0:
        computer_image = pygame.transform.rotate(original_image2, 90)
    if velocity_y == 0 and velocity_x > 0:
        computer_image = pygame.transform.rotate(original_image2, 180)
    if velocity_y == 0 and velocity_x < 0:
        computer_image = pygame.transform.rotate(original_image2, 0)
    if velocity_y < 0 and velocity_x == 0:
        computer_image = pygame.transform.rotate(original_image2, 270)

    if velocity_y > 0 and velocity_x > 0:
        computer_image = pygame.transform.rotate(original_image2, 135)
    if velocity_y < 0 and velocity_x < 0:
        computer_image = pygame.transform.rotate(original_image2, 315)
    if velocity_y > 0 and velocity_x < 0:
        computer_image = pygame.transform.rotate(original_image2, 45)
    if velocity_y < 0 and velocity_x > 0:
        computer_image = pygame.transform.rotate(original_image2, 225)

    if velocity_y == 0 and velocity_x == 0:
        computer_image = pygame.transform.rotate(original_image2, 0)

    player_rect.x = max(0, min(player_rect.x, SCREEN_WIDTH - player_rect.width))
    player_rect.y = max(0, min(player_rect.y, SCREEN_HEIGHT - player_rect.height))

    screen.fill((80, 140, 160))
    screen.blit(player_image, player_rect)
    screen.blit(computer_image, computer_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()