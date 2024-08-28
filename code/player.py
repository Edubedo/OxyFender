import pygame
from settings import GRID_SIZE

class Player:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.rect = pygame.Rect(0, 0, grid_size, grid_size)

    def move(self, pos):
        self.rect.topleft = (pos[0] // self.grid_size * self.grid_size, pos[1] // self.grid_size * self.grid_size)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)
