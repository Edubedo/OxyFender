import pygame
from utils.configuraciones import *
import sys

# Importamos las librerias de los niveles 
from menu.play.beginner.level1.level1 import Level1Beginner
from menu.play.beginner.level2.level2 import Level2Beginner
from menu.play.beginner.level3.level3 import Level3Beginner

from menu.play.advanced.level1.level1 import Level1Advanced
from menu.play.advanced.level2.level2 import Level2Advanced
from menu.play.advanced.level3.level3 import Level3Advanced
from pygame.math import Vector2 as vector
from os.path import join

class MenuPlay:
    def __init__(self, screen, config, bucleInicial):
        # Guardar atributos generales
        self.screen = screen 
        self.config = config
        self.font = pygame.font.Font(join("assets", "fonts", "Font_Menu_Options.ttf"), 18) # Fuente de texto

    def mostrarMenuDificultad(self):
        pygame.display.set_caption(f"Select Difficulty - {TITLE_GAME}") # Establecer titulo del nivel

        self.fondoMenuDificultad = pygame.image.load(join("assets", "img", "Background", "menu", "BackgroundProvisional2.jpg")).convert_alpha() # Fondo para menu de selección de dificultad
        self.fondoMenuDificultad = pygame.transform.scale(self.fondoMenuDificultad, (WIDTH, HEIGHT))
        
        self.screen.blit(self.fondoMenuDificultad, [0, 0])

        # Agregar el título de mostrar dificultad
        fontTitulo = pygame.font.Font(join("assets", "fonts", "Triforce.ttf"), 100)
        titulo = fontTitulo.render("Select Difficulty", True, BLACK)
        titulo_rect = titulo.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(titulo, titulo_rect)
        opcionesDificultad = [
                {
                "name" : "Beginner",
                "id": "beginner"
                },
                {
                "name" : "Advanced",
                "id": "advanced"
                }
            ] 
        
        self.dictMostrarOpcionesDificultad = []  

        # Dibujamos las opciones de dificultad
        for i, opcionDificultad in enumerate(opcionesDificultad):
            textoMostrarDificultad = self.font.render(opcionDificultad['name'], True, WHITE)
            background_rect = pygame.Surface((BUTTON_MENU_WIDTH, BUTTON_MENU_HEIGHT))
            background_rect.fill(DARK_BLUE)
            text_rect = textoMostrarDificultad.get_rect(topleft=(10, BUTTON_MENU_HEIGHT // 2 - textoMostrarDificultad.get_height() // 2))
            background_rect.blit(textoMostrarDificultad, text_rect.topleft)
            rectDificultad = background_rect.get_rect(topleft=(0, 150 + i * 70))
            self.screen.blit(background_rect, rectDificultad)
            self.dictMostrarOpcionesDificultad.append((opcionDificultad, rectDificultad))
        
        # Crear botón de regreso
        back_button = self.font.render("Back", True, WHITE)
        back_button_rect = back_button.get_rect(topleft=(10, HEIGHT - 50))
        self.screen.blit(back_button, back_button_rect)
        
        # Agregar nombre de la empresa
        fontTextoInferiorDerecha = pygame.font.Font(join("assets", "fonts", "Font_Name_Enterprise.ttf"), 24) # Fuente
        textoInferiorDerecha = fontTextoInferiorDerecha.render(NAME_ENTERPRISE, True, BLACK) # Texto
        texto_rect = textoInferiorDerecha.get_rect(bottomright=(self.screen.get_width() - 10, self.screen.get_height() - 10)) # Rectangulo para mostrar el texto en la pantalla
        self.screen.blit(textoInferiorDerecha, texto_rect) # Mostrar texto en la pantalla

        pygame.display.flip()

        hoverOpcionSeleccionadaDificultad = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Cuando hace hover con el mouse
                elif event.type == pygame.MOUSEMOTION:
                    hoverOpcionSeleccionadaDificultad = None # Establecer el hover como vacío
                    for i, (_, rect) in enumerate(self.dictMostrarOpcionesDificultad): # Recorrer las opciones de dificultad
                        # Si el mouse está encima de alguna de las opciones de dificultad cambiar el hombre a la mano y establecer el hover a 1 para despues pintar a azul
                        if rect.collidepoint(event.pos):
                            hoverOpcionSeleccionadaDificultad = i
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                            break
                    # Si el mouse no está encima de ninguna opción de dificultad cambiar el cursor a la flecha
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    
                        # Verificamos si el mouse está encima del botón de regreso para ponerle el curso de mano o de flecha
                        if back_button_rect.collidepoint(event.pos):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        else:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                # Cuando hace click con el mouse                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Recorrer las opciones de dificultad para saber cual fue la seleccionada
                    for opcionDificultad, rectDificultad in self.dictMostrarOpcionesDificultad:
                        if rectDificultad.collidepoint(event.pos):
                            self.mostrarMenuNiveles(opcionDificultad)
                            continue
                    # Si se hace clic en el botón de regreso
                    if back_button_rect.collidepoint(event.pos):
                        return

            # Pintar las opciones de dificultad en la pantalla
            self.screen.blit(self.fondoMenuDificultad, [0, 0])
            self.screen.blit(titulo, titulo_rect)

            for i, (opcionDificultad, rectDificultad) in enumerate(self.dictMostrarOpcionesDificultad):
                if i == hoverOpcionSeleccionadaDificultad:
                    textoMostrarDificultad = self.font.render(opcionDificultad['name'], True, WHITE)
                    background_rect = pygame.Surface((BUTTON_MENU_WIDTH, BUTTON_MENU_HEIGHT))
                    background_rect.fill(LIGHTBLUE)
                else:
                    textoMostrarDificultad = self.font.render(opcionDificultad['name'], True, WHITE)
                    background_rect = pygame.Surface((BUTTON_MENU_WIDTH, BUTTON_MENU_HEIGHT))
                    background_rect.fill(DARK_BLUE)
                text_rect = textoMostrarDificultad.get_rect(topleft=(10, BUTTON_MENU_HEIGHT // 2 - textoMostrarDificultad.get_height() // 2))
                background_rect.blit(textoMostrarDificultad, text_rect.topleft)
                self.screen.blit(background_rect, rectDificultad)
            
            # Las ponemos hasta abajo para que esten encima de todos

            # Pintar el botón de regreso
            self.screen.blit(back_button, back_button_rect)
            # Pinta el texto de la empresa
            self.screen.blit(textoInferiorDerecha, texto_rect)

            pygame.display.flip()

    def mostrarMenuNiveles(self, dificultadNivel):
        pygame.display.set_caption(f"Select Level - {TITLE_GAME}") # Establecer titulo del nivel

        self.fondoMenuDificultad = pygame.image.load(join("assets", "img", "Background", "menu", "BackgroundProvisional2.jpg")).convert_alpha()
        self.fondoMenuDificultad = pygame.transform.scale(self.fondoMenuDificultad, (WIDTH, HEIGHT)) # Escalar imagen
        self.option_rects = []
        
        self.screen.blit(self.fondoMenuDificultad, [0, 0])

        # Agregar el título de mostrar nivel
        fontTitulo = pygame.font.Font(join("assets", "fonts", "Triforce.ttf"), 100)
        titulo = fontTitulo.render("Select Level", True, BLACK)
        titulo_rect = titulo.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(titulo, titulo_rect)

        # Agregar nombre de la empresa
        fontTextoInferiorDerecha = pygame.font.Font(join("assets", "fonts", "Font_Name_Enterprise.ttf"), 24) # Fuente
        textoInferiorDerecha = fontTextoInferiorDerecha.render(NAME_ENTERPRISE, True, BLACK) # Texto
        texto_rect = textoInferiorDerecha.get_rect(bottomright=(self.screen.get_width() - 10, self.screen.get_height() - 10)) # Rectangulo para mostrar el texto en la pantalla
        self.screen.blit(textoInferiorDerecha, texto_rect) # Mostrar texto en la pantalla

        opcionNiveles = []

        for i in range(1, 4):
            opcionNiveles.append({
                "name": f"Level {i}",
                "dificultadNivel": dificultadNivel['name'],
                "id": f"{dificultadNivel['id'].lower()}_level_{i}"
            })

        # Dibujamos las opciones de niveles
        for i, level in enumerate(opcionNiveles):
            textNivel = self.font.render(level['name'], True, WHITE)
            background_rect = pygame.Surface((BUTTON_MENU_WIDTH, BUTTON_MENU_HEIGHT))
            background_rect.fill(DARK_BLUE)
            text_rect = textNivel.get_rect(topleft=(10, BUTTON_MENU_HEIGHT // 2 - textNivel.get_height() // 2))
            background_rect.blit(textNivel, text_rect.topleft)
            rectNivel = background_rect.get_rect(topleft=(0, 150 + i * 70))
            self.screen.blit(background_rect, rectNivel)
            self.option_rects.append((level, rectNivel))
        
        # Crear botón de regreso
        back_button = self.font.render("Back", True, WHITE)
        back_button_rect = back_button.get_rect(topleft=(10, HEIGHT - 50))
        self.screen.blit(back_button, back_button_rect)
        
        
        pygame.display.flip()

        hoverOpcionSeleccionadaNiveles = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    hoverOpcionSeleccionadaNiveles = None
                    for i, (_, rect) in enumerate(self.option_rects):
                        if rect.collidepoint(event.pos):
                            hoverOpcionSeleccionadaNiveles = i
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                            break  # Cambiado de continue a break
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                        # Verificamos si el mouse está encima del botón de regreso para ponerle el curso de mano o de flecha
                        if back_button_rect.collidepoint(event.pos):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        else:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for level, rectNivel in self.option_rects:
                        if rectNivel.collidepoint(event.pos):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Cambiar el cursor al cursor normal
                           # Niveles para principiantes 
                            if level['id'] == "beginner_level_1":
                                    self.current_stage = Level1Beginner(level['name'], level['dificultadNivel'], level['id']).run()
                            if level['id'] == "beginner_level_2":
                                    Level2Beginner(level['name'], level['dificultadNivel'], level['id'])
                            if level['id'] == "beginner_level_3":
                                    Level3Beginner(level['name'], level['dificultadNivel'], level['id'])
                            
                            # Niveles para avanzados 
                            if level['id'] == "advanced_level_1":
                                    Level1Advanced(level['name'], level['dificultadNivel'], level['id'])
                            if level['id'] == "advanced_level_2":
                                    Level2Advanced(level['name'], level['dificultadNivel'], level['id'])
                            if level['id'] == "advanced_level_3":
                                    Level3Advanced(level['name'], level['dificultadNivel'], level['id'])
                    # Si se hace clic en el botón de regreso
                    if back_button_rect.collidepoint(event.pos):
                        return
            
            self.screen.blit(self.fondoMenuDificultad, [0, 0])
            self.screen.blit(titulo, titulo_rect)
            for i, (level, rectNivel) in enumerate(self.option_rects):
                if i == hoverOpcionSeleccionadaNiveles:
                    textNivel = self.font.render(level['name'], True, WHITE)
                    background_rect = pygame.Surface((BUTTON_MENU_WIDTH, BUTTON_MENU_HEIGHT))
                    background_rect.fill(LIGHTBLUE)
                else:
                    textNivel = self.font.render(level['name'], True, WHITE)
                    background_rect = pygame.Surface((BUTTON_MENU_WIDTH, BUTTON_MENU_HEIGHT))
                    background_rect.fill(DARK_BLUE)
                text_rect = textNivel.get_rect(topleft=(10, BUTTON_MENU_HEIGHT // 2 - textNivel.get_height() // 2))
                background_rect.blit(textNivel, text_rect.topleft)
                self.screen.blit(background_rect, rectNivel)
            
            # Las ponemos hasta abajo para que esten encima de todo

            # Pintar el botón de regreso
            self.screen.blit(back_button, back_button_rect)
            # Pinta el texto de la empresa
            self.screen.blit(textoInferiorDerecha, texto_rect)

            pygame.display.flip()