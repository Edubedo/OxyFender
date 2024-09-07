# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
# Este software no puede ser copiado o redistribuido sin permiso del autor.
import pygame
from os.path import join

TITLE_GAME = 'OxyFender'
NAME_ENTERPRISE = 'Zip Studio'
ICON_GAME = join("assets", "img", "icon", "icon_oxygen.png")

WIDTH = 1080
HEIGHT = 600

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
DARK_BLUE = (6, 11, 28)
LIGHTBLUE = (12, 28, 82)
YELLOW = (255, 255, 0)
LIGHTGREEN = (0, 255, 0)
LIGHTYELLOW = (255, 255, 0)
LIGHTRED = (255, 0, 0)
LIGHTORANGE = (255, 165, 0)
LIGHTPURPLE = (255, 0, 255)


# Botones
BUTTON_MENU_WIDTH = 400
BUTTON_MENU_HEIGHT = 60