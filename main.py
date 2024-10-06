# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
# Este software no puede ser copiado o redistribuido sin permiso del autor.
import pygame
from menu.menu import Menu
from utilerias.configuraciones import *

def main():
    pygame.init()  
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Establecer tamaño de pantalla
    pygame.display.set_caption(TITLE_GAME) # Establecer el titulo del juego
    pygame.display.set_icon(pygame.image.load(ICON_GAME))  # Establecer el icono del juego

    menuInicial = Menu(screen)
    menuInicial.mostrarMenuInicial()  # Mostrar el menú del juego.

if __name__ == "__main__":
    main()


