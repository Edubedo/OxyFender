import pygame
from configuration.configuration import Configuration
from general.settings import *
from game_levels.menu_game import MenuGame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.config = Configuration()
        self.font = pygame.font.Font(None, 36) # Fuente de texto
        self.update_options() 

    def update_options(self):
        language = self.config.get_language()
        if language == "english":
            self.options = ["Play", "Credits", "Configuration", "Quit"]
        else:  
            self.options = ["Jugar", "Créditos", "Configuración", "Salir"]

    def show_options_menu(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.option_rects = []  
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, TEXT_COLOR)
            rect = text.get_rect(center=(self.screen.get_width() // 2, 150 + i * 50))
            self.screen.blit(text, rect)
            self.option_rects.append((option.lower(), rect))
        pygame.display.flip()

    def mostrar_menu_inicial(self):
        self.show_options_menu()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for option, rect in self.option_rects:
                        if rect.collidepoint(event.pos):
                            if option == "play" or option == "jugar":
                                game_menu = MenuGame(self.screen, self.config)
                                return game_menu.show_difficulty_menu()
                            elif option == "configuration" or option == "configuración":
                                self.show_configuration()
                                return 
                            else:
                                return option

    def show_configuration(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.option_rects = []  
        languages = ["English", "Español"]
        for i, language in enumerate(languages):
            text = self.font.render(language, True, TEXT_COLOR)
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
                            self.update_options()  
                            return

