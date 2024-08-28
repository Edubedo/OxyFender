import pygame

class Reactor:
    def __init__(self, position):
        self.position = position
        self.radius = 20

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.position, self.radius)

    def is_near(self, character_pos):
        return pygame.math.Vector2(self.position).distance_to(character_pos) < 50
