#Swordfish OOP

#Rewrite large portions of the code with Object-Oriented Programming to be more concise and understandable
#Also, figure out why it doesn't run correctly on Fedora would be good

#General game stuff
import os
os.environ['PYGAME_DETECT_AVX2'] = '1'
import pygame
import sys
import random

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

pygame.init()
pygame.font.init()

score = 0
font = pygame.font.Font(None, 35)

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
FPS = 60

numberx = [50, 700]
numbery = [50, 700]

#Background
background_image = pygame.image.load('background.png')
background_image = pygame.transform.scale(background_image, (750, 750))

#Swordfish
original_image = pygame.image.load('swordfish.png')
original_image = pygame.transform.scale(original_image, (100, 100))
swordfish_image = original_image.copy()
swordfish_rect = swordfish_image.get_rect()
swordfish_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
swordfish_speed = 5

swordfish_hitbox_rect = swordfish_rect.inflate(-60, -60) 
swordfish_hitbox_rect.center = swordfish_rect.center

swordfish_alive = True
let_you_see_the_score = 100000000

d1_straight = 25
d1_diag = 15

offsets1 = {
    0:   (d1_straight, 0),    # Right
    45:  (d1_diag, -d1_diag),  # Up-Right
    90:  (0, -d1_straight),   # Up
    135: (-d1_diag, -d1_diag), # Up-Left
    180: (-d1_straight, 0),   # Left
    225: (-d1_diag, d1_diag),  # Down-Left
    270: (0, d1_straight),    # Down
    315: (d1_diag, d1_diag)    # Down-Right
}

#Sword
sword_rect = pygame.Rect(0, 0, 30, 30)
d2_straight = -35
d2_diag = -25

offsets2 = {
    0:   (d2_straight, 0),    # Right
    45:  (d2_diag, -d2_diag),  # Up-Right
    90:  (0, -d2_straight),   # Up
    135: (-d2_diag, -d2_diag), # Up-Left
    180: (-d2_straight, 0),   # Left
    225: (-d2_diag, d2_diag),  # Down-Left
    270: (0, d2_straight),    # Down
    315: (d2_diag, d2_diag)    # Down-Right
}
current_angle = 0

#Shark
original_image2 = pygame.image.load('shark.png')
original_image2 = pygame.transform.scale(original_image2, (125, 125))
shark_image = original_image2.copy()
shark_rect = shark_image.get_rect()
shark_rect.center = (random.uniform(50, 700), random.uniform(50, 700))

shark_alive = True

velocity_x_shark = 0
velocity_y_shark = 0
change_direction_timer_shark = 0
change_direction_interval_shark = 60

shark_hitbox_rect = shark_rect.inflate(-50, -50)

class Fish(pygame.sprite.Sprite):
    def __init__(self, color, image, interval):
        super().__init__()

        self.raw_image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.raw_image, (75, 75))
        self.rect = self.image.get_rect()
        self.rect.center = (random.uniform(50, 700), random.uniform(50, 700))

        self.color = color
        self.interval = interval
        self.timer = 0
        self.alive = True
        self.hitbox = self.rect.inflate(-20, -20)

    def update(self, score):
        fish_speed = [-2, -1, 0, 1, 2,]
        if score >= 40:
            fish_speed = [-6, -5, -4, -3, -2, 0, 2, 3, 4, 5, 6]
        elif score >= 30:
            fish_speed = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        elif score >= 20:
            fish_speed = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
        else:
            fish_speed = [-3, -2, -1, 0, 1, 2, 3]

        self.timer +=1
        if self.timer >= self.interval:
            self.change_x = random.choice(fish_speed)
            self.change_y = random.choice(fish_speed)
            self.timer = 0

        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.left < -50 or self.rect.right > SCREEN_WIDTH:
            self.rect.x *= -2
        if self.rect.top < -50 or self.rect.bottom > SCREEN_WIDTH:
            self.rect.y *= -2

        if self.rect.y > 0 and self.rect.x == 0:
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.rect.y == 0 and self.rect.x > 0:
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.rect.y == 0 and self.rect.x < 0:
            self.image = pygame.transform.rotate(self.image, 0)
        elif self.rect.y < 0 and self.rect.x == 0:
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.rect.y > 0 and self.rect.x > 0:
            self.image = pygame.transform.rotate(self.image, 135)
        elif self.rect.y < 0 and self.rect.x < 0:
            self.image = pygame.transform.rotate(self.image, 315)
        elif self.rect.y > 0 and self.rect.x < 0:
            self.image = pygame.transform.rotate(self.image, 45)
        elif self.rect.y < 0 and self.rect.x > 0:
            self.image = pygame.transform.rotate(self.image, 225)
        elif self.rect.y == 0 and self.rect.x == 0:
            self.image = pygame.transform.rotate(self.image, 0)
        else:
            pass


fish_colors = [
    ("green", "green_fish.png")
    ("yellow", "yellow_fish.png")
    ("orange", "orange_fish.png")
    ("red", "red_fish.png")
]

all_fish = pygame.sprite.Group()

for color, img in fish_colors:
    new_fish = Fish(color, img, 60)
    all_fish.add(new_fish)

running = True
while running:
    #Just make the game run and stop
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    #Swordfish movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        swordfish_rect.y -= swordfish_speed
        swordfish_image = pygame.transform.rotate(original_image, 270)
        current_angle = 270
    if keys[pygame.K_DOWN]:
        swordfish_rect.y += swordfish_speed
        swordfish_image = pygame.transform.rotate(original_image, 90)
        current_angle = 90
    if keys[pygame.K_LEFT]:
        swordfish_rect.x -= swordfish_speed
        swordfish_image = pygame.transform.rotate(original_image, 0)
        current_angle = 0
    if keys[pygame.K_RIGHT]:
        swordfish_rect.x += swordfish_speed
        swordfish_image = pygame.transform.rotate(original_image, 180)
        current_angle = 180
    if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
        swordfish_image = pygame.transform.rotate(original_image, 225)
        current_angle = 225
    if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
        swordfish_image = pygame.transform.rotate(original_image, 135)
        current_angle = 135
    if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
        swordfish_image = pygame.transform.rotate(original_image, 45)
        current_angle = 45
    if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
        swordfish_image = pygame.transform.rotate(original_image, 315)
        current_angle = 315

    swordfish_rect.x = max(0, min(swordfish_rect.x, SCREEN_WIDTH - swordfish_rect.width))
    swordfish_rect.y = max(0, min(swordfish_rect.y, SCREEN_HEIGHT - swordfish_rect.height))
 
    #Hitbox movement with the swordfish
    off1_x, off1_y = offsets1[current_angle]
    off2_x, off2_y = offsets2[current_angle]

    swordfish_hitbox_rect.centerx = swordfish_rect.centerx + off1_x
    swordfish_hitbox_rect.centery = swordfish_rect.centery + off1_y
    sword_rect.centerx = swordfish_rect.centerx + off2_x
    sword_rect.centery = swordfish_rect.centery + off2_y

    #Shark movement
    shark_speed = [-2, -1, 0, 1, 2]
    if score >= 30:
        shark_speed = [-7, -6, -5, -4, 0, 4, 5, 6, 7]
    if score >= 25:
        shark_speed = [-6, -5, -4, -3, 0, 3, 4, 5, 6]
    if score >= 20:
        shark_speed = [-5, -4, -3, 0, 3, 4, 5]
    if score >= 15:
        shark_speed = [-5, -4, -3, -2, 0, 2, 3, 4, 5]
    if score >= 10:
        shark_speed = [-4, -3, -2, 0, 2, 3, 4]
    if score >= 5:
        shark_speed = [-3, -2, -1, 0, 1, 2, 3]

    change_direction_timer_shark +=1
    if change_direction_timer_shark >= change_direction_interval_shark:
        velocity_x_shark = random.choice(shark_speed)
        velocity_y_shark = random.choice(shark_speed)
        change_direction_timer_shark = 0
    
    shark_rect.x += velocity_x_shark
    shark_rect.y += velocity_y_shark

    if shark_rect.left < -50 or shark_rect.right > SCREEN_WIDTH:
        velocity_x_shark *= -1.5
    if shark_rect.top < -50 or shark_rect.bottom > SCREEN_WIDTH:
        velocity_y_shark *= -1.5

    if velocity_y_shark > 0 and velocity_x_shark == 0:
        shark_image = pygame.transform.rotate(original_image2, 90)
    if velocity_y_shark == 0 and velocity_x_shark > 0:
        shark_image = pygame.transform.rotate(original_image2, 180)
    if velocity_y_shark == 0 and velocity_x_shark < 0:
        shark_image = pygame.transform.rotate(original_image2, 0)
    if velocity_y_shark < 0 and velocity_x_shark == 0:
        shark_image = pygame.transform.rotate(original_image2, 270)
    if velocity_y_shark > 0 and velocity_x_shark > 0:
        shark_image = pygame.transform.rotate(original_image2, 135)
    if velocity_y_shark < 0 and velocity_x_shark < 0:
        shark_image = pygame.transform.rotate(original_image2, 315)
    if velocity_y_shark > 0 and velocity_x_shark < 0:
        shark_image = pygame.transform.rotate(original_image2, 45)
    if velocity_y_shark < 0 and velocity_x_shark > 0:
        shark_image = pygame.transform.rotate(original_image2, 225)
    if velocity_y_shark == 0 and velocity_x_shark == 0:
        shark_image = pygame.transform.rotate(original_image2, 0)

    #Fish movement
    all_fish.update(score)

    #Revive
    if shark_alive == False and current_time - respawn_time_shark > 3000:
        shark_alive = True
    if green_fish_alive == False and current_time - respawn_time_green > 20000:
        green_fish_alive = True
    if yellow_fish_alive == False and current_time - respawn_time_yellow > 20000:
        yellow_fish_alive = True
    if red_fish_alive == False and current_time - respawn_time_red > 20000:
        red_fish_alive = True
    if orange_fish_alive == False and current_time - respawn_time_orange > 20000:
        orange_fish_alive = True
    
    #Collisions
    if shark_alive == True and swordfish_alive == True and sword_rect.colliderect(shark_hitbox_rect):
        shark_alive = False
        respawn_time_shark = current_time
        score += 1
    if swordfish_hitbox_rect.colliderect(shark_hitbox_rect) and shark_alive == True:
        swordfish_alive = False
        let_you_see_the_score = current_time
    if current_time - let_you_see_the_score > 3000:
        pygame.quit()
    if green_fish_alive == True and swordfish_alive == True and sword_rect.colliderect(green_fish_hitbox_rect):
        green_fish_alive = False
        respawn_time_green = current_time
        score -= 1
    if yellow_fish_alive == True and swordfish_alive == True and sword_rect.colliderect(yellow_fish_hitbox_rect):
        yellow_fish_alive = False
        respawn_time_yellow = current_time
        score -= 2
    if red_fish_alive == True and swordfish_alive == True and sword_rect.colliderect(red_fish_hitbox_rect):
        red_fish_alive = False
        respawn_time_red = current_time
        score -= 3
    if orange_fish_alive == True and swordfish_alive == True and sword_rect.colliderect(orange_fish_hitbox_rect):
        orange_fish_alive = False
        respawn_time_orange = current_time
        score -= 4

    #Fish importance
    fish_status = [green_fish_alive, yellow_fish_alive, red_fish_alive, orange_fish_alive]
    if not any(fish_status):
        pygame.quit()

    #Actually render the game
    screen.blit(background_image, (0, 0))
    all_fish.draw(screen)

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()