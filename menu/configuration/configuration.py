# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
# Este software no puede ser copiado o redistribuido sin permiso del autor.
import json
import pygame
from utils.settings import *
import sys
class Configuration:
    def __init__(self, config_file="language.json"):
        self.config_file = config_file
        self.settings = self.load_settings()

    def load_settings(self):
        try:
            with open(self.config_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"language": "english"}

    def save_settings(self):
        with open(self.config_file, "w", encoding="utf-8") as file:
            json.dump(self.settings, file, indent=4, ensure_ascii=False)

    def obtenerLenguajeActual(self):
        return self.settings.get("language", "english")

    def set_language(self, language):
        self.settings["language"] = language.lower()
        self.save_settings()
        
    def diseño_opciones(self, screen): 
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        color = (255,255,255)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running == False
            pygame.draw.rect(screen, color, pygame.Rect(200, 500, 200, 200)) 
            pygame.display.flip()

    def show_configuration(self, screen, font):
        screen.fill(BACKGROUND_COLOR)
        option_rects = []  
        languages = ["English", "Español"]
        for i, language in enumerate(languages):
            text = font.render(language, True, WHITE)
            rect = text.get_rect(center=(screen.get_width() // 12, 200 + i * 50))
            screen.blit(text, rect)
            option_rects.append((language.lower(), rect))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for language, rect in option_rects:
                        if rect.collidepoint(event.pos):
                            self.set_language(language)
                            return