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

        self.config = Configuration() # Establecemos la configuracion del lenguaje 
        self.font = pygame.font.Font(join("assets", "fonts", "Font_Menu_Options.ttf"), 18) # Establecemos la Fuente de texto

        # Música de fondo 

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

    def mostrarOpcionesMenu(self, indice_opcion_curso_encima=None): # Opciones del menú principal
        self.background = pygame.image.load(join("assets", "img", "Background", "menu", "BackgroundProvisional2.jpg")).convert_alpha() # Agregar background al menú
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT)) # Escalar imagen del background del menú

        self.screen.blit(self.background, [0, 0]) # Acomodamos la imagenes del backgroud en la posición x=0 y=0
        self.option_rects = []

        # Agregar el título del juego
        fontTitulo = pygame.font.Font(join("assets", "fonts", "Triforce.ttf"), 100) # Establecemos la fuente del titulo
        titulo = fontTitulo.render(TITLE_GAME, True, BLACK) #  Le agregamos color al titulo
        titulo_rect = titulo.get_rect(center=(self.screen.get_width() // 2, 50)) # Creamos un rectangulo donde vamos a insertar el titulo del juego
        self.screen.blit(titulo, titulo_rect) # Insertar el titulo de nuestro juego

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

        pygame.display.flip() # Actualizar pantalla

    def mostrarMenuInicial(self):
        indice_opcion_curso_encima = None # Se usa para manejar el hover 

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
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                            break
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
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
