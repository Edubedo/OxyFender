import pygame
from menu.menu import Menu
from game_levels.game import Game
from menu.credits.credits import show_credits

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("OxyFender")


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

        clock.tick(60)  

    pygame.quit()

if __name__ == "__main__":
    main()
