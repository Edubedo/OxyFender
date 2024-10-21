import pygame
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        # Cargar todas las imágenes necesarias para cada estado
        self.images_run_right = self.cargar_imagenes("run", "right", 8)
        self.images_run_left = self.cargar_imagenes("run", "left", 8)
        self.images_jump_right = self.cargar_imagenes("jump", "right", 8)  # 8 imágenes para el salto
        self.images_jump_left = self.cargar_imagenes("jump", "left", 8)
        self.images_idle_right = self.cargar_imagenes("idle", "right", 2)
        self.images_idle_left = self.cargar_imagenes("idle", "left", 2)

        # Estado inicial
        self.images = self.images_idle_right
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.animation_index = 0

        # Velocidades de animación para diferentes estados
        self.run_animation_speed = 0.2
        self.idle_animation_speed = 0.05  # Más lenta para idle
        self.jump_animation_speed = 0.03  # Hacer aún más lenta la animación de salto
        self.current_animation_speed = self.idle_animation_speed  # Inicialmente idle

        self.direction = "right"  # Dirección inicial
        self.state = "idle"  # Estado inicial

        # Cargar el sonido de caminar
        self.sonido_pasos = pygame.mixer.Sound(join("assets", "audio", "jugador", "caminar_concreto.mp3"))
        self.sonido_pasos.set_volume(0)

    def cargar_imagenes(self, action, direction, num_images):
        images = []
        for i in range(0, num_images):
            image = pygame.image.load(join("assets", "sprites", "character2", action, direction, f"SPRITE_PRIN100%{i}.png")).convert_alpha()
            images.append(image)
        return images

    def actualizar_estado(self, moving, jumping):
        # Actualizar el estado según el movimiento y el salto
        if jumping:
            self.state = "jumping"
        elif moving:
            self.state = "running"
        else:
            self.state = "idle"

    def update(self, moving, direction, juegoPausado, jumping):
        # Actualizar dirección si ha cambiado
        if direction != self.direction:
            self.direction = direction

        # Actualizar estado del personaje
        self.actualizar_estado(moving, jumping)

        # Seleccionar las imágenes y la velocidad adecuada según el estado y la dirección
        if self.state == "jumping":
            self.images = self.images_jump_right if self.direction == "right" else self.images_jump_left
            self.current_animation_speed = self.jump_animation_speed
        elif self.state == "running":
            self.images = self.images_run_right if self.direction == "right" else self.images_run_left
            self.current_animation_speed = self.run_animation_speed
        else:  # Estado idle
            self.images = self.images_idle_right if self.direction == "right" else self.images_idle_left
            self.current_animation_speed = self.idle_animation_speed

        # Manejar la animación
        self.animation_index += self.current_animation_speed
        if self.animation_index >= len(self.images):
            self.animation_index = 0
        self.image = self.images[int(self.animation_index)]

        # Ajustar la posición del rectángulo de colisión
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

        # Reproducir o detener el sonido de pasos
        if self.state == "running" and not self.sonido_pasos.get_num_channels():
            self.sonido_pasos.play()
        else:
            self.sonido_pasos.stop()
