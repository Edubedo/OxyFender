# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
# Este software no puede ser copiado o redistribuido sin permiso del autor.
import pygame
from menu.menu import Menu
from utils.settings import *
class Starter: # Creamos la clase Starter
    def __init__(self): # Creamos el constructor
        pygame.init()  # Initialize all Pygame modules
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Establecemos el tamaño de la pantalla
        pygame.display.set_caption(TITLE_GAME) # Establecemos el titulo del juego
        pygame.display.set_icon(pygame.image.load(ICON_GAME)) # Establecemos el icono del juego

    def run(self): # Creamos el metodo run
        clock = pygame.time.Clock() # Creamos un reloj para controlar los FPS del juego
        Menu(self.screen).mostrarMenuInicial() # Mostramos el menu inicial y guardamos la opcion seleccionada<

        while True: # Bucle principal
            clock.tick(FPS) # Limitamos los FPS

            for event in pygame.event.get(): # Recorremos todos los eventos
                if event.type == pygame.QUIT: # Si el evento es cerrar la ventana, salimos del bucle
                    return

            pygame.display.flip() # Actualizamos la pantalla

if __name__ == "__main__": # Si el nombre del modulo es igual a main, ejecutamos la funcion principal
    start_game = Starter() # Creamos una instancia de la clase Starter
    start_game.run() # Ejecutamos el metodo run