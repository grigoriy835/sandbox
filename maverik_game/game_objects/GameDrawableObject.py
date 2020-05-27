import pygame


class GameDrawableObject:

    def __init__(self):
        self.color = None
        self.height = 0
        self.width = 0
        self.rect = None

    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), self.color, self.rect)