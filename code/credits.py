import pygame

def show_credits(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render("Credits", True, (255, 255, 255))
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
