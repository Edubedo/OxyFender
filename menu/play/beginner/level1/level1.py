# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
# Este software no puede ser copiado o redistribuido sin permiso del autor.
import pygame
from utils.settings import *
from os.path import join
from pytmx.util_pygame import load_pygame # Importamos la libreria para cargar el mapa
import sys
from menu.play.beginner.level1.sprites import Sprite
from menu.play.beginner.level1.player import Player
from random import uniform # Importamos la libreria para generar numeros aleatorios

class Level1Beginner:
    def __init__(self,tmx_map, name, dificultadNivel, id):
        # Datos generales el nivel
        self.name = name
        self.dificultadNivel = dificultadNivel
        self.id = id

        self.display_surface = pygame.display.get_surface() # Obtenemos la superficie de la pantalla

        # Groups
        self.all_sprites = pygame.sprite.Group() # Creamos un grupo para todos los sprites(Objetos)
        self.setup(tmx_map) # Llamamos al metodo setup para cargar los objetos del nivel

        # Layer de abi
        self.tmx_mapAbi = load_pygame(join("assets","maps","beginner","level1","SCIENCE.tmx"))
        print("self.tmx_mapAbi; ",self.tmx_mapAbi)
        # for layer in self.tmx_mapAbi.layers:
        #     print(layer.name)
            
            # Verificar si la capa es "Cableado" y tiene objetos
            # if layer.name == "Cableado":
            #     for obj in layer.objects:
            #         print(f"Object: {obj.name}, Type: {obj.type}, X: {obj.x}, Y: {obj.y}, Width: {obj.width}, Height: {obj.height}")

            # for obj in layer.objects:
            #     print(obj)
       
    def setup(self, tmx_map):
        # Agregamos el mapa
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles(): # Obtenemos un objeto de tiled llamado terrain
            Sprite((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites) # Creamos un objeto de la clase Sprite con las coordenadas y la imagen del objeto
    
        # Agregamos el jugador creando el Sprite Player
        for obj in tmx_map.get_layer_by_name('Objects'): # Obtenemos un objeto de tiled llamado objects
            if obj.name == 'player': # Buscamos el objeto player en el mapa
                Player((obj.x, obj.y), self.all_sprites)
                
    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update all sprites
            self.all_sprites.update()

            # Draw everything
            self.display_surface.fill(BLACK)
            self.all_sprites.draw(self.display_surface)

            pygame.display.flip()

            # Cap the frame rate
            clock.tick(60)