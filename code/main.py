import pygame
from menu.menu import Menu
from maps_levels.game import Game
from general.credits import show_credits

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
        elif action == "credits":
            show_credits(screen)
        elif action == "quit":
            break

        clock.tick(60)  # Limita el juego a 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
