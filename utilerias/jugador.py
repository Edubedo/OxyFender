# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
# Este software no puede ser copiado o redistribuido sin permiso del autor.
import pygame
from os.path import join

# jugador.py

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.images_right = self.cargar_imagenes("right")
        self.images_left = self.cargar_imagenes("left")
        self.images = self.images_right  # Default to right images
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.animation_index = 0
        self.animation_speed = 0.1
        self.direction = "right"  # Default direction
        
        # Cargar el sonido de caminar
        self.sonido_pasos = pygame.mixer.Sound(join("assets", "audio", "jugador", "caminar_concreto.mp3"))
        self.sonido_pasos.set_volume(0)

    def cargar_imagenes(self, direction):
        images = []
        for i in range(1, 6):  # Asumiendo que tienes 5 imágenes para el sprite
            image = pygame.image.load(join("assets", "sprites", "character", direction, f"SPRITE_PRIN100%{i}.png")).convert_alpha()
            images.append(image) # append para agregar la imagen a la lista
        return images

    def update(self, moving, direction, juegoPausado):
        if direction != self.direction:
            self.direction = direction
            self.images = self.images_right if direction == "right" else self.images_left

        if moving and not juegoPausado:
            self.animation_index += self.animation_speed
            if self.animation_index >= len(self.images):
                self.animation_index = 0
            self.image = self.images[int(self.animation_index)]
            
            # Reproducir el sonido de caminar si no está ya reproduciéndose
            if not self.sonido_pasos.get_num_channels():
                self.sonido_pasos.play()

            if self.rect.left < 0:  # Establece el limite de lado izquierdo para no salir del mapa
                self.rect.left = 0  # Correctly set the left attribute instead of the entire rect
        else:
            # Detener el sonido de caminar si el personaje deja de moverse o el juego está en pausa
            self.sonido_pasos.stop()

        # Ajustar la posición del rectángulo de colisión
        self.rect = self.image.get_rect(topleft=self.rect.topleft)