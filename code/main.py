import pygame
from menu import Menu
from game import Game
from settings import Settings
from credits import Credits

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Pygame Game")

MENU = 'menu'
GAME = 'game'
SETTINGS = 'settings'
CREDITS = 'credits'
QUIT = 'quit'

def main():
    clock = pygame.time.Clock()
    running = True
    state = MENU
    
    menu = Menu(screen)
    game = Game(screen)
    settings = Settings(screen)
    credits = Credits(screen)

    while running:
        if state == MENU:
            state = menu.run()
        elif state == GAME:
            state = game.run()
        elif state == SETTINGS:
            state = settings.run()
        elif state == CREDITS:
            state = credits.run()
        elif state == QUIT:
            running = False
        
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
