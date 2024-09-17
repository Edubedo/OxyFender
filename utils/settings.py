# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
#ste software no puede ser copiado o redistribuido sin permiso del autor.
import pygame
from os.path import join
from os import walk
from pygame.math import Vector2 as vector

TITLE_GAME = 'OxyFender'
NAME_ENTERPRISE = 'Zip Studio'
ICON_GAME = join("assets", "img", "icon", "icon_oxygen.png")

WIDTH = 1040
HEIGHT = 600
TILE_SIZE = 32 # 32x32

FPS = 60 

BACKGROUND_COLOR = (0, 0, 0)  
PLAYER_VEL = 3.6
PLAYER_GRAVEDAD = 0.32
PLAYER_FUERZA_SALTO = -6
PLAYER_VELOCIDAD_MAXIMA_CAIDA = 3
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

Z_LAYERS = {
	'bg': 0,
	'clouds': 1,
	'bg tiles': 2,
	'path': 3,
	'bg details': 4,
	'main': 5,
	'water': 6,
	'fg': 7
}


def import_folder(*path):
	frames = []
	for folder_path, subfolders, image_names in walk(join(*path)):
		for image_name in sorted(image_names, key = lambda name: int(name.split('.')[0])):
			full_path = join(folder_path, image_name)
			frames.append(pygame.image.load(full_path).convert_alpha())
	return frames 


def import_sub_folders(*path):
	frame_dict = {}
	for _, sub_folders, __ in walk(join(*path)): 
		if sub_folders:
			for sub_folder in sub_folders:
				frame_dict[sub_folder] = import_folder(*path, sub_folder)
	return frame_dict


def import_image(*path, alpha = True, format = 'png'):
	full_path = join(*path) + f'.{format}'
	return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()

def import_folder(*path):
	frames = []
	for folder_path, subfolders, image_names in walk(join(*path)):
		for image_name in sorted(image_names, key = lambda name: int(name.split('.')[0])):
			full_path = join(folder_path, image_name)
			frames.append(pygame.image.load(full_path).convert_alpha())
	return frames

def import_folder_dict(*path):
	frame_dict = {}
	for folder_path, _, image_names in walk(join(*path)):
		for image_name in image_names:
			full_path = join(folder_path, image_name)
			surface = pygame.image.load(full_path).convert_alpha()
			frame_dict[image_name.split('.')[0]] = surface
	return frame_dict
