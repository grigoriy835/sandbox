import pygame
from pygame.rect import Rect
from pygame.sprite import Sprite


class World(Sprite):

    def __init__(self):
        super().__init__()
        self.color = (139, 195, 74)
        self.area = pygame.display.get_surface().get_rect()
        self.height = self.area.height / 5
        self.width = self.area.width
        self.rect = Rect(0, self.area.height - self.height, self.area.width, self.height)
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)

