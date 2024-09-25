from utils.configuraciones import *

class BarraOxigeno():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = 0
        self.max_hp = max_hp

    def draw(self, surface):
        # Calcular radio de la barra
        ratio = self.hp / self.max_hp
        current_height = self.h * ratio
        pygame.draw.rect(surface, RED, (self.x, self.y, self.w, self.h))  # Draw background
        pygame.draw.rect(surface, GREEN, (self.x, self.y + (self.h - current_height), self.w, current_height))  # Draw bar