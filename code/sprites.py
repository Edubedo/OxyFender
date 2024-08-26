from setting import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE, TILE_SIZE)), groups = None):
        super().__init__(groups) # Call the __init__ method of the parent class
        self.image = surf # Create a new surface
        self.image.fill('white') # Fill the surface with white color
        self.rect = self.image.get_rect(topleft = pos) # Get the rectangle of the surface
        self.old_rect = self.rect.copy() # Get the rectangle of the surface

class MovingSprite(Sprite):
    def __init__ (self, groups, start_pos, end_pos, move_dir, speed):
        surf = pygame.Surface((200, 50))
        super().__init__(start_pos, surf, groups)
        self.rect.center = start_pos
        self.start_pos = start_pos
        self.end_pos = end_pos

        # Mov
        self.speed = speed
        self.direction = vector(1, 0) if move_dir == 'x' else vector(0, 1)
        self.move_dir = move_dir

    def check_border(self): # Function that we use for check if the plataform reach it limit
        if self.move_dir == 'x':
            if self.rect.right >= self.end_pos[0] and self.direction.x == 1:
                self.direction.x = -1
                self.rect.right = self.end_pos[0]

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.direction + self.speed
        self.check_border()