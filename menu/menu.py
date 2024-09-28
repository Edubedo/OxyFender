import pygame
from menu.configuration.configuration import Configuration
from utils.configuraciones import *
from menu.play.menu_game import MenuPlay
from menu.credits.credits import Creditos
from os.path import join
import sys

class Menu:
    def __init__(self, screen):
        self.screen = screen 
        pygame.display.set_caption(f"Menú - {TITLE_GAME}") # Establecemos tituloPrincipalJuego del Menú

        self.bucleInicial = True # Bucle para iniciar el menú
        self.config = Configuration() # Establecemos la configuracion del lenguaje 
        self.font = pygame.font.Font(join("assets", "fonts", "Font_Menu_Options.ttf"), 18) # Establecemos la Fuente de texto
        
        # TODO MANEJO CON ESPAÑOL E INGLES
        self.opcionesMenuPrincipal = [
        {
            "name": "Play",
            "id": "play",
            "image": pygame.image.load(join("assets", "img", "BOTONES", "b_play.png")).convert_alpha()
        }, 
        {
            "name": "Credits",
            "id": "credits",
            "image": pygame.image.load(join("assets", "img", "BOTONES", "b_credits.png")).convert_alpha()
        }, 
        {
            "name": "Configuration",
            "id": "configuration",
            "image": pygame.image.load(join("assets", "img", "BOTONES", "b_configuration.png")).convert_alpha()
        }, 
        {
            "name": "Quit",
            "id": "quit",
            "image": pygame.image.load(join("assets", "img", "BOTONES", "b_quit.png")).convert_alpha()
        }] # Opciones inicales del menu principal
        
        # * Música de fondo 
        pygame.mixer.init() # Inicializar el módulo de sonido
        pygame.mixer.music.load(join("assets", "audio", "music", "let_us_adore_you.mp3")) # Cargar la música
        pygame.mixer.music.play(-1) # Reproducir la música en bucle
        pygame.mixer.music.set_volume(1)
        # volumen

        # Cargar sonido de clic
        self.sonidoDeClick = pygame.mixer.Sound(join("assets", "audio", "utils", "click_madera.mp3"))

    def mostrarOpcionesMenu(self, hoverOpcionSeleccionada=None): # Opciones del menú principal
        self.fondoPrincipalVideojuego = pygame.image.load(join("assets", "img", "Background", "menu", "Background_5.jpeg")).convert_alpha() # Agregar fondoPrincipalVideojuego al menú
        
        self.fondoPrincipalVideojuego = pygame.transform.scale(self.fondoPrincipalVideojuego, (WIDTH, HEIGHT)) # Escalar imagen del fondoPrincipalVideojuego del menú

        self.screen.blit(self.fondoPrincipalVideojuego, [0, 0]) # Acomodamos la imagenes del backgroud en la posición x=0 y=0
        self.rectOpcionesMenuPrincipal = []

        # Agregar el título del juego como imagen
        tituloPrincipalJuego = pygame.image.load(join("assets", "img", "TITULOS_FONDOS", "titulo_oxyfender.png")).convert_alpha()
        tituloPrincipalJuego = pygame.transform.scale(tituloPrincipalJuego, (self.screen.get_width(), 115)) # Escalar la imagen si es necesario
        recTituloPrincipalJuego = tituloPrincipalJuego.get_rect(topleft=(-5, 5))
        self.screen.blit(tituloPrincipalJuego, recTituloPrincipalJuego)

        for i, opcionMenuPrincipal in enumerate(self.opcionesMenuPrincipal): # Recorremos todas las opciones del menu principal
            if i == hoverOpcionSeleccionada: # * Si el cursor está encima de alguna de las opciones pintar azul claro y hacer el botón más largo
                image = opcionMenuPrincipal['image']
                image = pygame.transform.scale(image, (opcionMenuPrincipal['image'].get_width() + 100, opcionMenuPrincipal['image'].get_height() + 20))
                image.set_alpha(255)  # Set the alpha of the image (opacity level)
                image_rect = image.get_rect(topleft=(10, 150 + i * (image.get_height() + 10)))
                fondoTextoOpcionMenuPrincipal = self.screen.blit(image, image_rect)

            else:  # * Si el cursor no está encima de la opción
                image = opcionMenuPrincipal['image']
                image = pygame.transform.scale(image, (image.get_width() + 30, image.get_height() + 20))
                image.set_alpha(150)  # Set the alpha of the image (opacity level)
                image_rect = image.get_rect(topleft=(10, 150 + i * (image.get_height() + 10)))
                self.screen.blit(image, image_rect)

            
            # Posicionar los fondos 
            # Agregar las opciones a un arreglo para manejar el hover
            self.rectOpcionesMenuPrincipal.append((opcionMenuPrincipal, image_rect))
        
        # Agregar nombre de la empresa
        fontTextoInferiorDerecha = pygame.font.Font(join("assets", "fonts", "Font_Name_Enterprise.ttf"), 24) # Fuente
        textoInferiorDerecha = fontTextoInferiorDerecha.render(NAME_ENTERPRISE, True, WHITE) # Texto
        texto_rect = textoInferiorDerecha.get_rect(bottomright=(self.screen.get_width() - 10, self.screen.get_height() - 10)) # Rectangulo para mostrar el texto en la pantalla
        self.screen.blit(textoInferiorDerecha, texto_rect) # Mostrar texto en la pantalla

        pygame.display.flip() # Actualizar pantalla

    def mostrarMenuInicial(self):
        hoverOpcionSeleccionada = None # Se usa para manejar el hover 

        # Entramos en un bucle infinito para mostrar el menú
        while self.bucleInicial:
            self.mostrarOpcionesMenu(hoverOpcionSeleccionada)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Si el cursor se mueve sobre alguna de las opciones del menú principal cambiar el hover a 1 para posteriormente manejar el color
                elif event.type == pygame.MOUSEMOTION:
                    hoverOpcionSeleccionada = None
                    for i, (_, rect) in enumerate(self.rectOpcionesMenuPrincipal):
                        if rect.collidepoint(event.pos):
                            hoverOpcionSeleccionada = i
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                            break
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                # Dependiendo de la opción seleccionada, se ejecuta una acción
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for option, rect in self.rectOpcionesMenuPrincipal: # Recorremos las opciones del menú principal
                        if rect.collidepoint(event.pos):
                            # Reproducir sonido de clic
                            self.sonidoDeClick.play() # Cuando hace un click dentro de las opciones del menú
                            
                            if option['id'] == "play" or option['id'] == "jugar":
                                game_menu = MenuPlay(self.screen, self.config, self.bucleInicial)
                                game_menu.mostrarMenuDificultad()
                                continue
                            
                            if option['id'] == "credits" or option['id'] == "créditos":
                                credits = Creditos(self.screen)
                                credits.run()
                                self.bucleInicial = True  # Reiniciar el bucle del menú después de mostrar los créditos
                                # Reproducir la música de fondo nuevamente
                                pygame.mixer.music.load(join("assets", "audio", "music", "let_us_adore_you.mp3"))
                                pygame.mixer.music.play(-1)
                                pygame.mixer.music.set_volume(0.2)

                            elif option['id'] == "configuration" or option['id'] == "configuración":
                                self.config.show_configuration(self.screen, self.font)

                            elif option['id'] == "quit" or option['id'] == "salir":
                                pygame.quit()
                                sys.exit()
                            else:
                                return option['id']