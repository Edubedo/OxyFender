import pygame
from general.settings import *

class MenuGame:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.font = pygame.font.Font(None, 36)

    def show_difficulty_menu(self):
        self.screen.fill(BACKGROUND_COLOR)
        difficulty_options = ["Beginner", "Advanced"] if self.config.get_language() == "english" else ["Principiante", "Avanzado"]
        self.option_rects = []  
        for i, option in enumerate(difficulty_options):
            text = self.font.render(option, True, TEXT_COLOR)
            rect = text.get_rect(center=(self.screen.get_width() // 2, 150 + i * 50))
            self.screen.blit(text, rect)
            self.option_rects.append((option.lower(), rect))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for option, rect in self.option_rects:
                        if rect.collidepoint(event.pos):
                            return self.show_level_menu(option)

    def show_level_menu(self, difficulty):
        self.screen.fill(BACKGROUND_COLOR)
        level_options = [f"Level {i+1} - {difficulty}" for i in range(3)]
        self.option_rects = []  
        for i, level in enumerate(level_options):
            text = self.font.render(level, True, TEXT_COLOR)
            rect = text.get_rect(center=(self.screen.get_width() // 2, 150 + i * 50))
            self.screen.blit(text, rect)
            self.option_rects.append((level.lower(), rect))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for level, rect in self.option_rects:
                        if rect.collidepoint(event.pos):
                           #  return difficulty, level
                           print("event", event)
                           print("level", level)