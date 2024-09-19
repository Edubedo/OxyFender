import pygame
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.images_right = self.load_images("right")
        self.images_left = self.load_images("left")
        self.images = self.images_right  # Default to right images
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.animation_index = 0
        self.animation_speed = 0.1
        self.direction = "right"  # Default direction

    def load_images(self, direction):
        images = []
        for i in range(1, 6):  # Asumiendo que tienes 5 imágenes para el sprite
            image = pygame.image.load(join("assets", "sprites", "character", direction, f"SPRITE_PRIN100%{i}.png")).convert_alpha()
            images.append(image)
        return images

    def update(self, moving, direction):
        if direction != self.direction:
            self.direction = direction
            self.images = self.images_right if direction == "right" else self.images_left

        if moving:
            self.animation_index += self.animation_speed
            if self.animation_index >= len(self.images):
                self.animation_index = 0
            self.image = self.images[int(self.animation_index)]
        # Ajustar la posición del rectángulo de colisión
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
