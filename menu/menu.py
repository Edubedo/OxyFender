# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
# Este software no puede ser copiado o redistribuido sin permiso del autor.
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
        
        self.opcionesMenuPrincipal = ["Play", "Credits", "Configuration", "Quit"] # Opciones inicales del menu principal
        
        # * Música de fondo 
        pygame.mixer.init() # Inicializar el módulo de sonido
        pygame.mixer.music.load(join("assets", "audio", "music", "let_us_adore_you.mp3")) # Cargar la música
        pygame.mixer.music.play(-1) # Reproducir la música en bucle
        pygame.mixer.music.set_volume(1)
        # volumen

    def mostrarOpcionesMenu(self, hoverOpcionSeleccionada=None): # Opciones del menú principal
        self.fondoPrincipalVideojuego = pygame.image.load(join("assets", "img", "Background", "menu", "Background_3.jpeg")).convert_alpha() # Agregar fondoPrincipalVideojuego al menú
        
        self.fondoPrincipalVideojuego = pygame.transform.scale(self.fondoPrincipalVideojuego, (WIDTH, HEIGHT)) # Escalar imagen del fondoPrincipalVideojuego del menú

        self.screen.blit(self.fondoPrincipalVideojuego, [0, 0]) # Acomodamos la imagenes del backgroud en la posición x=0 y=0
        self.rectOpcionesMenuPrincipal = []

        # Agregar el título del juego como imagen
        tituloPrincipalJuego = pygame.image.load(join("assets", "img", "TITULOS_FONDOS", "titulo_oxyfender.png")).convert_alpha()
        tituloPrincipalJuego = pygame.transform.scale(tituloPrincipalJuego, (self.screen.get_width() // 2, 115)) # Escalar la imagen si es necesario
        recTituloPrincipalJuego = tituloPrincipalJuego.get_rect(topleft=(-65, 5))
        self.screen.blit(tituloPrincipalJuego, recTituloPrincipalJuego)

        for i, opcionMenuPrincipal in enumerate(self.opcionesMenuPrincipal): # Recorremos todas las opciones del menu principal
            
            # Si el cursor está encima de alguna de las opciones pintar azul claro y hacer el botón más largo
            if i == hoverOpcionSeleccionada: 
                textoOpcionMenuPrincipal = self.font.render(opcionMenuPrincipal, True, WHITE)
                fondoTextoOpcionMenuPrincipal = pygame.Surface((BUTTON_MENU_WIDTH + 40, BUTTON_MENU_HEIGHT + 10))
                fondoTextoOpcionMenuPrincipal.fill(DARK_BLUE)
                fondoTextoOpcionMenuPrincipal.set_alpha(255) # Full opacity
            # Si el cursor NO está encima de alguna de las opciones pintar azul oscuro
            else: # Si el cursor no está encima de la opción
                textoOpcionMenuPrincipal = self.font.render(opcionMenuPrincipal, True, WHITE)
                fondoTextoOpcionMenuPrincipal = pygame.Surface((BUTTON_MENU_WIDTH + 10, BUTTON_MENU_HEIGHT + 10))
                fondoTextoOpcionMenuPrincipal.fill(DARK_BLUE)
                fondoTextoOpcionMenuPrincipal.set_alpha(204) # 0.8 opacity
            
            # A partir de cada opcion, dibujarle el rectangulo donde estárá centrada
            rectTextoOpcionMenuPrincipal = textoOpcionMenuPrincipal.get_rect(topleft=(10, (BUTTON_MENU_HEIGHT + 10) // 2 - textoOpcionMenuPrincipal.get_height() // 2))
            
            # Pintar el texto dentro de cada fondo
            fondoTextoOpcionMenuPrincipal.blit(textoOpcionMenuPrincipal, rectTextoOpcionMenuPrincipal.topleft)
            
            # Posicionar los fondos 
            rectOptionMenu = fondoTextoOpcionMenuPrincipal.get_rect(topleft=(0, 150 + i * 80)) # Más margen hacia abajo
            # Pintar los fondos dentro de la pantalla
            self.screen.blit(fondoTextoOpcionMenuPrincipal, rectOptionMenu)
            # Agregar las opciones a un arreglo para manejar el hover
            self.rectOpcionesMenuPrincipal.append((opcionMenuPrincipal.lower(), rectOptionMenu))
        
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
                            if option == "play" or option == "jugar":
                                game_menu = MenuPlay(self.screen, self.config, self.bucleInicial)
                                game_menu.mostrarMenuDificultad()
                                continue
                            
                            if option == "credits" or option == "créditos":
                                credits = Creditos(self.screen)
                                credits.run()
                                self.bucleInicial = True  # Reiniciar el bucle del menú después de mostrar los créditos
                                # Reproducir la música de fondo nuevamente
                                pygame.mixer.music.load(join("assets", "audio", "music", "let_us_adore_you.mp3"))
                                pygame.mixer.music.play(-1)
                                pygame.mixer.music.set_volume(0.2)

                            elif option == "configuration" or option == "configuración":
                                self.config.show_configuration(self.screen, self.font)

                            elif option == "quit" or option == "salir":
                                pygame.quit()
                                sys.exit()
                            else:
                                return option