import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('First Game')
clock = pygame.time.Clock()

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky_surface = pygame.image.load('graphics/Sky.png').convert() #converting the image to something more efficient for pygame. 
ground_surface = pygame.image.load('graphics/ground.png').convert()
text_surface = test_font.render("Running Man", False, 'Black') #render takes three arguments: the text to display, whether you want anti-aliasing, and the color of the font
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha() #convert_alpha to remove weird image frame around the snail
snail_x_pos = 600

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #blit stands for Block Image Transfer - fancy way of saying to put one surface on another surface. This is placing the test_surface that we've created onto the display screen we've created. The coordinates here are important. Unlike with a traditional x,y axis in math, the 0,0 coordinate represents the top left corner of the display screen (screen).

    screen.blit(sky_surface, (0,0)) # The precedence of the blit function matters in terms of z-index. So, the ground_surface will sit on top of the sky_surface since it is called second. 
    screen.blit(ground_surface, (0, 300))
    screen.blit(text_surface, (300, 50))
    screen.blit(snail_surface, (snail_x_pos, 265))
    if snail_x_pos > -55:
        snail_x_pos -= 3
    else:
        snail_x_pos = 855
        

    pygame.display.update()
    clock.tick(60) #sets a cap on how often our while loop can iterate. This controls the framerate of our game