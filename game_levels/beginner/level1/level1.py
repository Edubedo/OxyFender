import pygame
from general.settings import *

class Level1Beginner:
    def __init__(self, name, difficulty, id):
        self.name = name
        self.difficulty = difficulty
        self.id = id
        self.clock = pygame.time.Clock() # Reloj para controlar los FPS

    
    
    def run(self):
        # Inicializar Pygame y crear una ventana
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(f"{self.name} - {self.difficulty}")

        white = (255, 255, 255)
        black = (0, 0, 0)

        x, y = 50, 50
        width, height = 40, 60

        run = True
        while run:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

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

            # Dibujar en la pantalla
            screen.fill(white)
            pygame.draw.rect(screen, black, (x, y, width, height))
            pygame.display.update()

        pygame.quit()
        quit()