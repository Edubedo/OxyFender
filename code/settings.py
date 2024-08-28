import pygame

class Settings:
    def __init__(self, screen):
        self.screen = screen

    def run(self):
        while True:
            self.screen.fill((0, 0, 128))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'menu'
