# loading and draw image
import pygame
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

run = True
while run:

    for i in layer_list:
        WIN.blit(i, (0, 0))

    
    score_text = font.render("Score: {}".format(SCORE), True, (0, 0, 0))
    WIN.blit(score_text, (10, 10)) 
    pygame.display.update()

    # Quit 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()