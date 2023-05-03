import pygame
import math
import random

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 793



WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("the-game")


SCORE = 0 
font = pygame.font.SysFont('arial', 24)

# layer image load
layer_list = []
for i in range(0, 12):
    layer_list.append(pygame.image.load("layers\L-" + str(i) + ".png").convert_alpha())
bg_width = layer_list[0].get_width()

# Parallax  variables
# num of images we need to draw at a given time per layer to fill the whole window
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

layer_scroll_velocities = [0, 0.1, 0.2, 0.25, 0.3, 0.35, 0.55, 0.7, 0.8, 0.8, 1, 1]
scrolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
vel = 1

# Layer drawer
def drawLayer(image, scrolled_by, speed_modifier):
    for i in range(tiles):
        WIN.blit(image, (bg_width * i + scrolled_by, 0))

    scrolled_by -= vel * speed_modifier
    # reset Scroll if 793 px i.e, 1 image is scrolled 
    if abs(scrolled_by) >= bg_width:
        scrolled_by = 0
    return scrolled_by


max_vel = 8
acceleration = 0.2
def lerp(lerp_from, lerp_to, t):
    return lerp_from + t * (lerp_to - lerp_from)


walk_list = [pygame.image.load("sprite\walk_0.png").convert_alpha(),
             pygame.image.load("sprite\walk_1.png").convert_alpha(),
             pygame.image.load("sprite\walk_2.png").convert_alpha(),
             pygame.image.load("sprite\walk_3.png").convert_alpha(),
             pygame.image.load("sprite\walk_4.png").convert_alpha(),
             pygame.image.load("sprite\walk_5.png").convert_alpha(),
             pygame.image.load("sprite\walk_6.png").convert_alpha(),
             pygame.image.load("sprite\walk_7.png").convert_alpha(),
            ]
anim_index = 0
idleUp_list = [pygame.image.load("sprite\idleUp_0.png").convert_alpha(),
             pygame.image.load("sprite\idleUp_1.png").convert_alpha(),
             pygame.image.load("sprite\idleUp_2.png").convert_alpha(),
             pygame.image.load("sprite\idleUp_3.png").convert_alpha(),
             pygame.image.load("sprite\idleUp_4.png").convert_alpha(),
             pygame.image.load("sprite\idleUp_5.png").convert_alpha(),
             pygame.image.load("sprite\idleUp_6.png").convert_alpha(),
             pygame.image.load("sprite\idleUp_7.png").convert_alpha(),
            ]
sprite_list = [ walk_list , idleUp_list]
sprite_index = 1

def drawSprite(image, curr_index, list_length, speed):
    WIN.blit(image,(x_pos, y_pos))
    if curr_index >= list_length:
        curr_index = 0
    else: 
        curr_index +=1 / speed
    return curr_index

# draw a transparent rectangle to work as a collider 
def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


coin_img = pygame.image.load("coins/gold_0.png").convert_alpha()
coin_width, coin_height = coin_img.get_size()

class Coin:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self):
        WIN.blit(self.image, (self.x, self.y))

    def move(self):
        self.x -= vel

    def is_off_screen(self):
        return self.x < 0
# Create a list to hold all the coins
coins = []


spawn_delay = 4000  # ms between spawns
last_spawn_time = pygame.time.get_ticks() - spawn_delay

# sprite variables 
x_pos = 100
y_pos = 473  
# 473 coz  793 - 64 - 256 
# 793 height of each layer 
# 64 pixels is height grass platfrom  
# 26 is the resolution of each sprite 

isJump = False
jump_count = 10

special_rect = pygame.Rect(200, y_pos, coin_width, coin_height)


run = True
while run:

    clock.tick(FPS)
    # key inputs 
    keys = pygame.key.get_pressed()

    # scroll Controller 
    if keys[pygame.K_RIGHT]:
        if vel < max_vel:
            sprite_index = 0
            # vel = max_vel
            vel = lerp(vel, max_vel, acceleration)
    else:
        sprite_index = 1
        if vel > 0:
            # vel = 0 
            vel = lerp(vel, 0, acceleration)

    # layers Draw when the velocity is > 0 
    if vel > 0:
        # SCORE += 1
        for i in range(0, len(layer_list)):
            scrolls[i] = drawLayer(layer_list[i], scrolls[i], layer_scroll_velocities[i])
    
    # coin draw 

    current_time = pygame.time.get_ticks()
    # Spawn a new coin if enough time has passed
    if current_time - last_spawn_time > spawn_delay + random.randint(0, 1000):
        y = random.choice([552, 652 ])
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
    
    draw_rect_alpha(WIN, (255, 0, 0, 0), special_rect)
    anim_index = drawSprite(sprite_list[sprite_index][math.floor(anim_index)], anim_index, len(walk_list)-1, 10)
    # sprite collider rect near face of the cat has dimension of the coin not needed
    special_rect = pygame.Rect(216, y_pos+168, coin_width, coin_height)

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
    score_text = font.render("Score: {}".format(SCORE), True, (0, 0, 0))
    WIN.blit(score_text, (10, 10))

    # Quit 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
