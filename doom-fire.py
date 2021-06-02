import pygame, sys
from random import choice, seed, randint
from pygame.locals import *
from pygame.time import delay

#seed(2)
pygame.init()
pygame.display.set_caption("Doom Fire")
clock = pygame.time.Clock()

black_color = (0, 0, 0)
white_color = (255, 255, 255)
grey_color = (25, 25, 25)
red_color = (255, 100, 100)
teal_color = (100, 255, 255)
green_color = (100, 255, 100)

FPS = 60
screen_w, screen_h = 256, 256
window_w, window_h = 512, 512
screen = pygame.Surface((screen_w, screen_h))
window = pygame.display.set_mode((window_w, window_h))


fire_on = True
burn = False
wind_direction = False
blow_wind = False
wind_intensity = 3
it = 0

def start_fire():
    global fireBuffer

    for i in range(n_pixels - screen_w, n_pixels):
        fireBuffer[i] = 36


def stop_fire():
    global fireBuffer

    for i in range(n_pixels - screen_w, n_pixels):
        fireBuffer[i] = 0
    
    # explosion (?)
    #for i in range(n_pixels):
    #    fireBuffer[i] = 35

def update_fire():

    global fireBuffer

    for row in range(screen_w - 1, 0, -1):
        for col in range(screen_h - 1, -1, -1):

            pos = row * screen_w + col

            if fireBuffer[pos] >= 0:
                
                # vortex ?
                #decay = randint(-1, 2)

                decay = randint(0, 1)

                new_val = fireBuffer[pos] - decay
                if new_val < 0: new_val = 0

                # wind force
                wind = 1
                if blow_wind:
                    wind = wind_direction
                    if wind_direction:
                        wind = - wind_intensity
                

                new_pos = pos - screen_w - decay + wind
                if new_pos < 0: continue

                fireBuffer[new_pos] = new_val 
    global it    
    pygame.image.save(window,"gif/" +  str(it) + "_iteration.jpeg")
    it += 1
    

def pixel(surface, pos, color):
    surface.set_at(pos, color)


def draw_screen(surface):
    for row in range(screen_w - 1, -1, -1):
        for col in range(screen_h - 1, -1, -1):
            pos = row * screen_w + col
            index = fireBuffer[pos]
            pixel(surface, (col, row), fireColorsPalette[index])
            

fireColorsPalette = [(7, 7, 7), (31, 7, 7), (47, 15, 7), (71, 15, 7), (87,23,7), (103, 31,7), (119, 31, 7), (143, 39, 7),
                     (159,47,7), (175, 63, 7), (191, 71, 7), (199, 71, 7), (223,79,7), (223, 87, 7), (223, 87, 7), 
                     (215, 95, 7), (215, 95, 7), (215, 103, 15), (207, 111, 15), (207, 119, 15), (207, 127, 15), 
                     (207, 135, 23), (199, 135, 23), (199, 143, 23), (199, 151, 31), (191, 159, 31), (191, 159, 31), 
                     (191, 167, 39), (191, 167, 39), (191, 175, 47), (183, 175, 47), (183, 183, 47), (183,183,55), 
                     (207, 207, 111), (223, 223, 159), (239, 239,199), (255, 255, 255)]


n_pixels = screen_w * screen_h
fireBuffer = [ 0 for i in range(n_pixels)]
start_fire()


while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
               update_fire()
            if event.button == 3:
                burn = not burn

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                wind_direction = not wind_direction

            if event.key == pygame.K_w:
                blow_wind = not blow_wind

            if event.key == pygame.K_SPACE:
                if fire_on:
                    stop_fire()
                    fire_on = False
                else:
                    start_fire()
                    fire_on = True

    if burn:
        update_fire()

    draw_screen(screen)
    window.blit(pygame.transform.scale(screen, window.get_rect().size), (0, 0))
    pygame.display.update()
    clock.tick(FPS)
    