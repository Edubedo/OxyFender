import pygame
import cv2
import sys
from utilerias.configuraciones import *
from os.path import join

class Creditos:
    def __init__(self, screen, configLanguage, datosLanguage):
        self.screen = screen
        self.configLanguage = configLanguage
        self.datosLanguage = datosLanguage
    def mostrarCreditos(self):
        pygame.time.wait(0)
        self.empezarVideoCreditos()

    def empezarVideoCreditos(self):
        self.configLanguage == "es" and pygame.display.set_caption("Credits - OxyFender") or pygame.display.set_caption("Créditos - OxyFender")
        rutaVideo = self.configLanguage == "es" and join("assets", "videos","creditos", "creditsSpanish.mp4") or join("assets", "videos","creditos", "creditsEnglish.mp4")
        cap = cv2.VideoCapture(rutaVideo)

        if not cap.isOpened():
            return

        # Detener la música de fondo
        pygame.mixer.music.stop()

        # Inicializar el módulo de sonido de Pygame
        pygame.mixer.init()

        # Reproducir el audio del video
        rutaAudio = join("assets", "audio", "music", "Creditos.mpeg")
        pygame.mixer.music.load(rutaAudio)
        #volumen
        pygame.mixer.music.play()

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
                    if event.key == pygame.K_ESCAPE:
                        activo = False

            self.screen.blit(frame, (0, 0))
            pygame.display.update()
            clock.tick(30)

        cap.release()
        pygame.mixer.music.stop()

    def run(self):
        pygame.init()
        self.mostrarCreditos()