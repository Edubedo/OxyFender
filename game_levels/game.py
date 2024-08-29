import pygame

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.start_time = pygame.time.get_ticks()  
        self.font = pygame.font.Font(None, 36)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if not self.paused:
                self.screen.fill((0, 0, 0))  
                pygame.display.flip()
            
            self.clock.tick(60)  