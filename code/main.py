from setting import * # Import all from file 'setting'
from level import Level # Import class 'Level' from file 'level'
from pytmx.util_pygame import load_pygame
from os.path import join

class Game:
    def __init__(self):
        pygame.init() # Start the game
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Set size of the window
        pygame.display.set_caption("Super Pirate World") # Set name of the game
        
        self.tmx_maps = {0: load_pygame(join('data','levels','omni.tmx'))} # 
        self.current_state = Level(self.tmx_maps[0]) # Assign class 'Level'
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.current_state.run() # Execute class 'Level'
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()