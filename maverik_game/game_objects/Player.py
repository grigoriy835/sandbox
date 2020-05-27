import pygame
from pygame.sprite import Sprite


class Player(Sprite):

    def __init__(self):
        Sprite.__init__(self)
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.width = 40
        self.height = 100
        self.color = (150, 10, 200)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = self.area.width / 2 - self.width, self.area.height / 2 - self.height
        self.speed = [0, 0]
        self.acc = [1, 0]
        self.can_jump = True

    def jump(self):
        if self.can_jump:
            self.speed[1] -= 10
            self.can_jump = False

    def move_up(self, dir):
        self.speed[1] = dir

    def move_stop(self):
        self.speed[0] = 0
        self.speed[1] = 0
    
    def update(self, *args):
        newpos = self.rect.move(self.speed)
        new_speed = self.get_speed()
        self.speed[0] = new_speed[0]
        self.speed[1] = new_speed[1]
        self.rect = newpos

    def get_speed(self):
        speed = [0, 0]
        if self.rect.right < self.area.right:
            speed[0] += self.acc[0]
            speed[1] += self.acc[1]
            return speed
        elif self.rect.left > self.area.left:
            speed[0] += self.acc[0]
            speed[1] += self.acc[-1]
            return speed

