import pygame
import time

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.start_time = pygame.time.get_ticks()  # Guardar el tiempo de inicio
        self.font = pygame.font.Font(None, 36)

    def draw_timer(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        time_text = f"Time: {elapsed_time}s"
        text_surface = self.font.render(time_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))

    def show_pause_menu(self):
        pause_font = pygame.font.Font(None, 74)
        pause_text = pause_font.render("Paused", True, (255, 0, 0))
        resume_text = self.font.render("Press 'P' to Resume", True, (255, 255, 255))
        quit_text = self.font.render("Press 'Q' to Quit", True, (255, 255, 255))

        self.screen.fill((0, 0, 0))
        self.screen.blit(pause_text, (self.screen.get_width() // 2 - pause_text.get_width() // 2, self.screen.get_height() // 2 - 50))
        self.screen.blit(resume_text, (self.screen.get_width() // 2 - resume_text.get_width() // 2, self.screen.get_height() // 2 + 10))
        self.screen.blit(quit_text, (self.screen.get_width() // 2 - quit_text.get_width() // 2, self.screen.get_height() // 2 + 50))
        pygame.display.flip()

        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Resume game
                        self.paused = False
                    elif event.key == pygame.K_q:  # Quit game
                        self.running = False
                        return

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Pausa
                        self.paused = True
                        self.show_pause_menu()
                    elif event.key == pygame.K_q:  # Salir del juego
                        self.running = False

            if not self.paused:
                self.screen.fill((0, 0, 0))  # Limpiar la pantalla
                # Aquí agregarías la lógica del juego
                self.draw_timer()  # Dibujar el temporizador
                pygame.display.flip()
            
            self.clock.tick(60)  # Limitar el juego a 60 FPS
