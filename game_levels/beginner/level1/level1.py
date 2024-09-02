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

        x, y = 50, 50
        width, height = 40, 60

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # Obtener teclas presionadas
            keys = pygame.key.get_pressed()

            # Actualizar posición del objeto
            if keys[pygame.K_LEFT]:
                x -= PLAYER_VEL
            if keys[pygame.K_RIGHT]:
                x += PLAYER_VEL
            if keys[pygame.K_UP]:
                y -= PLAYER_VEL
            if keys[pygame.K_DOWN]:
                y += PLAYER_VEL

            screen.fill(white)
            rectCuadrado = pygame.draw.rect(screen, black, (x, y, width, height))
            
            print(x, y)
            print(screen)

            punteroMouse = pygame.mouse.get_pos()
            collide = rectCuadrado.collidepoint(punteroMouse)
            color = RED if collide else BLUE

            pygame.draw.rect(window, color, rectCuadrado)
            pygame.display.update()

        pygame.quit()
        quit()


   