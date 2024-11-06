# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
# Este software no puede ser copiado o redistribuido sin permiso del autor.
import pygame
import cv2
from menu.menu import Menu
from utilerias.configuraciones import *
from os.path import join

class VideoInicio:
    def __init__(self, screen):
        self.screen = screen

    def mostrarVideoInicio(self):
        pygame.time.wait(0)
        self.empezarVideoInicio()

    def empezarVideoInicio(self):
        pygame.display.set_caption("Inicio - OxyFender")
        rutaVideo = join("assets", "videos", "Inicio.mp4")
        cap = cv2.VideoCapture(rutaVideo)

        if not cap.isOpened():
            return

        clock = pygame.time.Clock()
        activo = True

        while activo:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.screen.get_width(), self.screen.get_height()))
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    activo = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    activo = False
                elif event.type == pygame.KEYDOWN:
                    activo = False

            self.screen.blit(frame, (0, 0))

            # Mostrar mensaje en la parte superior izquierda
            font = pygame.font.SysFont(None, 36)
            text = font.render("Presione cualquier tecla para continuar", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))

            pygame.display.update()
            clock.tick(30)

        cap.release()

def main():
    pygame.init()  # Inicializar pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Establecer tamaño de pantalla
    pygame.display.set_caption(TITLE_GAME) # Establecer el titulo del juego
    pygame.display.set_icon(pygame.image.load(ICON_GAME))  # Establecer el icono del juego

    videoInicio = VideoInicio(screen)
    videoInicio.mostrarVideoInicio()  # Mostrar el video de inicio.

    menuInicial = Menu(screen)
    menuInicial.mostrarMenuInicial()  # Mostrar el menú del juego.

if __name__ == "__main__": # Iniciar el juego si el nombre del archivo es main
    main()