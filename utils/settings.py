# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
# Este software no puede ser copiado o redistribuido sin permiso del autor.
import pygame
from os.path import join

TITLE_GAME = 'OxyFender'
ICON_GAME = join("assets", "img", "icon", "icon_oxygen.png")

WIDTH = 1280
HEIGHT = 720

FPS = 60 

BACKGROUND_COLOR = (0, 0, 0)  
PLAYER_VEL = 2

ENEMY_SPEED = 3

FONT_NAME = 'Arial'  

DEFAULT_FONT_SIZE = 30
DEFAULT_LANGUAGE = "english"


MUSIC='on'

window = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
TEXT_COLOR_OPTION_MENU = (128, 128, 128)  
BLACK = (0, 0, 0)  
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
LIGHTGREEN = (0, 255, 0)
LIGHTYELLOW = (255, 255, 0)
LIGHTRED = (255, 0, 0)
LIGHTORANGE = (255, 165, 0)
LIGHTPURPLE = (255, 0, 255)


# Botones
BUTTON_MENU_WIDTH = 200
BUTTON_MENU_HEIGHT = 50