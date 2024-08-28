import pygame

def draw_text(screen, text, pos, font_size=36, color=(255, 255, 255)):
    font = pygame.font.Font(None, font_size)
    render = font.render(text, True, color)
    screen.blit(render, pos)
