import os, sys
import pygame
from pygame import draw
from pygame.locals import *
import random

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

def main():
    colors = {
        'black': (0,0,0),
        'grin': (150, 255, 150),
        'read': (255, 0, 0),
        'white': (255,255,255),
        'blue': (150,150,255)
    }
    # Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((1000,600))
    pygame.display.set_caption('fuck')
    # pygame.mouse.set_visible(0)

    #The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    screen.blit(background, (0, 0))

    lines = [
        {
            'color': colors['black'],
            'height': 111,
            'speed': 1,
            'acceleration': 1,
            'direction': 1,
            'switch_chance': 10,
        },
        {
            'color': colors['read'],
            'height': 222,
            'speed': 1,
            'acceleration': 4,
            'direction': -1,
            'switch_chance': 0,
        },
        {
            'color': colors['grin'],
            'height': 333,
            'speed': 1,
            'acceleration': 0.3,
            'direction': 1,
            'switch_chance': 4,
        },
        {
            'color': colors['blue'],
            'height': 444,
            'speed': 1,
            'acceleration': 1.5,
            'direction': 1,
            'switch_chance': 84,
        },
    ]

    def draw_next_frame():

        background.fill((250, 250, 250))
        for line in lines:
            if random.random()*1000 < line['switch_chance']:
                line['direction'] *= -1
            if line['speed'] > 10 or line['speed'] < 0:
                line['acceleration'] = -line['acceleration']
            line['speed'] = line['speed'] + line['acceleration']/120
            next_height = line['height'] + line['speed'] * line['direction']
            if next_height > 580:
                next_height = 1160 - next_height
                line['direction'] *= -1
            if next_height < 0:
                next_height = -next_height
                line['direction'] *= -1
            line['height'] = next_height
            rect = draw.rect(background, line['color'], [0, int(line['height']), 1000, 20])

        screen.blit(background, (0, 0))
        pygame.display.update()

    clock = pygame.time.Clock()
    # Main Loop
    going = True
    key_dict = {32: True}
    pause = False
    while going:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type != pygame.MOUSEMOTION:
                print(event)
            if event.type == pygame.QUIT:
                going = False
            if event.type == KEYDOWN:
                if event.key in key_dict:
                    # pause = not pause
                    for line in lines:
                        line['speed'] = 1

        if not pause:
            draw_next_frame()


    pygame.quit()


if __name__ == '__main__':
    main()
