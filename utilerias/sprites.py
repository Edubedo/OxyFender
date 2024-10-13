import pygame
from os.path import join
from utilerias.configuraciones import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

class FiltroSprite(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.images = [
            pygame.image.load(join("assets", "img", "sprites", "filtro", "FILTRO1.png")).convert_alpha(),
            pygame.image.load(join("assets", "img", "sprites", "filtro", "FILTRO2.png")).convert_alpha(),
            pygame.image.load(join("assets", "img", "sprites", "filtro", "FILTRO3.png")).convert_alpha(),
            pygame.image.load(join("assets", "img", "sprites", "filtro", "FILTRO4.png")).convert_alpha(),
            pygame.image.load(join("assets", "img", "sprites", "filtro", "FILTRO5.png")).convert_alpha(),
            pygame.image.load(join("assets", "img", "sprites", "filtro", "FILTRO6.png")).convert_alpha()
        ]
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect(topleft=pos)
        self.animation_time = 100  # Time in milliseconds for each frame
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_time:
            self.last_update = now
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image = self.images[self.current_image]