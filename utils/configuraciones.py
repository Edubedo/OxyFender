# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
#ste software no puede ser copiado o redistribuido sin permiso del autor.
import pygame
from os.path import join
from pygame.math import Vector2 as vector

TITLE_GAME = 'OxyFender'
NAME_ENTERPRISE = 'Zip Studio'
ICON_GAME = join("assets", "img", "icon", "icon_oxygen.png")

WIDTH = 1040
HEIGHT = 600
TILE_SIZE = 32 # 32x32

FPS = 60 

BACKGROUND_COLOR = (0, 0, 0)  
PLAYER_VEL = 3.5
PLAYER_GRAVEDAD = 0.32
PLAYER_FUERZA_SALTO = -4
PLAYER_VELOCIDAD_MAXIMA_CAIDA = 2.5
PLAYER_VELOCIDAD_Y = 0

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
GRAY = (128, 128, 128)
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
AZUL_TITULO = (34,31, 74)


CON_OXIGENO = ()

FONDO_CAFE = (76,72, 78)

# Botones
BUTTON_MENU_WIDTH = 400
BUTTON_MENU_HEIGHT = 60
