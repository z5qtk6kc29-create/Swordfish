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

#General game stuff
import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
FPS = 60

numberx = [50, 700]
numbery = [50, 700]

#Swordfish
original_image = pygame.image.load('player_swordfish.png')
original_image = pygame.transform.scale(original_image, (100, 100))
player_image = original_image.copy()
player_rect = player_image.get_rect()
player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
player_speed = 5

#Shark
original_image2 = pygame.image.load('computer_shark.png')
original_image2 = pygame.transform.scale(original_image2, (125, 125))
computer_image = original_image2.copy()
computer_rect = computer_image.get_rect()
computer_rect.center = (random.uniform(50, 700), random.uniform(50, 700))

velocity_x_shark = 0
velocity_y_shark = 0
change_direction_timer_shark = 0
change_direction_interval_shark = 60

#Green Fish
original_image3 = pygame.image.load('green_fish.png')
original_image3 = pygame.transform.scale(original_image3, (75, 75))
green_fish_image = original_image3.copy()
green_fish_rect = green_fish_image.get_rect()
green_fish_rect.center = (random.uniform(50, 700), random.uniform(50, 700))

velocity_x_green = 0
velocity_y_green = 0
change_direction_timer_green = 0
change_direction_interval_green = 60

#Yellow Fish
original_image4 = pygame.image.load('yellow_fish.png')
original_image4 = pygame.transform.scale(original_image4, (75, 75))
yellow_fish_image = original_image4.copy()
yellow_fish_rect = yellow_fish_image.get_rect()
yellow_fish_rect.center = (random.uniform(50, 700), random.uniform(50, 700))

velocity_x_yellow = 0
velocity_y_yellow = 0
change_direction_timer_yellow = 0
change_direction_interval_yellow = 60

#Red Fish
original_image5 = pygame.image.load('red_fish.png')
original_image5 = pygame.transform.scale(original_image5, (75, 75))
red_fish_image = original_image5.copy()
red_fish_rect = red_fish_image.get_rect()
red_fish_rect.center = (random.uniform(50, 700), random.uniform(50, 700))

velocity_x_red = 0
velocity_y_red = 0
change_direction_timer_red = 0
change_direction_interval_red = 60

#Orange Fish
original_image6 = pygame.image.load('orange_fish.png')
original_image6 = pygame.transform.scale(original_image6, (75, 75))
orange_fish_image = original_image6.copy()
orange_fish_rect = orange_fish_image.get_rect()
orange_fish_rect.center = (random.uniform(50, 700), random.uniform(50, 700))

velocity_x_orange = 0
velocity_y_orange = 0
change_direction_timer_orange = 0
change_direction_interval_orange = 60

running = True
while running:
    #Just make the game run and stop
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    #Player movement
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

    player_rect.x = max(0, min(player_rect.x, SCREEN_WIDTH - player_rect.width))
    player_rect.y = max(0, min(player_rect.y, SCREEN_HEIGHT - player_rect.height))

    #Shark movement
    change_direction_timer_shark +=1
    if change_direction_timer_shark >= change_direction_interval_shark:
        velocity_x_shark = random.uniform(-4, 4)
        velocity_y_shark = random.uniform(-4, 4)
        change_direction_timer_shark = 0

    computer_rect.x += velocity_x_shark
    computer_rect.y += velocity_y_shark

    if computer_rect.left < -50 or computer_rect.right > SCREEN_WIDTH:
        velocity_x_shark *= -1.5
    if computer_rect.top < -50 or computer_rect.bottom > SCREEN_WIDTH:
        velocity_y_shark *= -1.5

    if velocity_y_shark > 0 and velocity_x_shark == 0:
        computer_image = pygame.transform.rotate(original_image2, 90)
    if velocity_y_shark == 0 and velocity_x_shark > 0:
        computer_image = pygame.transform.rotate(original_image2, 180)
    if velocity_y_shark == 0 and velocity_x_shark < 0:
        computer_image = pygame.transform.rotate(original_image2, 0)
    if velocity_y_shark < 0 and velocity_x_shark == 0:
        computer_image = pygame.transform.rotate(original_image2, 270)
    if velocity_y_shark > 0 and velocity_x_shark > 0:
        computer_image = pygame.transform.rotate(original_image2, 135)
    if velocity_y_shark < 0 and velocity_x_shark < 0:
        computer_image = pygame.transform.rotate(original_image2, 315)
    if velocity_y_shark > 0 and velocity_x_shark < 0:
        computer_image = pygame.transform.rotate(original_image2, 45)
    if velocity_y_shark < 0 and velocity_x_shark > 0:
        computer_image = pygame.transform.rotate(original_image2, 225)
    if velocity_y_shark == 0 and velocity_x_shark == 0:
        computer_image = pygame.transform.rotate(original_image2, 0)

    #Green fish specific movement
    change_direction_timer_green +=1
    if change_direction_timer_green >= change_direction_interval_green:
        velocity_x_green = random.uniform(-2, 2)
        velocity_y_green = random.uniform(-2, 2)
        change_direction_timer_green = 0

    green_fish_rect.x += velocity_x_green
    green_fish_rect.y += velocity_y_green

    if green_fish_rect.left < -50 or green_fish_rect.right > SCREEN_WIDTH:
        velocity_x_green *= -1.5
    if green_fish_rect.top < -50 or green_fish_rect.bottom > SCREEN_WIDTH:
        velocity_y_green *= -1.5

    if velocity_y_green > 0 and velocity_x_green == 0:
        green_fish_image = pygame.transform.rotate(original_image3, 90)
    if velocity_y_green == 0 and velocity_x_green > 0:
        green_fish_image = pygame.transform.rotate(original_image3, 180)
    if velocity_y_green == 0 and velocity_x_green < 0:
        green_fish_image = pygame.transform.rotate(original_image3, 0)
    if velocity_y_green < 0 and velocity_x_green == 0:
        green_fish_image = pygame.transform.rotate(original_image3, 270)
    if velocity_y_green > 0 and velocity_x_green > 0:
        green_fish_image = pygame.transform.rotate(original_image3, 135)
    if velocity_y_green < 0 and velocity_x_green < 0:
        green_fish_image = pygame.transform.rotate(original_image3, 315)
    if velocity_y_green > 0 and velocity_x_green < 0:
        green_fish_image = pygame.transform.rotate(original_image3, 45)
    if velocity_y_green < 0 and velocity_x_green > 0:
        green_fish_image = pygame.transform.rotate(original_image3, 225)
    if velocity_y_green == 0 and velocity_x_green == 0:
        green_fish_image = pygame.transform.rotate(original_image3, 0)

    #Yellow fish specific movement
    change_direction_timer_yellow +=1
    if change_direction_timer_yellow >= change_direction_interval_yellow:
        velocity_x_yellow = random.uniform(-2, 2)
        velocity_y_yellow = random.uniform(-2, 2)
        change_direction_timer_yellow = 0

    yellow_fish_rect.x += velocity_x_yellow
    yellow_fish_rect.y += velocity_y_yellow

    if yellow_fish_rect.left < -50 or yellow_fish_rect.right > SCREEN_WIDTH:
        velocity_x_yellow *= -1.5
    if yellow_fish_rect.top < -50 or yellow_fish_rect.bottom > SCREEN_WIDTH:
        velocity_y_yellow *= -1.5

    if velocity_y_yellow > 0 and velocity_x_yellow == 0:
        yellow_fish_image = pygame.transform.rotate(original_image4, 90)
    if velocity_y_yellow == 0 and velocity_x_yellow > 0:
        yellow_fish_image = pygame.transform.rotate(original_image4, 180)
    if velocity_y_yellow == 0 and velocity_x_yellow < 0:
        yellow_fish_image = pygame.transform.rotate(original_image4, 0)
    if velocity_y_yellow < 0 and velocity_x_yellow == 0:
        yellow_fish_image = pygame.transform.rotate(original_image4, 270)
    if velocity_y_yellow > 0 and velocity_x_yellow > 0:
        yellow_fish_image = pygame.transform.rotate(original_image4, 135)
    if velocity_y_yellow < 0 and velocity_x_yellow < 0:
        yellow_fish_image = pygame.transform.rotate(original_image4, 315)
    if velocity_y_yellow > 0 and velocity_x_yellow < 0:
        yellow_fish_image = pygame.transform.rotate(original_image4, 45)
    if velocity_y_yellow < 0 and velocity_x_yellow > 0:
        yellow_fish_image = pygame.transform.rotate(original_image4, 225)
    if velocity_y_yellow == 0 and velocity_x_yellow == 0:
        yellow_fish_image = pygame.transform.rotate(original_image4, 0)

    #Red fish specific movement
    change_direction_timer_red +=1
    if change_direction_timer_red >= change_direction_interval_red:
        velocity_x_red = random.uniform(-2, 2)
        velocity_y_red = random.uniform(-2, 2)
        change_direction_timer_red = 0

    red_fish_rect.x += velocity_x_red
    red_fish_rect.y += velocity_y_red

    if red_fish_rect.left < -50 or red_fish_rect.right > SCREEN_WIDTH:
        velocity_x_red *= -1.5
    if red_fish_rect.top < -50 or red_fish_rect.bottom > SCREEN_WIDTH:
        velocity_y_red *= -1.5

    if velocity_y_red > 0 and velocity_x_red == 0:
        red_fish_image = pygame.transform.rotate(original_image5, 90)
    if velocity_y_red == 0 and velocity_x_red > 0:
        red_fish_image = pygame.transform.rotate(original_image5, 180)
    if velocity_y_red == 0 and velocity_x_red < 0:
        red_fish_image = pygame.transform.rotate(original_image5, 0)
    if velocity_y_red < 0 and velocity_x_red == 0:
        red_fish_image = pygame.transform.rotate(original_image5, 270)
    if velocity_y_red > 0 and velocity_x_red > 0:
        red_fish_image = pygame.transform.rotate(original_image5, 135)
    if velocity_y_red < 0 and velocity_x_red < 0:
        red_fish_image = pygame.transform.rotate(original_image5, 315)
    if velocity_y_red > 0 and velocity_x_red < 0:
        red_fish_image = pygame.transform.rotate(original_image5, 45)
    if velocity_y_red < 0 and velocity_x_red > 0:
        red_fish_image = pygame.transform.rotate(original_image5, 225)
    if velocity_y_red == 0 and velocity_x_red == 0:
        red_fish_image = pygame.transform.rotate(original_image5, 0)

    #Orange fish specific movement
    change_direction_timer_orange +=1
    if change_direction_timer_orange >= change_direction_interval_orange:
        velocity_x_orange = random.uniform(-2, 2)
        velocity_y_orange = random.uniform(-2, 2)
        change_direction_timer_orange = 0

    orange_fish_rect.x += velocity_x_orange
    orange_fish_rect.y += velocity_y_orange

    if orange_fish_rect.left < -50 or orange_fish_rect.right > SCREEN_WIDTH:
        velocity_x_orange *= -1.5
    if orange_fish_rect.top < -50 or orange_fish_rect.bottom > SCREEN_WIDTH:
        velocity_y_orange *= -1.5

    if velocity_y_orange > 0 and velocity_x_orange == 0:
        orange_fish_image = pygame.transform.rotate(original_image6, 90)
    if velocity_y_orange == 0 and velocity_x_orange > 0:
        orange_fish_image = pygame.transform.rotate(original_image6, 180)
    if velocity_y_orange == 0 and velocity_x_orange < 0:
        orange_fish_image = pygame.transform.rotate(original_image6, 0)
    if velocity_y_orange < 0 and velocity_x_orange == 0:
        orange_fish_image = pygame.transform.rotate(original_image6, 270)
    if velocity_y_orange > 0 and velocity_x_orange > 0:
        orange_fish_image = pygame.transform.rotate(original_image6, 135)
    if velocity_y_orange < 0 and velocity_x_orange < 0:
        orange_fish_image = pygame.transform.rotate(original_image6, 315)
    if velocity_y_orange > 0 and velocity_x_orange < 0:
        orange_fish_image = pygame.transform.rotate(original_image6, 45)
    if velocity_y_orange < 0 and velocity_x_orange > 0:
        orange_fish_image = pygame.transform.rotate(original_image6, 225)
    if velocity_y_orange == 0 and velocity_x_orange == 0:
        orange_fish_image = pygame.transform.rotate(original_image6, 0)

    #Actually render the game
    screen.fill((80, 140, 160))
    screen.blit(player_image, player_rect)
    screen.blit(computer_image, computer_rect)
    screen.blit(green_fish_image, green_fish_rect)
    screen.blit(yellow_fish_image, yellow_fish_rect)
    screen.blit(red_fish_image, red_fish_rect)
    screen.blit(orange_fish_image, orange_fish_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()