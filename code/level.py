from setting import *
from sprites import Sprite
from player import Player

class Level:
    def __init__(self,tmx_map):
        self.display_surface = pygame.display.get_surface() # Get surface of the screen
        
        # groups
        self.all_sprites = pygame.sprite.Group() # Create a of the structure of the map
        self.setup(tmx_map)  

    def setup(self, tmx_map):
        # 
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles(): # Get the tiles of the layer 'Terrain'
            Sprite((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites) # Create a new sprite
        for obj in tmx_map.get_layer_by_name('Objects'): # Get the objects of the layer 'Objects'
            if obj.name == 'player': # If the object is the player
                Player((obj.x, obj.y), self.all_sprites)
            
    def run(self, dt):
        self.all_sprites.update(dt)
        self.display_surface.fill('black') # Change screen of the window
        self.all_sprites.draw(self.display_surface)