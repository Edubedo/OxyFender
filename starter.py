# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
# Este software no puede ser copiado o redistribuido sin permiso del autor.
import pygame
from menu.menu import Menu
from utils.settings import *
import sys

def main():
    pygame.init()  # Initialize all Pygame modules
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set the screen size
    pygame.display.set_caption(TITLE_GAME)  # Set the game title
    pygame.display.set_icon(pygame.image.load(ICON_GAME))  # Set the game icon

    clock = pygame.time.Clock()  # Create a clock to control FPS

    menu = Menu(screen)
    menu.mostrarMenuInicial()  # Show the initial menu

    while True:  # Main loop
        clock.tick(FPS)  # Limit FPS

        for event in pygame.event.get():  # Handle events
            if event.type == pygame.QUIT:  # Exit the game
                pygame.quit()
                sys.exit()

        pygame.display.flip()  # Update the screen

if __name__ == "__main__":
    main()
