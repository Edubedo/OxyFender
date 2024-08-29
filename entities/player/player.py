import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 128, 255))

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))