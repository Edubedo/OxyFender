# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
# Este software no puede ser copiado o redistribuido sin permiso del autor.
import pygame
from utils.settings import *

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
        self.screen = screen
        self.config = config
        self.font = pygame.font.Font(None, 36)

        self.tmx_maps = {0: load_pygame(join("assets","media","data","levels","omni.tmx"))}
    def mostrarMenuDificultad(self):
        self.screen.fill(WHITE)

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
            textDificulad = self.font.render(opcionDificultad['name'], True, BLACK)
            rectDificultad = textDificulad.get_rect(topleft=(0, 150 + i * 50))
            self.screen.blit(textDificulad, rectDificultad)
            self.dictMostrarOpcionesDificultad.append((opcionDificultad, rectDificultad))
        pygame.display.flip()

        while True:
            # Cuando el usuario haga click en una de las opciones de dificultad se mostrara el menu de niveles 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for opcionDificultad, rectDificultad in self.dictMostrarOpcionesDificultad:
                        if rectDificultad.collidepoint(event.pos):
                            return self.mostrarMenuNiveles(opcionDificultad)

    def mostrarMenuNiveles(self, dificultadNivel):
        self.screen.fill(WHITE)
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
            textNivel = self.font.render(level['name'], True, BLACK)
            rectNivel = textNivel.get_rect(topleft=(0, 150 + i * 50))
            self.screen.blit(textNivel, rectNivel)
            self.option_rects.append((level, rectNivel))
        pygame.display.flip()

        while True:
            # Cuando el usuario haga click en una de las opciones de niveles se mostrara el nivel seleccionado
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for level, rectNivel in self.option_rects:
                        if rectNivel.collidepoint(event.pos):

                           # Nivekes para principiantes 
                           if level['id'] == "beginner_level_1":
                                self.current_stage = Level1Beginner(self.tmx_maps[0], level['name'], level['dificultadNivel'], level['id']).run()
                           if level['id'] == "beginner_level_2":
                                Level2Beginner(level['name'], level['dificultadNivel'], level['id'])
                           if level['id'] == "beginner_level_3":
                                Level3Beginner(level['name'], level['dificultadNivel'], level['id'])
                           
                           # Niveles para avanzadis 
                           if level['id'] == "advanced_level_1":
                                Level1Advanced(level['name'], level['dificultadNivel'], level['id'])
                           if level['id'] == "advanced_level_2":
                                Level2Advanced(level['name'], level['dificultadNivel'], level['id'])
                           if level['id'] == "advanced_level_3":
                                Level3Advanced(level['name'], level['dificultadNivel'], level['id'])