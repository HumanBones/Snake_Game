import pygame
from pygame.locals import *
import random

pygame.init()

screen_widht = 800
screen_hight = 600

food_size_x = 30
food_size_y = 30

screen_size = (screen_widht, screen_hight)

offset = 5

snake_list = []

game_font = pygame.font.Font('Font/Pixellari.ttf', 72)
score_font = pygame.font.Font('Font/Pixellari.ttf', 32)

clock = pygame.time.Clock()

red = (150,0,0)
blue = (0,0,255)
green = (0,150,0)
white = (255, 255, 255)

pygame.display.set_caption("I'm a Ssssnake")
window_surface = pygame.display.set_mode(screen_size)

background = pygame.Surface(screen_size)


def score_disp(score):
    text = score_font.render('Score: ' + str(score), True, white)
    window_surface.blit(text, [0, 0])


def txt_obj(msg,color,use):
    if use == 'score':
        txt_surf = score_font.render(msg, True, color)
    elif use == 'game':
        txt_surf = game_font.render(msg, True, color)
    return txt_surf, txt_surf.get_rect()

def msg_to_display(msg,color,offset_y=0,use='game'):
    txt_surf , txt_rect = txt_obj(msg,color,use)
    txt_rect.center = (round(screen_widht / 2)), round((screen_hight / 2) + offset_y)
    background.blit(txt_surf, txt_rect)


def game_loop():

    #Vars
    widht = 30
    hight = 30

    x = 400
    y = 300

    speed = 5
    dir_x = -1
    dir_y = 0
    
    snake_len = 1
    score = 0
    

    is_running = True
    game_over = False
    show_score = True
    food_pos = spawn_food()
    while is_running:

        #Exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.KEYDOWN:
                ###Event keys
                
                #Basic movment
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    dir_x = 1
                    dir_y = 0
                    
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    dir_x = -1
                    dir_y = 0

                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    dir_y = -1
                    dir_x = 0

                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    dir_y = 1
                    dir_x = 0

                #Quit
                elif event.key == pygame.K_ESCAPE:
                    is_running = False
                #Restart
                elif event.key == pygame.K_r:
                    snake_list.clear()
                    snake_len = 0
                    score = 0
                    game_loop()
                    
                elif event.key == pygame.K_SPACE:
                    food_pos = spawn_food()

        #Screen Overlaping
        if x > screen_widht:
            x = 0
        elif x < 0:
            x = screen_widht
        
        if y > screen_hight:
            y = 0
        elif y < 0:
            y = screen_hight

        #Doing movment
        x += dir_x * speed
        y += dir_y * speed
            

        background.fill(pygame.Color('#000000'))
        
        #Draw food
        food = pygame.draw.rect(background, green, (food_pos[0], food_pos[1], food_size_x, food_size_y))

        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)

        if len(snake_list) > snake_len:
            del snake_list[0]

        for sgm in snake_list[:-1]:
            if sgm == snake_head:
                game_over = True

        if game_over:
            show_score = False
            snake_list.clear()
            snake_len = 0
            score = 0
            msg_to_display('Game Over', white, -100, 'game')

        else:
            player = snake(snake_list,widht,hight)
        
        window_surface.blit(background, (0, 0))
        
        if show_score:
            score_disp(score)
        
        pygame.display.update() #Update

        #Collision
        if x > food_pos[0] and x < food_pos[0] + food_size_x + offset or x + widht > food_pos[0] + offset and x + widht < food_pos[0] + food_size_x + offset:
            if y > food_pos[1] and y < food_pos[1] + food_size_y + offset or y + hight + offset > food_pos[1] + offset and y + hight + offset < food_pos[1] + food_size_y + offset:
                food_pos = spawn_food()
                snake_len += 1
                score += 1
                
        clock.tick(60) #FPS
    pygame.quit()
    quit()

#Draw player
def snake(snake_list,w,h):
    for elem in snake_list:
        pygame.draw.rect(background, red, (elem[0], elem[1], w, h))


#Spawn food
def spawn_food():
    food_x = round(random.randrange(0 + offset, screen_widht - offset))
    food_y = round(random.randrange(0 + offset, screen_hight - offset))
    
    food_pos = [food_x,food_y]

    return food_pos

game_loop()
