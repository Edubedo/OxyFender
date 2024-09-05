# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
# Este software no puede ser copiado o redistribuido sin permiso del autor.
import pygame
from utils.settings import *
from os.path import join

class Level1Beginner:
    def __init__(self, name, dificultadNivel, id):
        self.name = name
        self.dificultadNivel = dificultadNivel
        self.id = id

    def run(self):
        # Inicializar Pygame y crear una ventana
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(f"{self.name} - {self.dificultadNivel}")

        gravedad = 0.5
        x, y = 50, 50
        widthCuadrado, heightCuadrado = 40, 60
        is_jumping = False  # Variable para controlar el salto
        y_velocity = 0  # Velocidad vertical del personaje

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Obtener teclas presionadas
            keys = pygame.key.get_pressed()

            # Movimiento del personaje
            if keys[pygame.K_LEFT]:
                x -= PLAYER_VEL
            if keys[pygame.K_RIGHT]:
                x += PLAYER_VEL
            if keys[pygame.K_DOWN]:
                y += PLAYER_VEL
            if keys[pygame.K_SPACE] and not is_jumping:
                y_velocity -= 15
                is_jumping = True

            # Manejar la gravedad y el salto
            y_velocity += gravedad
            y += y_velocity
            if y > (HEIGHT - heightCuadrado):
                y = (HEIGHT - heightCuadrado)
                y_velocity = 0
                is_jumping = False  # Restablecer el salto cuando toca el suelo

            # Limpiar la pantalla
            self.background = pygame.image.load(join("assets", "maps", "beginner", "laboratorio.webp")).convert_alpha() # Cargamos la imagen de fondo
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

            screen.blit(self.background, [0, 0])

            # Dibujar el personaje
            image = pygame.image.load(join("assets","img", "character", "personaje_principal.png")).convert_alpha()
            image = pygame.transform.scale(image, (widthCuadrado, heightCuadrado))
            screen.blit(image, (x, y))

            pygame.display.update()

        pygame.quit()