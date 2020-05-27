import pygame
from pygame.sprite import Sprite


class Player(Sprite):

    def __init__(self):
        Sprite.__init__(self)
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.width = 20
        self.height = 100
        self.color = (10, 250, 10)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = self.area.width / 2 - self.width, self.area.height / 2 - self.height
        self.speed = 0, 0
        self.acc = 1, 0
        self.can_jump = True

    def jump(self):
        if self.can_jump:
            self.speed[0] -= 10
            self.can_jump = False

    def move_up(self, dir):
        self.speed[1] += dir

    def update(self, *args):
        newpos = self.rect.move(self.speed)
