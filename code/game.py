import pygame
from utils import Reactor

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.reactors = [Reactor((100, 100)), Reactor((200, 200)), Reactor((300, 300))]
        self.character_pos = [50, 50]

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))

            # Draw reactors
            for reactor in self.reactors:
                reactor.draw(self.screen)

            # Draw character
            pygame.draw.circle(self.screen, (0, 255, 0), self.character_pos, 20)

            pygame.display.flip()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'menu'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.character_pos = list(event.pos)
                    for reactor in self.reactors:
                        if reactor.is_near(self.character_pos):
                            # Trigger mini-game or task
                            pass
