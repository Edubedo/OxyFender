import pygame
from utils.settings import *
from os.path import join
from pytmx.util_pygame import load_pygame
import sys
from menu.play.beginner.level1.sprites import Sprite
from menu.play.beginner.level1.player import Player
from random import uniform

class Level1Beginner:
    def __init__(self, tmx_map, name, dificultadNivel, id):
        self.name = name
        self.dificultadNivel = dificultadNivel
        self.id = id

        self.display_surface = pygame.display.get_surface()

        self.all_sprites = pygame.sprite.Group()

        self.tmx_mapAbi = load_pygame(join("assets", "maps", "beginner", "level1", "SCIENCE.tmx"))

        self.camera_offset = pygame.Vector2(0, 0)
        self.player = None

        self.setup(self.tmx_mapAbi)

    def setup(self, tmx_map):
        self.posicion_x_personaje = 0

        for x, y, surf in tmx_map.get_layer_by_name('Suelo').tiles():
            Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.all_sprites, "RED")

        for x, y, surf in tmx_map.get_layer_by_name('Paredes').tiles():
            Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.all_sprites, "GREEN")

        for x, y, surf in tmx_map.get_layer_by_name('Techo').tiles():
            Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.all_sprites, "ORANGE")

        for x, y, surf in tmx_map.get_layer_by_name('FondoPiso1').tiles():
            Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.all_sprites, "WHITE")

        for x, y, surf in tmx_map.get_layer_by_name('FondoPiso2').tiles():
            Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.all_sprites, "WHITE")

        for x, y, surf in tmx_map.get_layer_by_name("Ascensor").tiles():
            Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.all_sprites, "BLUE")

        self.player = Player((300, 300), self.all_sprites)

        self.run()

    def run(self):
        clock = pygame.time.Clock()

        print("Ejecutando juego")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.rect.x -= PLAYER_VEL
            if keys[pygame.K_RIGHT]:
                self.player.rect.x += PLAYER_VEL
            if keys[pygame.K_UP]:
                self.player.rect.y -= PLAYER_VEL
            if keys[pygame.K_DOWN]:
                self.player.rect.y += PLAYER_VEL

            self.camera_offset.x = self.player.rect.centerx - self.display_surface.get_width() // 2
            self.camera_offset.y = self.player.rect.centery - self.display_surface.get_height() // 2

            self.all_sprites.update()

            self.display_surface.fill(BACKGROUND_COLOR)
            for sprite in self.all_sprites:
                self.display_surface.blit(sprite.image, sprite.rect.topleft - self.camera_offset)

            pygame.display.flip()

            clock.tick(FPS)