import os, sys
import pygame
from pygame import draw
from pygame.locals import *

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
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption('fuck')
    # pygame.mouse.set_visible(0)

    # Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    rect = draw.rect(background, colors['black'], [0,550,1000,560])

    # Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    rect = draw.rect(background, colors['black'], [0, 10, 1000, 20])

    pygame.display.update()
    clock = pygame.time.Clock()
    # Main Loop
    going = True
    key_dict = {}
    while going:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type != pygame.MOUSEMOTION:
                print(event)
            if event.type == pygame.QUIT:
                going = False
            if event.type == KEYDOWN:
                if event.key in key_dict:
                    pass

    pygame.quit()


if __name__ == '__main__':
    main()
