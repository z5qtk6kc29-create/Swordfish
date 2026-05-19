#Swordfish OOP

#Rewrite large portions of the code with Object-Oriented Programming to be more concise and understandable #very not done
#Also, figure out why it doesn't run correctly on Fedora would be good #done

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

#Background
background_image = pygame.image.load('background.png')
background_image = pygame.transform.scale(background_image, (750, 750))

class Swordfish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Load and scale image
        self.raw_image = pygame.image.load('swordfish.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.raw_image, (100, 100))
        self.image = self.original_image.copy()
        
        # Main Position Rect
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.alive = True
        self.current_angle = 0
        
        # --- Hitboxes ---
        # Body Hitbox (Inflated to be smaller than the image)
        self.hitbox = self.rect.inflate(-60, -60)
        
        # Sword Hitbox (Separate tracking rectangle)
        self.sword_hitbox = pygame.Rect(0, 0, 30, 30)
        
        # Your exact dictionary offsets
        d1_straight = 25
        d1_diag = 15
        self.offsets1 = {
            0: (d1_straight, 0), 45: (d1_diag, -d1_diag), 90: (0, -d1_straight),
            135: (-d1_diag, -d1_diag), 180: (-d1_straight, 0), 225: (-d1_diag, d1_diag),
            270: (0, d1_straight), 315: (d1_diag, d1_diag)
        }

        d2_straight = -35
        d2_diag = -25
        self.offsets2 = {
            0: (d2_straight, 0), 45: (d2_diag, -d2_diag), 90: (0, -d2_straight),
            135: (-d2_diag, -d2_diag), 180: (-d2_straight, 0), 225: (-d2_diag, d2_diag),
            270: (0, d2_straight), 315: (d2_diag, d2_diag)
        }

    def update(self):
        # 1. Handle Keyboard Inputs
        keys = pygame.key.get_pressed()
        move_x = 0
        move_y = 0
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:    move_y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  move_y = self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  move_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: move_x = self.speed
        
        # Move the main tracking position
        self.rect.x += move_x
        self.rect.y += move_y
        
        # 2. Determine Facing Angle based on movement direction
        if move_x > 0 and move_y == 0:    self.current_angle = 180
        elif move_x > 0 and move_y < 0:  self.current_angle = 225
        elif move_x == 0 and move_y < 0:  self.current_angle = 270
        elif move_x < 0 and move_y < 0:  self.current_angle = 315
        elif move_x < 0 and move_y == 0:  self.current_angle = 0
        elif move_x < 0 and move_y > 0:  self.current_angle = 45
        elif move_x == 0 and move_y > 0:  self.current_angle = 90
        elif move_x > 0 and move_y > 0:  self.current_angle = 135

        # Rotate visual sprite image crisp and clean
        self.image = pygame.transform.rotate(self.original_image, self.current_angle)
        
        # 3. Synchronize all internal Hitboxes using your offsets
        self.hitbox.center = self.rect.center
        
        # Update your sword_hitbox position based on current angle offsets
        off1 = self.offsets1[self.current_angle]
        off2 = self.offsets2[self.current_angle]
        
        self.sword_hitbox.centerx = self.rect.centerx + off1[0] + off2[0]
        self.sword_hitbox.centery = self.rect.centery + off1[1] + off2[1]

player = Swordfish()
player_group = pygame.sprite.GroupSingle(player)

#Shark
class Shark(pygame.sprite.Sprite):
    def __init__(self, image, interval):
        super().__init__()

        self.raw_image = pygame.image.load(image).convert_alpha()
        self.original_image = pygame.transform.scale(self.raw_image, (125, 125))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (random.uniform(50, 700), random.uniform(50, 700))
        self.interval = interval
        self.timer = 0
        self.time = 0
        self.alive = True
        self.hitbox = self.rect.inflate(-50, -50)
        self.change_x = 0
        self.change_y = 0
        self.current_angle = 0

    def update(self, score):
        if score >= 30: shark_speed = [-7, -6, -5, -4, 0, 4, 5, 6, 7]
        if score >= 25: shark_speed = [-6, -5, -4, -3, 0, 3, 4, 5, 6]
        if score >= 20: shark_speed = [-5, -4, -3, 0, 3, 4, 5]
        if score >= 15: shark_speed = [-5, -4, -3, -2, 0, 2, 3, 4, 5]
        if score >= 10: shark_speed = [-4, -3, -2, 0, 2, 3, 4]
        if score >= 5: shark_speed = [-3, -2, -1, 0, 1, 2, 3]
        else: shark_speed = [-2, -1, 0, 1, 2]

        self.timer +=1
        if self.timer >= self.interval:
            self.change_x = random.choice(shark_speed)
            self.change_y = random.choice(shark_speed)
            self.timer = 0

        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.left < -50 or self.rect.right > SCREEN_WIDTH:
            self.change_x *= -1
        if self.rect.top < -50 or self.rect.bottom > SCREEN_WIDTH:
            self.change_y *= -1

        if self.change_y > 0 and self.change_x == 0: self.current_angle = 90
        elif self.change_y == 0 and self.change_x > 0: self.current_angle = 180
        elif self.change_y == 0 and self.change_x < 0: self.current_angle = 0
        elif self.change_y < 0 and self.change_x == 0: self.current_angle = 270
        elif self.change_y > 0 and self.change_x > 0: self.current_angle = 135
        elif self.change_y < 0 and self.change_x < 0: self.current_angle = 315
        elif self.change_y > 0 and self.change_x < 0: self.current_angle = 45
        elif self.change_y < 0 and self.change_x > 0: self.current_angle = 225
        elif self.change_y == 0 and self.change_x == 0: self.current_angle = 0

        self.image = pygame.transform.rotate(self.original_image, self.current_angle)

shark = Shark("shark.png", 60)
shark_group = pygame.sprite.GroupSingle(shark)

class Fish(pygame.sprite.Sprite):
    def __init__(self, color, image, interval):
        super().__init__()

        self.raw_image = pygame.image.load(image).convert_alpha()
        self.original_image = pygame.transform.scale(self.raw_image, (75, 75))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (random.uniform(50, 700), random.uniform(50, 700))
        self.color = color
        self.interval = interval
        self.timer = 0
        self.time = 0
        self.alive = True
        self.hitbox = self.rect.inflate(-20, -20)
        self.change_x = 0
        self.change_y = 0
        self.current_angle = 0

    def update(self, score):
        if score >= 40: fish_speed = [-6, -5, -4, -3, -2, 0, 2, 3, 4, 5, 6]
        elif score >= 30: fish_speed = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        elif score >= 20: fish_speed = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
        else: fish_speed = [-2, -1, 0, 1, 2,]

        self.timer +=1
        if self.timer >= self.interval:
            self.change_x = random.choice(fish_speed)
            self.change_y = random.choice(fish_speed)
            self.timer = 0

        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.left < -50 or self.rect.right > SCREEN_WIDTH:
            self.change_x *= -1
        if self.rect.top < -50 or self.rect.bottom > SCREEN_WIDTH:
            self.change_y *= -1

        if self.change_y > 0 and self.change_x == 0: self.current_angle = 90
        elif self.change_y == 0 and self.change_x > 0: self.current_angle = 180
        elif self.change_y == 0 and self.change_x < 0: self.current_angle = 0
        elif self.change_y < 0 and self.change_x == 0: self.current_angle = 270
        elif self.change_y > 0 and self.change_x > 0: self.current_angle = 135
        elif self.change_y < 0 and self.change_x < 0: self.current_angle = 315
        elif self.change_y > 0 and self.change_x < 0: self.current_angle = 45
        elif self.change_y < 0 and self.change_x > 0: self.current_angle = 225
        elif self.change_y == 0 and self.change_x == 0: self.current_angle = 0

        self.image = pygame.transform.rotate(self.original_image, self.current_angle)

fish_colors = [
    ("green", "green_fish.png"),
    ("yellow", "yellow_fish.png"),
    ("orange", "orange_fish.png"),
    ("red", "red_fish.png")
]

all_fish = pygame.sprite.Group()
master_fish_list = []

for color, img in fish_colors:
    new_fish = Fish(color, img, 60)
    all_fish.add(new_fish)
    master_fish_list.append(new_fish)

running = True
while running:
    #Just make the game run and stop
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    #Fish movement
    player_group.update()
    all_fish.update(score)
    shark_group.update(score)

    #Revive
    if shark.alive == False and current_time - shark.time > 3000:
        shark.alive = True
    
    for fish in master_fish_list:
        if not fish.alive == True and current_time - fish.time > 20000:
                fish.alive = True
                all_fish.add(fish)
    
    #Collisions
    if shark.alive == True and player.alive == True and player.sword_hitbox.colliderect(shark.hitbox):
        shark.kill()
        shark.time = current_time
        score += 1
    if player.hitbox.colliderect(shark.hitbox) and shark.alive == True:
        player.kill()
        running = False
    for fish in all_fish:
        if fish.alive == True and player.alive == True and player.hitbox.colliderect(fish.hitbox):
            fish.alive = False
            fish.kill()
            fish.time = current_time
            score -= random.choice([1,2,3,4])

    #Fish importance
    if len(all_fish) == 0 and shark.alive == True:
        running = False

    #Actually render the game
    screen.blit(background_image, (0, 0))
    for fish in all_fish:
        if fish.alive: screen.blit(fish.image, fish.rect)
    if shark.alive: 
        screen.blit(shark.image, shark.rect)
    
    player_group.draw(screen)

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

running = False
sys.exit()