import pygame
from menu.menu import Menu
from game_levels.game import Game
from menu.credits.credits import show_credits
from general.settings import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE_GAME)
    pygame.display.set_icon(pygame.image.load("assets/icon/icon_oxygen.png"))

    clock = pygame.time.Clock()
    menu = Menu(screen) 

    while True:
        action = menu.show()
        if action == "play":
            game = Game(screen)
            game.run()
        elif action == "credits" or action == "créditos":
            show_credits(screen)
        elif action == "quit" or action == "salir":
            break


        clock.tick(FPS)  

    pygame.quit()

if __name__ == "__main__":
    main()
