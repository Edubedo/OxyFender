import pygame
from utils.settings import *


# Importamos las librerias de los niveles 
from menu.play.beginner.level1.level1 import Level1Beginner
from menu.play.beginner.level2.level2 import Level2Beginner
from menu.play.beginner.level3.level3 import Level3Beginner

from menu.play.advanced.level1.level1 import Level1Advanced
from menu.play.advanced.level2.level2 import Level2Advanced
from menu.play.advanced.level3.level3 import Level3Advanced
from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame
from os.path import join

class MenuGame:
    def __init__(self, screen, config):
        pygame.display.set_caption(f"Seleccionar Nivel - {TITLE_GAME}")
        self.screen = screen
        self.config = config
        self.font = pygame.font.Font(join("assets", "fonts", "Font_Menu_Options.ttf"), 18) # Fuente de texto

    def mostrarMenuDificultad(self):
        self.background = pygame.image.load(join("assets", "img", "Background", "menu", "BackgroundProvisional2.jpg")).convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        
        self.screen.blit(self.background, [0, 0])
        self.option_rects = []

        # Agregar el título de mostrar dificultad
        fontTitulo = pygame.font.Font(join("assets", "fonts", "Triforce.ttf"), 100)
        titulo = fontTitulo.render("Seleccionar Dificultad", True, BLACK)
        titulo_rect = titulo.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(titulo, titulo_rect)

        if self.config.obtenerLenguajeActual() == "english":
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
        else: 
            opcionesDificultad = [
                {
                "name" : "Principiante",
                "id": "beginner"
                },
                {
                "name" : "Avanzado",
                "id": "advanced"
                }
            ] 
        
        self.dictMostrarOpcionesDificultad = []  

        # Dibujamos las opciones de dificultad
        for i, opcionDificultad in enumerate(opcionesDificultad):
            textDificulad = self.font.render(opcionDificultad['name'], True, WHITE)
            background_rect = pygame.Surface((BUTTON_MENU_WIDTH, BUTTON_MENU_HEIGHT))
            background_rect.fill(DARK_BLUE)
            text_rect = textDificulad.get_rect(topleft=(10, BUTTON_MENU_HEIGHT // 2 - textDificulad.get_height() // 2))
            background_rect.blit(textDificulad, text_rect.topleft)
            rectDificultad = background_rect.get_rect(topleft=(0, 150 + i * 70))
            self.screen.blit(background_rect, rectDificultad)
            self.dictMostrarOpcionesDificultad.append((opcionDificultad, rectDificultad))
        pygame.display.flip()

        indice_opcion_curso_encima = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEMOTION:
                    indice_opcion_curso_encima = None
                    for i, (_, rect) in enumerate(self.dictMostrarOpcionesDificultad):
                        if rect.collidepoint(event.pos):
                            indice_opcion_curso_encima = i
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                            break
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for opcionDificultad, rectDificultad in self.dictMostrarOpcionesDificultad:
                        if rectDificultad.collidepoint(event.pos):
                            return self.mostrarMenuNiveles(opcionDificultad)
            
            self.screen.blit(self.background, [0, 0])
            self.screen.blit(titulo, titulo_rect)
            for i, (opcionDificultad, rectDificultad) in enumerate(self.dictMostrarOpcionesDificultad):
                if i == indice_opcion_curso_encima:
                    textDificulad = self.font.render(opcionDificultad['name'], True, WHITE)
                    background_rect = pygame.Surface((BUTTON_MENU_WIDTH, BUTTON_MENU_HEIGHT))
                    background_rect.fill(LIGHTBLUE)
                else:
                    textDificulad = self.font.render(opcionDificultad['name'], True, WHITE)
                    background_rect = pygame.Surface((BUTTON_MENU_WIDTH, BUTTON_MENU_HEIGHT))
                    background_rect.fill(DARK_BLUE)
                text_rect = textDificulad.get_rect(topleft=(10, BUTTON_MENU_HEIGHT // 2 - textDificulad.get_height() // 2))
                background_rect.blit(textDificulad, text_rect.topleft)
                self.screen.blit(background_rect, rectDificultad)
            pygame.display.flip()

    def mostrarMenuNiveles(self, dificultadNivel):
        self.background = pygame.image.load(join("assets", "img", "Background", "menu", "BackgroundProvisional2.jpg")).convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        
        self.screen.blit(self.background, [0, 0])
        self.option_rects = []

        # Agregar el título de mostrar nivel
        fontTitulo = pygame.font.Font(join("assets", "fonts", "Triforce.ttf"), 100)
        titulo = fontTitulo.render("Seleccionar Nivel", True, BLACK)
        titulo_rect = titulo.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(titulo, titulo_rect)

        opcionNiveles = []

        for i in range(1, 4):
            opcionNiveles.append({
                "name": f"Level {i}",
                "dificultadNivel": dificultadNivel['name'],
                "id": f"{dificultadNivel['id'].lower()}_level_{i}"
            })

        self.option_rects = []  
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
        pygame.display.flip()

        indice_opcion_curso_encima = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
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
            
            self.screen.blit(self.background, [0, 0])
            self.screen.blit(titulo, titulo_rect)
            for i, (level, rectNivel) in enumerate(self.option_rects):
                if i == indice_opcion_curso_encima:
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
            pygame.display.flip()
