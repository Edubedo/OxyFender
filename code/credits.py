import pygame

class Credits:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))
            text = self.font.render("Game by Your Name", True, (255, 255, 255))
            self.screen.blit(text, (200, 300))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'menu'
