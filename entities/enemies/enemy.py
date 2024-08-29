import pygame

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 40, 40)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
