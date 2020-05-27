import pygame

from Constants import Constants
from game_objects.GameDrawableObject import GameDrawableObject

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([50, 100])
        self.image.fill((10, 250, 10))

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.speed = 0,0
        self.acc = 1,0
        self.can_jump = True

    def jump(self):
        if self.can_jump:
            self.speed[0] -= 10
            self.can_jump = False
            
    def move_up(self, dir):
        self.speed[1] += dir
    
    def update(self, *args):
        newpos = self.rect.move(self.speed)
        
