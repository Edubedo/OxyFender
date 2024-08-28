import pygame
from configuration import Configuration

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.config = Configuration()
        self.font = pygame.font.Font(None, 36)
        self.options = self.get_options()

    def get_options(self):
        language = self.config.get_language()
        if language == "english":
            return ["Play", "Credits", "Configuration", "Quit"]
        else:  # Asumimos que es español
            return ["Jugar", "Créditos", "Configuración", "Salir"]

    def show(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.option_rects = []  # Reiniciar la lista de rectángulos en cada loop
            for i, option in enumerate(self.options):
                text = self.font.render(option, True, (255, 255, 255))
                rect = text.get_rect(center=(self.screen.get_width() // 2, 150 + i * 50))
                self.screen.blit(text, rect)
                self.option_rects.append((option.lower(), rect))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for option, rect in self.option_rects:
                        if rect.collidepoint(event.pos):
                            if option == "configuration" or option == "configuración":
                                self.show_configuration()
                                break  # Salir del loop actual después de mostrar configuración
                            else:
                                return option

    def show_configuration(self):
        self.screen.fill((0, 0, 0))
        self.option_rects = []  # Reiniciar la lista de rectángulos para el menú de configuración
        languages = ["English", "Español"]
        for i, language in enumerate(languages):
            text = self.font.render(language, True, (255, 255, 255))
            rect = text.get_rect(center=(self.screen.get_width() // 2, 150 + i * 50))
            self.screen.blit(text, rect)
            self.option_rects.append((language.lower(), rect))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for language, rect in self.option_rects:
                        if rect.collidepoint(event.pos):
                            self.config.set_language(language)
                            self.options = self.get_options()  # Actualizar opciones en base al nuevo idioma
                            return
