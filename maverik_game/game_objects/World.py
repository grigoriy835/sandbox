from pygame.rect import Rect

from Constants import Constants
from game_objects.GameDrawableObject import GameDrawableObject


class World(GameDrawableObject):

    def __init__(self):
        super().__init__()
        self.color = (139, 195, 74)
        self.height = Constants.WORLD_HEIGHT / 5
        self.width = Constants.WORLD_WIDTH
        self.rect = Rect(0, Constants.WORLD_HEIGHT - self.height, Constants.WORLD_WIDTH, self.height)

