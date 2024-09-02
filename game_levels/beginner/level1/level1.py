import pygame
from general.settings import *

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

        white = (255, 255, 255)
        black = (0, 0, 0)
        gravedad = 1
        x, y = 50, 50
        widthCuadrado, heightCuadrado = 40, 60

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            # Obtener teclas presionadas
            keys = pygame.key.get_pressed()

            # Actualizar posición del objeto por medio de teclas
            if keys[pygame.K_LEFT]:
                if x < 0:
                    x += PLAYER_VEL
                else:
                    x -= PLAYER_VEL

            if keys[pygame.K_RIGHT]:
                if x < (WIDTH - widthCuadrado):
                    x += PLAYER_VEL
                else:
                    x-= PLAYER_VEL

            if keys[pygame.K_DOWN]:
                if y > (HEIGHT - heightCuadrado):
                    y -= PLAYER_VEL
                else:
                    y += PLAYER_VEL
            if keys[pygame.K_SPACE]:
                y -= PLAYER_VEL
                # Evitar doble salto
            screen.fill(white)
            rectCuadrado = pygame.draw.rect(screen, black, (x, y, widthCuadrado, heightCuadrado))
            # Cargar imagen
            image = pygame.image.load("assets/img/character/personaje_principal.png").convert_alpha()

            # Restablecer el tamaño de la imagen
            image = pygame.transform.scale(image, (widthCuadrado, heightCuadrado))

            # Blit the image onto the screen
            screen.blit(image, (x, y))

            # Manejar Gravedad
            vel_grav = y + gravedad
            y = vel_grav

            if y > (HEIGHT - heightCuadrado):
                    y = (HEIGHT - heightCuadrado)
            # Detectar colisión entre el mouse y el cuadrado
            punteroMouse = pygame.mouse.get_pos()
            collide = rectCuadrado.collidepoint(punteroMouse)

            pygame.display.update()

        pygame.quit()
        quit()


   