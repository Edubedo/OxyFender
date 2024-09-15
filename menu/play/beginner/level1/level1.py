import pygame
from utils.settings import *
from os.path import join
from pytmx.util_pygame import load_pygame
import sys
from menu.play.beginner.level1.sprites import Sprite
from menu.play.beginner.level1.player import Player
from random import uniform

class Level1Beginner:  # Creamos el nivel 1
    def __init__(self, name, dificultadNivel, id):
        self.name = name
        self.dificultadNivel = dificultadNivel
        self.id = id

        self.mostrar_superficie = pygame.display.get_surface()

        self.todos_los_sprites = pygame.sprite.Group()  # Creamos un grupo de sprites para todos los sprites
        self.colisiones_sprites = pygame.sprite.Group()  # Creamos un grupo de sprites para las colisiones

        self.tmx_mapa_1 = load_pygame(join("assets", "maps", "beginner", "level1", "SCIENCE.tmx"))  # Cargamos el mapa del nivel 1

        self.camera_offset = pygame.Vector2(0, 0)  # Agregamos esta variable para que la camara siga al jugador

        self.player = None  # Agregamos esta variable para asignar el jugador jugador

        self.setup(self.tmx_mapa_1)

    def setup(self, tmx_mapa_1):
        self.tmx_tileset = pygame.image.load(join("assets", "maps", "beginner", "level1", "lab_tileset_LITE.png")).convert_alpha()  # Texturas del piso y techo

        self.posicion_x_personaje = 0  # Agregamos esta variable para la posicion del personaje

        # Agregamos las colisiones de las capas del mapa
        for layer_name in ['Suelo', 'Paredes', 'Techo', 'FondoPiso1', 'FondoPiso2', 'Ascensor']:
            for x, y, surf in tmx_mapa_1.get_layer_by_name(layer_name).tiles():

                # Estructuras
                sprite = Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.todos_los_sprites)

                # Colisiones
                if layer_name in ['Paredes', 'Suelo', 'Techo']:
                    self.colisiones_sprites.add(sprite)

        # Personaje
        self.player = Player((418, 418), self.todos_los_sprites, 'RED')  # ! Establecer posicion del jugador de tiled

        self.run()

    def run(self):
        clock = pygame.time.Clock()
        gravity = 0.35
        jump_strength = -8
        max_fall_speed = 10
        player_velocity_y = 0
        on_ground = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()  # Tenemos que agregar esta funciona para hacer que el jugador se mueva
            player_movement = pygame.Vector2(0, 0)
            moving = False
            if keys[pygame.K_LEFT]:
                player_movement.x -= PLAYER_VEL
                moving = True
            if keys[pygame.K_RIGHT]:
                player_movement.x += PLAYER_VEL
                moving = True
            if keys[pygame.K_SPACE] and on_ground:
                player_velocity_y = jump_strength

            # Aplicar gravedad solo si no está en el suelo
            if not on_ground:
                player_velocity_y += gravity
                if player_velocity_y > max_fall_speed:
                    player_velocity_y = max_fall_speed
            player_movement.y += player_velocity_y

            # Mover al jugador y verificar colisiones
            self.player.rect.x += player_movement.x
            if pygame.sprite.spritecollide(self.player, self.colisiones_sprites, False):
                self.player.rect.x -= player_movement.x

            self.player.rect.y += player_movement.y
            if pygame.sprite.spritecollide(self.player, self.colisiones_sprites, False):
                self.player.rect.y -= player_movement.y
                player_velocity_y = 0
                on_ground = True
            else:
                on_ground = False

            self.camera_offset.x = self.player.rect.centerx - self.mostrar_superficie.get_width() // 2
            self.camera_offset.y = self.player.rect.centery - self.mostrar_superficie.get_height() // 2

            self.todos_los_sprites.update(moving)

            self.mostrar_superficie.fill(BACKGROUND_COLOR)
            for sprite in self.todos_los_sprites:
                self.mostrar_superficie.blit(sprite.image, sprite.rect.topleft - self.camera_offset)

            pygame.display.flip()

            clock.tick(FPS)