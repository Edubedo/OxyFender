from setting import *
from sprites import Sprite
class Level:
    def __init__(self,tmx_map):
        self.display_surface = pygame.display.get_surface() # Get surface of the screen
        
        # groups
        self.all_sprites = pygame.sprite.Group()

        self.setup(tmx_map)  

    def setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x,y), surf, self.all_sprites)
        
    def run(self):
        self.display_surface.fill('black') # Change screen of the window
        self.all_sprites.draw(self.display_surface)