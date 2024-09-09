# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
# Este software no puede ser copiado o redistribuido sin permiso del autor.
import pygame
from menu.configuration.configuration import Configuration
from utils.settings import *
from menu.play.menu_game import MenuGame
from menu.credits.credits import show_credits
from os.path import join
import sys

class Menu:
    def __init__(self, screen):
        self.screen = screen
        pygame.display.set_caption(f"Menú - {TITLE_GAME}")

        self.config = Configuration()
        self.font = pygame.font.Font(join("assets", "fonts", "Font_Menu_Options.ttf"), 18) # Fuente de texto

        # pygame.mixer.init() # Inicializar el módulo de sonido
        # pygame.mixer.music.load(join("assets", "audio", "music", "let_us_adore_you.mp3")) # Cargar la música
        # pygame.mixer.music.play(-1) # Reproducir la música en bucle

        self.actualizarLenguajeTextos()

    def actualizarLenguajeTextos(self): # Actualizar el idioma de los textos
        language = self.config.obtenerLenguajeActual()
        if language == "english":
            self.options = ["Play", "Credits", "Configuration", "Quit"]
        else:  
            self.options = ["Jugar", "Créditos", "Configuración", "Salir"]

    def mostrarOpcionesMenu(self, indice_opcion_curso_encima=None):
        self.background = pygame.image.load(join("assets", "img", "Background", "menu", "BackgroundProvisional2.jpg")).convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.screen.blit(self.background, [0, 0])
        self.option_rects = []

        # Agregar el título del juego
        fontTitulo = pygame.font.Font(join("assets", "fonts", "Triforce.ttf"), 100)
        titulo = fontTitulo.render(TITLE_GAME, True, BLACK)
        titulo_rect = titulo.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(titulo, titulo_rect)

        for i, option in enumerate(self.options): # Mostrar las opciones del menú
            if i == indice_opcion_curso_encima: # Si el cursor está encima de la opción
                textOptionMenu = self.font.render(option, True, WHITE)
                background_rect = pygame.Surface((BUTTON_MENU_WIDTH, BUTTON_MENU_HEIGHT))
                background_rect.fill(LIGHTBLUE)
            else: # Si el cursor no está encima de la opción
                textOptionMenu = self.font.render(option, True, WHITE)
                background_rect = pygame.Surface((BUTTON_MENU_WIDTH, BUTTON_MENU_HEIGHT))
                background_rect.fill(DARK_BLUE)
            
            text_rect = textOptionMenu.get_rect(topleft=(10, BUTTON_MENU_HEIGHT // 2 - textOptionMenu.get_height() // 2))
            background_rect.blit(textOptionMenu, text_rect.topleft)
            
            rectOptionMenu = background_rect.get_rect(topleft=(0, 150 + i * 70))
            self.screen.blit(background_rect, rectOptionMenu)
            self.option_rects.append((option.lower(), rectOptionMenu))
        
        # Agregar texto en la esquina inferior derecha
        fontTextoInferiorDerecha = pygame.font.Font(join("assets", "fonts", "Font_Name_Enterprise.ttf"), 24)
        textoInferiorDerecha = fontTextoInferiorDerecha.render(NAME_ENTERPRISE, True, BLACK)
        texto_rect = textoInferiorDerecha.get_rect(bottomright=(self.screen.get_width() - 10, self.screen.get_height() - 10))
        self.screen.blit(textoInferiorDerecha, texto_rect)

        pygame.display.flip()

    def mostrarMenuInicial(self):
        indice_opcion_curso_encima = None
        while True:
            self.mostrarOpcionesMenu(indice_opcion_curso_encima)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    indice_opcion_curso_encima = None
                    for i, (_, rect) in enumerate(self.option_rects):
                        if rect.collidepoint(event.pos):
                            indice_opcion_curso_encima = i
                            break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for option, rect in self.option_rects:
                        if rect.collidepoint(event.pos):
                            if option == "play" or option == "jugar":
                                game_menu = MenuGame(self.screen, self.config)
                                return game_menu.mostrarMenuDificultad()
                            if option == "credits" or option == "créditos":
                                show_credits(self.screen)
                                continue
                            elif option == "configuration" or option == "configuración":
                                self.config.show_configuration(self.screen, self.font)
                                self.actualizarLenguajeTextos()
                            elif option == "quit" or option == "salir":
                                pygame.quit()
                                sys.exit()
                            else:
                                return option
