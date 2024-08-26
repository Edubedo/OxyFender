from setting import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE, TILE_SIZE)), groups = None):
        super().__init__(groups) # Call the __init__ method of the parent class
        self.image = surf # Create a new surface
        self.image.fill('white') # Fill the surface with white color
        self.rect = self.image.get_rect(topleft = pos) # Get the rectangle of the surface
        self.old_rect = self.rect.copy() # Get the rectangle of the surface

class MovingSprite(Sprite):
    def __init__ (self, groups, start_pos, end_pos, mode_dir, speed):
        surf = pygame.Surface((200, 50))
        super().__init__(start_pos, surf, groups)