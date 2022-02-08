import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('First Game')
clock = pygame.time.Clock()

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky_surface = pygame.image.load('graphics/Sky.png').convert() #converting the image to something more efficient for pygame. 
ground_surface = pygame.image.load('graphics/ground.png').convert()

score_surface = test_font.render("Running Man", False, 'Black') #render takes three arguments: the text to display, whether you want anti-aliasing, and the color of the font
score_rect = score_surface.get_rect(center = (400, 50))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha() #convert_alpha to remove weird image frame around the snail
snail_rect = snail_surface.get_rect(midbottom = (600, 300))

player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80, 300)) #takes a surface, then draws a rectangle around it and maps it to a location. 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #blit stands for Block Image Transfer - fancy way of saying to put one surface on another surface. This is placing the test_surface that we've created onto the display screen we've created. The coordinates here are important. Unlike with a traditional x,y axis in math, the 0,0 coordinate represents the top left corner of the display screen (screen).

    screen.blit(sky_surface, (0,0)) # The precedence of the blit function matters in terms of z-index. So, the ground_surface will sit on top of the sky_surface since it is called second. 
    screen.blit(ground_surface, (0, 300))
    pygame.draw.rect(screen, 'Pink', score_rect) # uses the draw() method to draw a shape, in this instance, a rectangle.
    pygame.draw.rect(screen, 'Pink', score_rect, 10) # duplicated the draw method to add some padding to the rectangle
    screen.blit(score_surface, score_rect)
    screen.blit(player_surface, player_rect)
    screen.blit(snail_surface, snail_rect)
    snail_rect.x -= 4 # How we are moving any rectangle in the game. In this instance, the snail is moving to the right 4 units 60 times a second
    if snail_rect.right <= 0: snail_rect.x = 800 # conditional to control the flow of the snail encounter. Resets the snail after it runs off screen to create a continuous loop.        



    if player_rect.colliderect(snail_rect): 
        # print('ouch!')
        pass

    mouse_point = pygame.mouse.get_pos() # gets the coordinates of the mouse
    if player_rect.collidepoint(mouse_point): # checks if the mouse's coordinates have collided with the player; collidepoint() method takes x,y arguments.
        # print('collision!')
        pass

    pygame.display.update()
    clock.tick(60) #sets a cap on how often our while loop can iterate. This controls the framerate of our game