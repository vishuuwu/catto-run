#parllax with  lerp and character jump

import pygame
import math
import random

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 793
SCORE = 0 
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("the-game")


# Layer drawer
def drawLayer(image, scroll, speed_modifier):
    for i in range(tiles):
        win.blit(image, (bg_width * i + scroll, 0))

    scroll -= vel * speed_modifier
    # resetScroll
    if abs(scroll) >= bg_width:
        scroll = 0
    return scroll

def lerp(lerp_from, lerp_to, t):
    return lerp_from + t * (lerp_to - lerp_from)


def drawSprite(image, index, list_length, speed):
    win.blit(image,(x_pos, y_pos))
    if index >= list_length:
        index = 0
    else: 
        index +=1 / speed
    return index

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)



# Load the image
layer_list = []
for i in range(0, 12):
    layer_list.append(pygame.image.load("layers\L-" + str(i) + ".png").convert_alpha())
bg_width = layer_list[0].get_width()

walk_list = [pygame.image.load("sprite\walk_0.png").convert_alpha(),
             pygame.image.load("sprite\walk_1.png").convert_alpha(),
             pygame.image.load("sprite\walk_2.png").convert_alpha(),
             pygame.image.load("sprite\walk_3.png").convert_alpha(),
             pygame.image.load("sprite\walk_4.png").convert_alpha(),
             pygame.image.load("sprite\walk_5.png").convert_alpha(),
             pygame.image.load("sprite\walk_6.png").convert_alpha(),
             pygame.image.load("sprite\walk_7.png").convert_alpha(),
            ]
walk_index = 0




coin_img = pygame.image.load("coins/gold_0.png").convert_alpha()
coin_width, coin_height = coin_img.get_size()

# Parallax  variables
scroll_velocities = [0, 0.1, 0.2, 0.25, 0.3, 0.35, 0.55, 0.7, 0.8, 0.8, 1, 1]
scrolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

# for the lerp
#vel = 0
max_vel = 8
acceleration = 0.2

# sprite variables 
x_pos = 100
y_pos = 473  # 793 - 64 - 256 
vel = 1
width, heigth = 32, 32
isJump = False
jump_count = 10
special_rect = pygame.Rect(200, y_pos, coin_width, coin_height)
# coin
coin_speed = 2
spawn_delay = 4000  # ms between spawns
last_spawn_time = pygame.time.get_ticks() - spawn_delay

class Coin:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self):
        win.blit(self.image, (self.x, self.y))

    def move(self):
        self.x -= vel

    def is_off_screen(self):
        return self.x < 0
# Create a list to hold all the coins
coins = []




run = True
while run:
    SCORE += 1
    # pygame.time.delay(100)
    clock.tick(FPS)
    #layers Draw
    if vel > 0:
        for i in range(0, len(layer_list)):
            scrolls[i] = drawLayer(layer_list[i], scrolls[i], scroll_velocities[i])
    
    #coin draw 
    # Spawn a new coin if enough time has passed
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > spawn_delay + random.randint(0, 1000):
        y = random.choice([592, 652 ])
        coins.append(Coin(SCREEN_WIDTH, y, coin_img))
        last_spawn_time = current_time

    # Move and draw the coins
    for coin in coins:
        coin.move()
        coin.draw()
        # Destroy the coin if it goes off the screen
        if coin.is_off_screen():
            coins.remove(coin)
        # Check for collision with special rectangle
        elif (special_rect.colliderect(pygame.Rect(coin.x, coin.y, coin_width, coin_height))):
            SCORE += 5
            coins.remove(coin)
    
    
    #character draw
    special_rect = pygame.Rect(216, y_pos+168, coin_width, coin_height)
    draw_rect_alpha(win, (255, 0, 0, 0), special_rect)
    walk_index = drawSprite(walk_list[math.floor(walk_index)], walk_index, len(walk_list)-1, 5)

    # coins_index = drawCoins(coins_list[math.floor(coins_index)], coins_index, len(coins_list)-1, 5)

    # Controller
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        if vel < max_vel:
            vel = lerp(vel, max_vel, acceleration)
    else:
        if vel > 0:
            vel = lerp(vel, 0, acceleration)

    #jump
    if not(isJump):
        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            isJump = True
    else: 
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            y_pos -= (jump_count ** 2 ) * 0.3 * neg
            jump_count -= 1
        else:
            isJump = False
            jump_count = 10

    # Event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
