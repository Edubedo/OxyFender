import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.options = ["Jugar", "Configuración", "Créditos", "Salir"]

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))
            for i, option in enumerate(self.options):
                text = self.font.render(option, True, (255, 255, 255))
                self.screen.blit(text, (300, 200 + i * 60))
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 200 < y < 260:
                        return 'game'
                    elif 260 < y < 320:
                        return 'settings'
                    elif 320 < y < 380:
                        return 'credits'
                    elif 380 < y < 440:
                        return 'quit'
