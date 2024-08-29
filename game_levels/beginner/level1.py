import pygame
from entities.player.player import Player
from general.settings import *

class Level1Beginner:
    def __init__(self, name, difficulty, id):
        self.name = name
        self.difficulty = difficulty
        self.id = id
        self.enemies = []
        print(self.name, self.difficulty, self.id)
        self.player = Player(375, 275)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Simple 2D Game')
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.start_time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 36)

    def draw_timer(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        time_text = f"Time: {elapsed_time}s"
        text_surface = self.font.render(time_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))

   
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Pause
                        self.paused = True
                        self.show_pause_menu()
                    elif event.key == pygame.K_q:  # Quit game
                        Menu(self.screen)

            if not self.paused:
                self.screen.fill((0, 0, 0))  # Clear the screen
                keys = pygame.key.get_pressed()
                dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
                dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

                self.player.move(dx, dy)
                self.render()
                self.player.draw(self.screen)
                self.draw_timer()  

                pygame.display.flip()
            
            self.clock.tick(FPS) 

    def render(self):
        self.screen.fill((0, 0, 0))  