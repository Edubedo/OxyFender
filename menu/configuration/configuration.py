import json
import pygame
from utils.settings import *

class Configuration:
    def __init__(self, config_file="language.json"):
        self.config_file = config_file
        self.settings = self.load_settings()

    def load_settings(self):
        try:
            with open(self.config_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"language": "english"}

    def save_settings(self):
        with open(self.config_file, "w") as file:
            json.dump(self.settings, file, indent=4)

    def obtenerLenguajeActual(self):
        return self.settings.get("language", "english")

    def set_language(self, language):
        self.settings["language"] = language
        self.save_settings()

    def show_configuration(self, screen, font):
        screen.fill(BACKGROUND_COLOR)
        option_rects = []  
        languages = ["English", "Español"]
        for i, language in enumerate(languages):
            text = font.render(language, True, WHITE)
            rect = text.get_rect(center=(screen.get_width() // 2, 150 + i * 50))
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
    
