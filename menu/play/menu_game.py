# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
# Este software no puede ser copiado o redistribuido sin permiso del autor.
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
        pygame.display.set_caption(f"Select Difficulty - {TITLE_GAME}")  # Establecer titulo del nivel

        self.fondoMenuDificultad = pygame.image.load(join("assets", "img", "FONDOS", "secciones_nivel_fondo.png")).convert_alpha()  # Fondo para menu de selección de dificultad
        self.fondoMenuDificultad = pygame.transform.scale(self.fondoMenuDificultad, (WIDTH, HEIGHT))
        
        self.screen.blit(self.fondoMenuDificultad, [0, 0])

        # Agregar el título de mostrar dificultad
        fontTitulo = pygame.font.Font(join("assets", "fonts", "Transformers Movie.ttf"), 100)
        titulo = fontTitulo.render("Select Difficulty", True, AZUL_TITULO)
        titulo_rect = titulo.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(titulo, titulo_rect)
        
        opcionesDificultad = [
            {
                "name": "Beginner",
                "id": "beginner",
                "image": pygame.image.load(join("assets", "img", "BOTONES", "b_beginner.png")).convert_alpha()
            },
            {
                "name": "Advanced",
                "id": "advanced",
                "image": pygame.image.load(join("assets", "img", "BOTONES", "b_advanced.png")).convert_alpha()
            }
        ]
        
        self.dictMostrarOpcionesDificultad = []

        # Dibujamos las opciones de dificultad
        margin = 20
        start_y = 300  # Ajustar este valor para mover los botones más arriba

        for i, opcionDificultad in enumerate(opcionesDificultad):
            image = opcionDificultad['image']
            image_rect = image.get_rect(center=(self.screen.get_width() // 2, start_y + i * (image.get_height() + margin)))
            self.screen.blit(image, image_rect)
            self.dictMostrarOpcionesDificultad.append((opcionDificultad, image_rect))
        
        # Crear botón de regreso
        back_button = pygame.image.load(join("assets","img","BOTONES","b_regreso.png")).convert_alpha()
        back_button = pygame.transform.scale(back_button, (back_button.get_width() - 10, back_button.get_height() - 10))
        back_button_rect = back_button.get_rect(topleft=(40, HEIGHT - 100))
        self.screen.blit(back_button, back_button_rect)
        
        # Agregar nombre de la empresa
        fontTextoInferiorDerecha = pygame.font.Font(join("assets", "fonts", "Font_Name_Enterprise.ttf"), 24)  # Fuente
        textoInferiorDerecha = fontTextoInferiorDerecha.render(NAME_ENTERPRISE, True, WHITE)  # Texto
        texto_rect = textoInferiorDerecha.get_rect(bottomright=(self.screen.get_width() - 10, self.screen.get_height() - 10))  # Rectangulo para mostrar el texto en la pantalla
        self.screen.blit(textoInferiorDerecha, texto_rect)  # Mostrar texto en la pantalla

        pygame.display.flip()

        hoverOpcionSeleccionadaDificultad = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Cuando hace hover con el mouse
                elif event.type == pygame.MOUSEMOTION:
                    hoverOpcionSeleccionadaDificultad = None  # Establecer el hover como vacío
                    for i, (_, rect) in enumerate(self.dictMostrarOpcionesDificultad):  # Recorrer las opciones de dificultad
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
                image = opcionDificultad['image']
                if i == hoverOpcionSeleccionadaDificultad:
                    image = pygame.transform.scale(image, (image.get_width() + 10, image.get_height() + 10))
                image_rect = image.get_rect(center=(self.screen.get_width() // 2, start_y + i * (image.get_height() + margin)))
                self.screen.blit(image, image_rect)
            
            # Las ponemos hasta abajo para que esten encima de todos

            # Pintar el botón de regreso
            self.screen.blit(back_button, back_button_rect)
            # Pinta el texto de la empresa
            self.screen.blit(textoInferiorDerecha, texto_rect)

            pygame.display.flip()

    def mostrarMenuNiveles(self, dificultadNivel):
        pygame.display.set_caption(f"Select Level - {TITLE_GAME}")  # Establecer titulo del nivel

        self.fondoMenuDificultad = pygame.image.load(join("assets", "img", "FONDOS", "secciones_nivel_fondo.png")).convert_alpha()
        self.fondoMenuDificultad = pygame.transform.scale(self.fondoMenuDificultad, (WIDTH, HEIGHT))  # Escalar imagen
        self.option_rects = []
        
        self.screen.blit(self.fondoMenuDificultad, [0, 0])

        # Agregar el título de mostrar nivel
        fontTitulo = pygame.font.Font(join("assets", "fonts", "Transformers Movie.ttf"), 100)
        titulo = fontTitulo.render("Select Level", True, AZUL_TITULO)
        titulo_rect = titulo.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(titulo, titulo_rect)

        # Agregar nombre de la empresa
        fontTextoInferiorDerecha = pygame.font.Font(join("assets", "fonts", "Font_Name_Enterprise.ttf"), 24)  # Fuente
        textoInferiorDerecha = fontTextoInferiorDerecha.render(NAME_ENTERPRISE, True, WHITE)  # Texto
        texto_rect = textoInferiorDerecha.get_rect(bottomright=(self.screen.get_width() - 10, self.screen.get_height() - 10))  # Rectangulo para mostrar el texto en la pantalla
        self.screen.blit(textoInferiorDerecha, texto_rect)  # Mostrar texto en la pantalla

        opcionNiveles = []

        for i in range(1, 4):
            opcionNiveles.append({
                "name": f"Level {i}",
                "dificultadNivel": dificultadNivel['name'],
                "id": f"{dificultadNivel['id'].lower()}_level_{i}",
                "image": pygame.image.load(join("assets", "img", "BOTONES", f"img_level{i}.png")).convert_alpha()
            })

        # Dibujamos las opciones de niveles
        margin = 20
        total_width = sum(level['image'].get_width() for level in opcionNiveles) + margin * (len(opcionNiveles) - 1)
        start_x = (self.screen.get_width() - total_width) // 2
        start_y = self.screen.get_height() // 2 - 100  # Ajustar este valor para mover los botones más arriba

        for i, level in enumerate(opcionNiveles):
            image = level['image']
            image_rect = image.get_rect(topleft=(start_x + i * (image.get_width() + margin), start_y))
            self.screen.blit(image, image_rect)
            self.option_rects.append((level, image_rect))
        
        # Crear botón de regreso
        back_button = pygame.image.load(join("assets","img","BOTONES","b_regreso.png")).convert_alpha()
        back_button = pygame.transform.scale(back_button, (back_button.get_width() - 10, back_button.get_height() - 10))
        back_button_rect = back_button.get_rect(topleft=(40, HEIGHT - 100))
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
                            break
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
                image = level['image']
                if i == hoverOpcionSeleccionadaNiveles:
                    image = pygame.transform.scale(image, (image.get_width() + 5, image.get_height() + 5))
                image_rect = image.get_rect(topleft=(start_x + i * (image.get_width() + margin), start_y))
                self.screen.blit(image, image_rect)
            
            # Las ponemos hasta abajo para que esten encima de todo

            # Pintar el botón de regreso
            self.screen.blit(back_button, back_button_rect)
            # Pinta el texto de la empresa
            self.screen.blit(textoInferiorDerecha, texto_rect)

            pygame.display.flip()