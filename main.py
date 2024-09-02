import pygame
from menu.menu import Menu
from general.settings import *

def main(): # Declaramos funcion principal
    pygame.init() # Iniciamos el bucle
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Establecemos el tamaño de la pantalla
    pygame.display.set_caption(TITLE_GAME) # Establecemos el titulo del juego
    pygame.display.set_icon(pygame.image.load(ICON_GAME)) # Establecemos el icono del juego

    clock = pygame.time.Clock() # Creamos un reloj para controlar los FPS del juego

    while True:
        opcion_abrir_menu = Menu(screen).mostrarMenuInicial() # Mostramos el menu inicial y guardamos la opcion seleccionada<
        
        if opcion_abrir_menu == "quit" or opcion_abrir_menu == "salir": # Si la opcion es salir, salimos del bucle
            break


        clock.tick(FPS)  # Limitamos los FPS 

    pygame.quit() # Salimos del bucle

if __name__ == "__main__": # Si el nombre del modulo es igual a main, ejecutamos la funcion principal
    main()
