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

        # Layer de abi
        self.tmx_mapAbi = load_pygame(join("assets","maps","beginner","level1","SCIENCE.tmx"))

        self.setup(self.tmx_mapAbi) # Llamamos al metodo setup para cargar los objetos del nivel
        
            
            # Verificar si la capa es "Cableado" y tiene objetos
            # if layer.name == "Cableado":
            #     for obj in layer.objects:
            #         print(f"Object: {obj.name}, Type: {obj.type}, X: {obj.x}, Y: {obj.y}, Width: {obj.width}, Height: {obj.height}")

            # for obj in layer.objects:
            #     print(obj)
       
    # Establecemos el mapa principal
    def setup(self, tmx_map):
        # Agregamos el mapa
        self.posicion_x_personaje = 0
        # Agregamos el suelo del mapa
        for x, y, surf in tmx_map.get_layer_by_name('Suelo').tiles(): 
            Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.all_sprites, "RED") 

        # Agregamos las paredes del mapa
        for x, y, surf in tmx_map.get_layer_by_name('Paredes').tiles():
            Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.all_sprites, "GREEN") 

        # Agregamos el techo del mapa
        for x, y, surf in tmx_map.get_layer_by_name('Techo').tiles(): 
            Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.all_sprites, "ORANGE") 

        # Agregamos la pared del piso 1
        for x, y, surf in tmx_map.get_layer_by_name('Techo').tiles(): 
            Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.all_sprites, "ORANGE") 

        # Agregamos el fondo del piso 1
        for x, y, surf in tmx_map.get_layer_by_name('FondoPiso1').tiles(): 
            Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.all_sprites, "WHITE") 

        # Agregamos el fondo del piso 2
        for x, y, surf in tmx_map.get_layer_by_name('FondoPiso2').tiles(): 
            Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.all_sprites, "WHITE") 

        # Agregamos el fondo del ascensor
        for x, y , surf in tmx_map.get_layer_by_name("Ascensor").tiles():
            Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.all_sprites, "BLUE")

        # Agregamos el jugador creando el Sprite Player
        # for obj in tmx_map.get_layer_by_name('Objects'): # Obtenemos un objeto de tiled llamado objects
        #     if obj.name == 'player': # Buscamos el objeto player en el mapa
        #         Player((obj.x, obj.y), self.all_sprites)

        self.run() # Ejecutamos juego

    # Empezar a jugar     
    def run(self):
        clock = pygame.time.Clock()

        print("Ejecutando juego")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Mover el jugador
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        print("Izquierda")
                        self.posicion_x_personaje -= 10
                    if event.key == pygame.K_RIGHT:
                        print("Derecha")
                        self.posicion_x_personaje -= 10
                    if event.key == pygame.K_UP:
                        print("Arriba")
                    if event.key == pygame.K_DOWN:
                        print("Abajo")
            # Actualizamos todos los sprite
            self.all_sprites.update()

            # Rellenamos el fondo
            self.display_surface.fill(BLACK)
            self.all_sprites.draw(self.display_surface)

            

            #  Actualizamos los surface del juego
            pygame.display.flip()

            # Establecemos los FPS del juego
            clock.tick(60)