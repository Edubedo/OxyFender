# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
# Este software no puede ser copiado o redistribuido sin permiso del autor.
import pygame
from utils.settings import *
from os.path import join
from pytmx.util_pygame import load_pygame # Importamos la libreria para cargar el mapa
import sys

class Level1Beginner:
    def __init__(self, name, dificultadNivel, id):
        self.name = name
        self.dificultadNivel = dificultadNivel
        self.id = id

        # Inicializar Pygame y crear una ventana
        pygame.init()
        self.display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(f"{self.name} - {self.dificultadNivel}")
        self.clock = pygame.time.Clock()

        # Cargar el mapa de tiled
        self.tmx_maps = {0: load_pygame('assets/media/data/levels/omni.tmx')}
        print(self.tmx_maps)


    def run(self):
        


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

           



          

            pygame.display.update()
