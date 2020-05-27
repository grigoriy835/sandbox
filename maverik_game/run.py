import os, sys
import pygame
from pygame import draw
from pygame.locals import *

from Constants import Constants
from game_objects.Player import Player
from game_objects.World import World

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

def main():
    # Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((Constants.WORLD_WIDTH, Constants.WORLD_HEIGHT))
    pygame.display.set_caption('fuck')
    pygame.mouse.set_visible(1)

    #The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    screen.blit(background, (0, 0))
    pygame.display.flip()

    world = World()
    player = Player(world)

    allsprites = pygame.sprite.RenderPlain((player, world))

    screen.blit(background, (0, 0))
    allsprites.draw(screen)
    pygame.display.flip()

    clock = pygame.time.Clock()
    # Main Loop
    going = True
    while going:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type not in [pygame.MOUSEMOTION, pygame.ACTIVEEVENT] :
                print(event)
            if event.type == pygame.QUIT:
                going = False
            if event.type == KEYDOWN:
                if event.key == 32:
                    player.jump()
                if event.key == 276:
                    player.move_up(-3)
                if event.key == 275:
                    player.move_up(3)
            if event.type == KEYUP:
                if event.key == 276 or event.key == 275:
                    player.move_stop()

        allsprites.update()
        
        # Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
