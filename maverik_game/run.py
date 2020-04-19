import os, sys
import pygame
from pygame import draw
from pygame.locals import *
import random

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

def main():
    # Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((1000,600))
    pygame.display.set_caption('fuck')
    pygame.mouse.set_visible(0)

    #The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    screen.blit(background, (0, 0))

    clock = pygame.time.Clock()
    # Main Loop
    going = True
    while going:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type != pygame.MOUSEMOTION:
                print(event)
            if event.type == pygame.QUIT:
                going = False
            if event.type == KEYDOWN:
                if event.key == 0:
                    going = False

    pygame.quit()


if __name__ == '__main__':
    main()
