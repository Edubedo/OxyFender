import pygame
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.images_right = self.cargar_imagenes("right")
        self.images_left = self.cargar_imagenes("left")
        self.images_jump_right = self.cargar_imagenes("jump", "right", 8)
        self.images_jump_left = self.cargar_imagenes("jump", "left", 8)
        self.images_idle = pygame.image.load(join("assets", "sprites", "character2", "right", "SPRITE_PRIN100%0.png")).convert_alpha()
        self.images = self.images_right  # Default to right images
        self.image = self.images_idle
        self.rect = self.image.get_rect(topleft=pos)
        self.animation_index = 0
        self.animation_speed = 0.1
        self.direction = "right"  # Default direction
        self.state = "idle"  # Possible states: idle, running, jumping
        
        # Cargar el sonido de caminar
        self.sonido_pasos = pygame.mixer.Sound(join("assets", "audio", "jugador", "caminar_concreto.mp3"))
        self.sonido_pasos.set_volume(0)

    def cargar_imagenes(self, action, direction=None, num_images=6):
        images = []
        if direction:
            for i in range(0, num_images):
                image = pygame.image.load(join("assets", "sprites", "character2", action, direction, f"SPRITE_PRIN100%{i}.png")).convert_alpha()
                images.append(image)
        else:
            for i in range(0, num_images):
                image = pygame.image.load(join("assets", "sprites", "character2", action, f"SPRITE_PRIN100%{i}.png")).convert_alpha()
                images.append(image)
        return images

    def update(self, moving, direction, juegoPausado, jumping):
        if direction != self.direction:
            self.direction = direction
            self.images = self.images_right if direction == "right" else self.images_left

        if jumping:
            self.state = "jumping"
            self.images = self.images_jump_right if self.direction == "right" else self.images_jump_left
            self.animation_index += self.animation_speed
            if self.animation_index >= len(self.images):
                self.animation_index = 0
                self.state = "idle"  # Reset to idle after jump
            self.image = self.images[int(self.animation_index)]
        elif moving and not juegoPausado:
            if self.state != "jumping":  # Only change to running if not jumping
                self.state = "running"
                self.animation_index += self.animation_speed
                if self.animation_index >= len(self.images):
                    self.animation_index = 0
                self.image = self.images[int(self.animation_index)]
                
                # Reproducir el sonido de caminar si no está ya reproduciéndose
                if not self.sonido_pasos.get_num_channels():
                    self.sonido_pasos.play()

                if self.rect.left < 0:  # Establece el limite de lado izquierdo para no salir del mapa
                    self.rect.left = 0
        else:
            if self.state != "jumping":  # Only change to idle if not jumping
                self.state = "idle"
                self.image = self.images_idle
                self.sonido_pasos.stop()

        # Ajustar la posición del rectángulo de colisión
        self.rect = self.image.get_rect(topleft=self.rect.topleft)