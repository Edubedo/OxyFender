from setting import * # Import all from file 'setting'
from level import Level # Import class 'Level' from file 'level'
from pytmx.util_pygame import load_pygame # Process files tiled
from os.path import join

class Game:
    def __init__(self):
        pygame.init() # Start the game
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Set size of the window
        pygame.display.set_caption("Super Game") # Set name of the game
        self.clock = pygame.time.Clock() # Start timer
        self.tmx_maps = {0: load_pygame(join('data','levels','omni.tmx'))} # Get data from file Tiled
        self.current_state = Level(self.tmx_maps[0]) # Pass the data from tiled to the class level
    
    def run(self):
        while True: # Loop where we continously check for events
            dt = self.clock.tick(30) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.current_state.run(dt) # Execute class 'Level'
            pygame.display.update()


if __name__ == '__main__': # If we are in the file main, we execute the game
    game = Game()
    game.run()