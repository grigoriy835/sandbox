import pygame
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
    pygame.mouse.set_visible(0)

    #The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    screen.blit(background, (0, 0))
    world = World()
    player = Player()
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

        # Draw Everything
        screen.blit(background, (0, 0))
        world.draw()
        player.draw()
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
