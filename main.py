import pygame

pygame.init()
screen = pygame.display.set_mode((800, 400)) # Create a window

#Set the title in pygame
pygame.display.set_caption('Runner')

# Set an icon in pygame
pygame.display.set_icon(pygame.image.load('messi.png')) 

clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

score_surf = test_font.render('Game',False, 'Black' )
score_rect = score_surf.get_rect(center=(400, 50))

snail_x_pos = 600
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(600,300))

player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80,300))


# If we want that the code works we need to add a loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos): print("Collision")
    
    screen.blit(sky_surface, (0, 0)) # Block Image Transfer(Put one surfer in another surfer)
    screen.blit(ground_surface, (0, 300))

    pygame.draw.rect(screen, 'Pink', score_rect, 6) # Add background

    pygame.draw.line(screen, 'firebrick', (0, 0), pygame.mouse.get_pos(), 10) # Draw a line

    screen.blit(score_surf, score_rect)
    
    snail_rect.x -= 4
    if snail_rect.x <= 0: snail_rect.x = 800

    screen.blit(player_surf, player_rect)
    screen.blit(snail_surface, snail_rect)

    # if player_rect.colliderect(snail_rect):
    #     print("Collision")

    # mouse_pos = pygame.mouse.get_pos()

    pygame.display.update() 
    clock.tick(60)
