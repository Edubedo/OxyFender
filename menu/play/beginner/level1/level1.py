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
        self.elevador_sprites = pygame.sprite.Group()  # Creamos un grupo de sprites para los elevadores

        self.tmx_mapa_1 = load_pygame(join("assets", "maps", "beginner", "level1", "SCIENCE.tmx"))  # Cargamos el mapa del nivel 1

        self.camera_offset = pygame.Vector2(0, 0)  # Agregamos esta variable para que la camara siga al jugador

        self.player = None  # Agregamos esta variable para asignar el jugador jugador

        self.last_elevator = None  # Último elevador al que fue teletransportado
        self.teleport_cooldown = 1000  # Tiempo de espera en milisegundos
        self.last_teleport_time = 0  # Última vez que se teletransportó

        self.setup(self.tmx_mapa_1)

    def setup(self, tmx_mapa_1):
        self.tmx_tileset = pygame.image.load(join("assets", "maps", "beginner", "level1", "lab_tileset_LITE.png")).convert_alpha()  # Texturas del piso y techo

        self.posicion_x_personaje = 0  # Agregamos esta variable para la posicion del personaje

        # Agregamos las colisiones de las capas del mapa
        for layer_name in [ 'prtatras', 'Suelo', 'Paredes', 'Techo', 'FondoPiso1', 'FondoPiso2', 'Ascensor']:
            for x, y, surf in tmx_mapa_1.get_layer_by_name(layer_name).tiles():

                # Estructuras
                sprite = Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.todos_los_sprites)

                # Colisiones
                if layer_name in ['Paredes', 'Suelo', 'Techo']:
                    self.colisiones_sprites.add(sprite)
                # Elevadores
                if layer_name == 'Ascensor':
                    self.elevador_sprites.add(sprite)

        # Personaje
        self.player = Player((100, 420), self.todos_los_sprites)  # ! Establecer posicion del jugador de tiled

        self.run()

    def run(self):
        clock = pygame.time.Clock()
        gravity = 0.30
        jump_strength = -7  # Ajustar la fuerza del salto
        max_fall_speed = 4
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
                on_ground = False  # El jugador ya no está en el suelo después de saltar

            # Aplicar gravedad solo si no está en el suelo
            if not on_ground:
                player_velocity_y += gravity
                if player_velocity_y > max_fall_speed:
                    player_velocity_y = max_fall_speed
            player_movement.y += player_velocity_y

            # Mover al jugador y verificar colisiones verticales
            self.player.rect.y += player_movement.y
            collided_sprites = pygame.sprite.spritecollide(self.player, self.colisiones_sprites, False)
            for sprite in collided_sprites:
                if player_movement.y > 0:  # Bajando
                    self.player.rect.bottom = sprite.rect.top
                    on_ground = True
                    player_velocity_y = 0
                elif player_movement.y < 0:  # Subiendo
                    self.player.rect.top = sprite.rect.bottom
                    player_velocity_y = 0

            # Mover al jugador y verificar colisiones horizontales
            self.player.rect.x += player_movement.x
            collided_sprites = pygame.sprite.spritecollide(self.player, self.colisiones_sprites, False)
            for sprite in collided_sprites:
                if player_movement.x > 0:  # Moviéndose a la derecha
                    self.player.rect.right = sprite.rect.left
                elif player_movement.x < 0:  # Moviéndose a la izquierda
                    self.player.rect.left = sprite.rect.right

            # Verificar colisiones con elevadores
            current_time = pygame.time.get_ticks()
            collided_elevators = pygame.sprite.spritecollide(self.player, self.elevador_sprites, False)
            if collided_elevators and current_time - self.last_teleport_time > self.teleport_cooldown:
                # Teletransportar al jugador al otro elevador
                for elevator in self.elevador_sprites:
                    if elevator not in collided_elevators and elevator != self.last_elevator:
                        self.player.rect.topleft = elevator.rect.topleft
                        self.last_elevator = elevator
                        self.last_teleport_time = current_time
                        break

            self.camera_offset.x = self.player.rect.centerx - self.mostrar_superficie.get_width() // 2
            self.camera_offset.y = self.player.rect.centery - self.mostrar_superficie.get_height() // 2

            self.todos_los_sprites.update(moving)

            self.mostrar_superficie.fill(BACKGROUND_COLOR)
            for sprite in self.todos_los_sprites:
                self.mostrar_superficie.blit(sprite.image, sprite.rect.topleft - self.camera_offset)

            pygame.display.flip()

            clock.tick(FPS)