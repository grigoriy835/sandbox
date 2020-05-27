from pygame.rect import Rect

from Constants import Constants
from game_objects.GameDrawableObject import GameDrawableObject


class Player(GameDrawableObject):

    def __init__(self):
        super().__init__()
        self.color = (3, 155, 229)
        self.height = 50
        self.width = 10
        self.rect = Rect(Constants.WORLD_WIDTH / 2 - self.width, Constants.WORLD_HEIGHT / 2 - self.height, self.width, self.height)



