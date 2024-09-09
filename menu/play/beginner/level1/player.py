from utils.settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_frect(topleft=pos)