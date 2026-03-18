#Swordfish Beta

#I would like this game to maybe have inspiration from wordle and my work on it, but be its own game outright.

#I think that I would like to use pygame on this one somehow

import pygame

pygame.init()

screen = pygame.display.set_mode((750, 750))
clock = pygame.time.Clock()
running = True

player_pos = pygame.Vector2(screen.get_width() /2, screen.get_height() / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((80, 140, 160))

    pygame.display.flip()
    
    clock.tick(60)

pygame.quit
