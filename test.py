from tracemalloc import start
import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = game_font.render(f'Score: {current_time}', False, (64,64,64)) #render takes three arguments: the text to display, whether you want anti-aliasing, and the color of the font
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5 # moves obstacle to the left by 5 

            if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
            else: screen.blit(fly_surf, obstacle_rect)

            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100] # List comprehension to check that we're only copying every item in the list if the condition obstacle.x is greater than zero. Essentially, if the obstacle is on the screen.
        
        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    global player_surf, player_index

    # checks if the player if jumping, if yes, displays jump image
    if player_rect.bottom < 300: 
        player_surf = player_jump
    else: 
        # slowly increments between the list indices of the walk image list. This prevents a rapid transition between walk_1 at index 0 and walk_2 at index 1, making things look more natural
        player_index += 0.1
        # resets the index value if it becomes greater than 1; creates continuous motion
        if player_index >= len(player_walk):player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('First Game')
clock = pygame.time.Clock()
game_active = False
start_time = 0 # initialize the timer at zero 
score = 0

game_font = pygame.font.Font('font/Pixeltype.ttf', 50)

sky_surface = pygame.image.load('graphics/Sky.png').convert() #converting the image to something more efficient for pygame. 
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Obstacles
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha() #convert_alpha to remove weird image frame around the snail
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300)) #takes a surface, then draws a rectangle around it and maps it to a location. 
player_gravity = 0

# Pre-Game Screen
player_ready_surf = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_ready_surf = pygame.transform.rotozoom(player_ready_surf, 0, 2) # redefining player_ready_surf to be transformed at 0 degrees rotation and double the size
player_ready_rect = player_ready_surf.get_rect(center = (400, 200))

title_surf = game_font.render('Running Man', False, (64,64,64))
title_rect = title_surf.get_rect(center = (400, 50))

to_play_surf = game_font.render('Tap SPACEBAR to begin!', False, (64,64,64))
to_play_rect = to_play_surf.get_rect(center = (400, 350))

# Timer
obstacle_timer = pygame.USEREVENT + 1 # Add plus one to avoid conflict with built-in pygame events
pygame.time.set_timer(obstacle_timer, 1400)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300: # records a player action using the keyword via the event loop. 
                    player_gravity = -20

            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900,1100), 300)))
                else: 
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(900,1100), 210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            
            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

        else: 
            # snail_rect.x = 800
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:

        #blit stands for Block Image Transfer - fancy way of saying to put one surface on another surface. This is placing the test_surface that we've created onto the display screen we've created. The coordinates here are important. Unlike with a traditional x,y axis in math, the 0,0 coordinate represents the top left corner of the display screen (screen).
        screen.blit(sky_surface, (0,0)) # The precedence of the blit function matters in terms of z-index. So, the ground_surface will sit on top of the sky_surface since it is called second. 
        screen.blit(ground_surface, (0, 300))
        # pygame.draw.rect(screen, '#c0e8ec', score_rect) # uses the draw() method to draw a shape, in this instance, a rectangle.
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10) # duplicated the draw method to add some padding to the rectangle
        # screen.blit(score_surface, score_rect)
        score = display_score()

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)   

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list) # Continuously updates the obstacle_rect_list value with with iteration of the obstacle_movement function

        # Collisions
        game_active = collisions(player_rect, obstacle_rect_list)

        # screen.blit(snail_surface, snail_rect)
        # snail_rect.x -= 7 # How we are moving any rectangle in the game. In this instance, the snail is moving to the right 4 units 60 times a second
        # if snail_rect.right <= 0: snail_rect.x = 800 # conditional to control the flow of the snail encounter. Resets the snail after it runs off screen to create a continuous loop.        



        # if player_rect.colliderect(snail_rect): 
        #     game_active = False

        mouse_point = pygame.mouse.get_pos() # gets the coordinates of the mouse
        if player_rect.collidepoint(mouse_point): # checks if the mouse's coordinates have collided with the player; collidepoint() method takes x,y arguments.
            # print('collision!')
            pass

        # keys = pygame.key.get_pressed() # This is the second way to record a player action via the keyboard. The first is in the event loop above. 
        # if keys[pygame.K_SPACE]:
        #     print('jump')
    else:
        screen.fill((173, 216, 230))
        screen.blit(player_ready_surf, player_ready_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0

        screen.blit(title_surf, title_rect)
        last_score_surf = game_font.render(f'Last Score: {score}', False, (64,64,64))
        last_score_rect = last_score_surf.get_rect(center = (400, 100))

        screen.blit(last_score_surf, last_score_rect)
        screen.blit(to_play_surf, to_play_rect)

    pygame.display.update()
    clock.tick(60) #sets a cap on how often our while loop can iterate. This controls the framerate of our game