# adds parallax effect

import pygame
import math


pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 793

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catto-run")

SCORE = 0 
font = pygame.font.SysFont('arial', 24)

# layer image load
layer_list = []
for i in range(0, 12):
    layer_list.append(pygame.image.load("layers/L-" + str(i) + ".png").convert_alpha())
bg_width = layer_list[0].get_width()

# Parallax  variables
# num of images we need to draw at a given time per layer to fill the whole window
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

layer_scroll_velocities = [0, 0.1, 0.2, 0.25, 0.3, 0.35, 0.55, 0.7, 0.8, 0.8, 1, 1]
scrolls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
vel = 1
max_vel = 8
# Layer drawer
def drawLayer(image, scrolled_by, speed_modifier):
    for i in range(tiles):
        WIN.blit(image, (bg_width * i + scrolled_by, 0))

    scrolled_by -= vel * speed_modifier
    # reset Scroll if 793 px i.e, 1 image is scrolled 
    if abs(scrolled_by) >= bg_width:
        scrolled_by = 0
    return scrolled_by

run = True
while run:
    clock.tick(FPS)

    keys = pygame.key.get_pressed()

    # layers Draw 
    for i in range(0, len(layer_list)):
            scrolls[i] = drawLayer(layer_list[i], scrolls[i], layer_scroll_velocities[i])

    # scroll Controller 
    if keys[pygame.K_RIGHT]:
        if vel < max_vel:
            # sprite_index = 0
            vel = max_vel
            # vel = lerp(vel, max_vel, acceleration)
    else:
        # sprite_index = 1
        if vel > 0:
            vel = 0 
            # vel = lerp(vel, 0, acceleration)

    
    
    score_text = font.render("Score: {}".format(SCORE), True, (0, 0, 0))
    WIN.blit(score_text, (10, 10)) 
    pygame.display.update()

    # Quit 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()