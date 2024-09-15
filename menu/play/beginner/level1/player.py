from utils.settings import *
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, col):
        super().__init__(groups)
        self.images = self.load_images()
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.animation_index = 0
        self.animation_speed = 0.1

    def load_images(self):
        images = []
        for i in range(1, 6):  # Asumiendo que tienes 4 imágenes para el sprite
            print(i)
            image = pygame.image.load(join("assets", "maps", "beginner","level1","PERS_SPRITE", f"SPRITE_PRIN100%{i}.png")).convert_alpha()
            images.append(image)
        return images

    def update(self, moving):
        if moving:
            self.animation_index += self.animation_speed
            if self.animation_index >= len(self.images):
                self.animation_index = 0
            self.image = self.images[int(self.animation_index)]