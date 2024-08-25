from setting import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups) # Call the __init__ method of the parent class
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE)) # Create a new surface
        self.image.fill('white') # Fill the surface with white color
        self.rect = self.image.get_rect(topleft = pos) # Get the rectangle of the surface
        self.old_rect = self.rect.copy() # Get the rectangle of the surface