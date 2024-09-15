import pygame
from utils.settings import *
from os.path import join
from pytmx.util_pygame import load_pygame
import sys
from menu.play.beginner.level1.sprites import Sprite
from menu.play.beginner.level1.player import Player
from random import uniform

class Level1Beginner: # Creamos el nivel 1
    def __init__(self, name, dificultadNivel, id):
        self.name = name
        self.dificultadNivel = dificultadNivel
        self.id = id

        self.mostrar_superficie = pygame.display.get_surface()

        self.todos_los_sprites = pygame.sprite.Group()

        self.tmx_mapa_1 = load_pygame(join("assets", "maps", "beginner", "level1", "SCIENCE.tmx"))

        self.camera_offset = pygame.Vector2(0, 0) # Agregamos esta variable para que la camara siga al jugador

        self.player = None  # Agregamos esta variable para asignar el jugador jugador
 
        self.setup(self.tmx_mapa_1)

    def setup(self, tmx_mapa_1):
        self.tmx_tileset = pygame.image.load(join("assets", "maps", "beginner", "level1", "lab_tileset_LITE.png")).convert_alpha() # Texturas del piso y techo
       
        self.posicion_x_personaje = 0


        # Agregamos las colisiones de las capas del mapa
        for layer_name in ['Suelo', 'Paredes', 'Techo', 'FondoPiso1', 'FondoPiso2', 'Ascensor']:
            for x, y, surf in tmx_mapa_1.get_layer_by_name(layer_name).tiles():
                # img = self.get_texture(surf)
                if layer_name == 'Paredes':
                    Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.todos_los_sprites, "BLACK")
                elif layer_name == 'Suelo':
                    print("surf: ", surf)
                    Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.todos_los_sprites, "WHITE")
                elif layer_name == 'Techo':
                    Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.todos_los_sprites, "RED")
                elif layer_name == 'FondoPiso1':
                    Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.todos_los_sprites, "ORANGE")
                elif layer_name == 'FondoPiso2':
                    Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.todos_los_sprites, "BLUE")
                elif layer_name == 'Ascensor':
                    Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.todos_los_sprites, "GREEN")
        self.player = Player((300, 300), self.todos_los_sprites)
        

        self.run()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed() # Tenemos que agregar esta funciona para hacer que el jugador se mueva
            if keys[pygame.K_LEFT]:
                self.player.rect.x -= PLAYER_VEL
            if keys[pygame.K_RIGHT]:
                self.player.rect.x += PLAYER_VEL
            if keys[pygame.K_UP]:
                self.player.rect.y -= PLAYER_VEL
            if keys[pygame.K_DOWN]:
                self.player.rect.y += PLAYER_VEL

            self.camera_offset.x = self.player.rect.centerx - self.mostrar_superficie.get_width() // 2
            self.camera_offset.y = self.player.rect.centery - self.mostrar_superficie.get_height() // 2

            self.todos_los_sprites.update()

            self.mostrar_superficie.fill(BACKGROUND_COLOR)
            for sprite in self.todos_los_sprites:
                self.mostrar_superficie.blit(sprite.image, sprite.rect.topleft - self.camera_offset)

            pygame.display.flip()

            clock.tick(FPS)
    
    