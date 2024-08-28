import pygame

def show_credits(screen):
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 36)
    text = font.render("Credits", True, (0, 0, 0))
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(1000)
