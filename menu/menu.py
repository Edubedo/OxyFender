import pygame
from configuration.configuration import Configuration
from general.settings import *
from game_levels.menu_game import MenuGame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.config = Configuration()
        self.font = pygame.font.Font(None, 36) # Fuente de texto
        self.actualizar_lenguage_textos() 

    def actualizar_lenguage_textos(self):
        language = self.config.get_language()
        if language == "english":
            self.options = ["Play", "Credits", "Configuration", "Quit"]
        else:  
            self.options = ["Jugar", "Créditos", "Configuración", "Salir"]

    def mostrarOpcionesMenu(self):
        self.background = pygame.image.load("assets/Background/menu/BackgroundProvisional.jpeg").convert() # Cargamos la imagen de fondo

        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.screen.blit(self.background, [0, 0]) # Dibujamos la imagen de fondo en la pantalla
        self.option_rects = []  
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, TEXT_COLOR)
            rect = text.get_rect(center=(self.screen.get_width() // 2, 150 + i * 50))
            self.screen.blit(text, rect)
            self.option_rects.append((option.lower(), rect))
        pygame.display.flip()

    def mostrarMenuInicial(self):
        self.mostrarOpcionesMenu()
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
                                self.config.show_configuration(self.screen, self.font)
                                return 
                            else:
                                return option