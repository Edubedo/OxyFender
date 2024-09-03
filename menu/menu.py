import pygame
from menu.configuration.configuration import Configuration
from utils.settings import *
from  menu.play.menu_game import MenuGame
from menu.credits.credits import show_credits


class Menu:
    def __init__(self, screen):
        # Configuración de la pantalla
        self.screen = screen
        pygame.display.set_caption(f"Menú - {TITLE_GAME}") # Establecemos el titulo del juego

        self.config = Configuration() # Inicializamos la configuración
        self.font = pygame.font.Font(None, 36) # Fuente de texto
        self.actualizarLenguajeTextos() 

    def actualizarLenguajeTextos(self):
        language = self.config.obtenerLenguajeActual()
        if language == "english":
            self.options = ["Play", "Credits", "Configuration", "Quit"]
        else:  
            self.options = ["Jugar", "Créditos", "Configuración", "Salir"]

    def mostrarOpcionesMenu(self):
        # Cargamos la imagen de fondo del menu
        self.background = pygame.image.load("assets/img/Background/menu/BackgroundProvisional.jpeg").convert_alpha() # Cargamos la imagen de fondo
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # Dibujamos la imagen de fondo en la pantalla
        self.screen.blit(self.background, [0, 0]) # Dibujamos la imagen de fondo en la pantalla
        self.option_rects = [] # Lista de opciones
        for i, option in enumerate(self.options):
            textOptionMenu = self.font.render(option, True, WHITE)
            background_rect = pygame.Surface((BUTTON_MENU_WIDTH, BUTTON_MENU_HEIGHT))
            background_rect.fill(BLACK)
            background_rect.blit(textOptionMenu, (2, 10))  
            
            option_rect = background_rect.get_rect(topleft=(0, 150 + i * 70))
            self.screen.blit(background_rect, option_rect)
            self.option_rects.append((option.lower(), option_rect))
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
                                return game_menu.mostrarMenuDificultad()
                            if option == "credits" or option == "créditos":
                                show_credits(self.screen)
                                return
                            elif option == "configuration" or option == "configuración":
                                self.config.show_configuration(self.screen, self.font)
                                return 
                            else:
                                return option