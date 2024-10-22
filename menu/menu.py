import pygame
from utilerias.configuraciones import *
from menu.play.menu_game import MenuPlay
from menu.credits.credits import Creditos
from os.path import join
import os
import sys
import json

class Menu:
    def __init__(self, screen, volumen="on"):
        self.screen = screen 
        pygame.display.set_caption(f"Menu - {TITLE_GAME}") # Establecemos tituloPrincipalJuego del Menú

        self.bucleInicial = True # Bucle para iniciar el menú
        self.font = pygame.font.Font(join("assets", "fonts", "Font_Menu_Options.ttf"), 18) # Establecemos la Fuente de texto
        
        self.configLanguage = "es"  # Default language configuration
        self.volumen = volumen  # Default volume state
        self.datosLanguage = {} # Datos del menú

        with open('language.json') as archivo:
            self.datosLanguage = json.load(archivo) #asignando los datos del archivo json a la variable datosLanguage

        self.actualizarOpcionesMenu()

        # * Música de fondo 
        pygame.mixer.init() # Inicializar el módulo de sonido
        pygame.mixer.music.load(join("assets", "audio", "music", "let_us_adore_you.mp3")) # Cargar la música
        pygame.mixer.music.play(-1) # Reproducir la música en bucle
        pygame.mixer.music.set_volume(1 if self.volumen == "on" else 0)

        # Cargar sonido de clic
        self.sonidoDeClick = pygame.mixer.Sound(join("assets", "audio", "utilerias", "click_madera.mp3"))
        self.sonidoDeClick.set_volume(1 if self.volumen == "on" else 0)
        
    def actualizarOpcionesMenu(self):
        self.opcionesMenuPrincipal = [
            {
                "name": self.datosLanguage[self.configLanguage]['menu']["playName"],
                "id": self.datosLanguage[self.configLanguage]['menu']["playId"],
                "image": pygame.image.load(join(os.path.join(*self.datosLanguage[self.configLanguage]['menu']["playImage"]))).convert_alpha() # Cargar imagen de la opción
            }, 
            {
                "name": self.datosLanguage[self.configLanguage]['menu']["creditsName"],
                "id": self.datosLanguage[self.configLanguage]['menu']["creditsId"],
                "image": pygame.image.load(join(os.path.join(*self.datosLanguage[self.configLanguage]['menu']["creditsImage"]))).convert_alpha()
            }, 
            {
                "name": self.datosLanguage[self.configLanguage]['menu']["quitName"],
                "id": self.datosLanguage[self.configLanguage]['menu']["quitName"],
                "image": pygame.image.load(join(os.path.join(*self.datosLanguage[self.configLanguage]['menu']["quitImage"]))).convert_alpha()
            }
        ] # Opciones iniciales del menú principal

    def mostrarOpcionesMenu(self, hoverOpcionSeleccionada=None, mostrarIdioma=False): # Opciones del menú principal
        pygame.display.set_caption(f"Menu - {TITLE_GAME}") # Establecemos tituloPrincipalJuego del Menú

        self.fondoPrincipalVideojuego = pygame.image.load(join("assets", "img", "Background", "menu", "fondoinicio.png")).convert_alpha() # Agregar fondoPrincipalVideojuego al menú
        
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
                image.set_alpha(200)  # Set the alpha of the image (opacity level)
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

        # Agregar bandera que posteriormente manejare para cambiar de idioma
        if self.configLanguage == "es":
            imagenBandera = pygame.image.load(join("assets", "img", "BOTONES", "config", "bandera_mexico.png")).convert_alpha() # Cargar imagen de la bandera
        else:
            imagenBandera = pygame.image.load(join("assets", "img", "BOTONES", "config", "bandera_eu.png")).convert_alpha() # Cargar imagen de la bandera

        imagenBandera = pygame.transform.scale(imagenBandera, (50, 50)) # Escalar imagen de la bandera
        bandera_rect = self.screen.blit(imagenBandera, (self.screen.get_width() - 60, 10)) # Mostrar texto en la pantalla

        if mostrarIdioma:
            if self.configLanguage == "es":
                imagenIdioma = pygame.image.load(join("assets", "img", "BOTONES", "config", "bandera_eu.png")).convert_alpha() # Cargar imagen de la bandera
            else:
                imagenIdioma = pygame.image.load(join("assets", "img", "BOTONES", "config", "bandera_mexico.png")).convert_alpha() # Cargar imagen de la bandera

            imagenIdioma = pygame.transform.scale(imagenIdioma, (50, 50)) # Escalar imagen de la bandera
            idioma_rect = self.screen.blit(imagenIdioma, (self.screen.get_width() - 60, 70)) # Mostrar texto en la pantalla
            self.rectOpcionesMenuPrincipal.append(({"id": "idioma"}, idioma_rect))

        # Agregar boton para la musica que simplemente la prende y la apaga
        if self.volumen == "on":
            imagenMusica = pygame.image.load(join("assets", "img", "BOTONES","config", "btnsound.png")).convert_alpha() # Cargar imagen de la bandera
        else:
            imagenMusica = pygame.image.load(join("assets", "img", "BOTONES","config", "btnmute.png")).convert_alpha() # Cargar imagen de la bandera

        imagenMusica = pygame.transform.scale(imagenMusica, (50, 50)) # Escalar imagen de la bandera
        volumen_rect = self.screen.blit(imagenMusica, (self.screen.get_width() - 120, 10)) # Mostrar texto en la pantalla
        pygame.display.flip() # Actualizar pantalla

        self.rectOpcionesMenuPrincipal.append(({"id": "bandera"}, bandera_rect))
        self.rectOpcionesMenuPrincipal.append(({"id": "volumen"}, volumen_rect))

    def mostrarMenuInicial(self):
        hoverOpcionSeleccionada = None # Se usa para manejar el hover 
        mostrarIdioma = False

        # Entramos en un bucle infinito para mostrar el menú
        while self.bucleInicial:
            self.mostrarOpcionesMenu(hoverOpcionSeleccionada, mostrarIdioma)
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
                                game_menu = MenuPlay(self.screen, self.configLanguage, self.datosLanguage, self.volumen)
                                game_menu.mostrarMenuDificultad()
                                continue
                            
                            if option['id'] == "credits":
                                credits = Creditos(self.screen)
                                credits.run()
                                self.bucleInicial = True  # Reiniciar el bucle del menú después de mostrar los créditos
                                # Reproducir la música de fondo nuevamente
                                pygame.mixer.music.load(join("assets", "audio", "music", "let_us_adore_you.mp3"))
                                pygame.mixer.music.play(-1)
                                pygame.mixer.music.set_volume(0.2 if self.volumen == "on" else 0)

                            elif option['id'] == "quit" or option['id'] == "salir":
                                pygame.quit()
                                sys.exit()

                            # Si le da click a la bandera
                            elif option['id'] == "bandera":
                                mostrarIdioma = not mostrarIdioma

                            elif option['id'] == "idioma":
                                self.configLanguage = "en" if self.configLanguage == "es" else "es"
                                self.actualizarOpcionesMenu()  # Actualizar las opciones del menú
                                mostrarIdioma = False

                            elif option['id'] == "volumen":
                                self.volumen = "off" if self.volumen == "on" else "on"
                                pygame.mixer.music.set_volume(1 if self.volumen == "on" else 0)
                                self.sonidoDeClick.set_volume(1 if self.volumen == "on" else 0)  # Actualizar el volumen del sonido de clic
                                if self.volumen == "on":
                                    pygame.mixer.music.load(join("assets", "audio", "music", "let_us_adore_you.mp3"))
                                    pygame.mixer.music.play(-1)
                                    pygame.mixer.music.set_volume(1)
                                
                            else:
                                return option['id']