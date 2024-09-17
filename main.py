# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
# Este software no puede ser copiado o redistribuido sin permiso del autor.
import pygame
from menu.menu import Menu
from utils.settings import *

def main():
    pygame.init()  # Initialize all Pygame modules
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set the screen size
    pygame.display.set_caption(TITLE_GAME)  # Set the game title
    pygame.display.set_icon(pygame.image.load(ICON_GAME))  # Set the game icon

    menu = Menu(screen)
    menu.mostrarMenuInicial()  # Mostrar el menú del juego.

if __name__ == "__main__":
    main()
