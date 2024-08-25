from setting import *
from sprites import Sprite
from player import Player

class Level:
    def __init__(self,tmx_map):
        self.display_surface = pygame.display.get_surface() # Get surface of the screen
        
        # sprite.Group() class provided by Pygame that is used to hold and manage multiple Sprite objects.
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map)  

    def setup(self, tmx_map):
        # iterates over the tiles in the 'Terrain' layer of the Tiled map, creating a new Sprite instance for each tile at the correct position and adding it to the sprite groups and player
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles(): 
            Sprite((x * TILE_SIZE,y * TILE_SIZE), surf, (self.all_sprites, self.collision_sprites)) # Create a new sprite
 
        for obj in tmx_map.get_layer_by_name('Objects'): # Get the objects of the layer 'Objects'
            if obj.name == 'player': # If the object is the player
                Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
            
    def run(self, dt): # update all sprites
        self.display_surface.fill('black') # Change screen of the window
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.display_surface)