import pygame
from player import Player
from settings import GRID_SIZE, BOX_POSITION

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player(GRID_SIZE)
        self.running = True
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.move(event.pos)

    def update(self):
        if self.player.rect.collidepoint(BOX_POSITION):
            print("Reparar")

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        pygame.draw.rect(self.screen, (0, 255, 0), (*BOX_POSITION, GRID_SIZE, GRID_SIZE))
        pygame.display.flip()
