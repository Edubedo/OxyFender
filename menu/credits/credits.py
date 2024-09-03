import pygame
from utils.settings import *

def show_credits(screen):
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(None, 36)
    text = font.render("Credits to the team", True, WHITE)
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2))
    pygame.display.flip()
