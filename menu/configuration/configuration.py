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

    def show_configuration(self, screen, font):
        # Crear superficies de configuración y de sobreposición
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparente para sombrear la pantalla principal

        config_surface = pygame.Surface((400, 300))
        config_surface.fill(BACKGROUND_COLOR)

        # Configurar opciones
        option_rects = []  
        languages = ["English", "Español"]
        for i, language in enumerate(languages):
            text = font.render(language, True, WHITE)
            rect = text.get_rect(center=(config_surface.get_width() // 2, 50 + i * 50))
            config_surface.blit(text, rect)
            option_rects.append((language.lower(), rect))

        exit_text = font.render("Salir", True, WHITE)
        exit_rect = exit_text.get_rect(center=(config_surface.get_width() // 2, 200))
        config_surface.blit(exit_text, exit_rect)
        option_rects.append(("exit", exit_rect))

        # Mostrar la pantalla de configuración sobre la principal
        screen.blit(overlay, (0, 0))
        screen.blit(config_surface, (screen.get_width() // 2 - config_surface.get_width() // 2, screen.get_height() // 2 - config_surface.get_height() // 2))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Verificar clic izquierdo
                    pos = pygame.mouse.get_pos()  # Obtener la posición del ratón
                    print(f'Posición del ratón: {pos}')  # Imprimir posición para depuración
                    for option_text, rect in option_rects:
                        if rect.collidepoint(pos):
                            print(f'Click en: {option_text}')
                            if option_text == "exit":
                                print("Regresando al menú desde configuración.")
                                return "menu"
                            else:
                                print(f"Cambiando idioma a: {option_text}")
                                self.set_language(option_text)  # Guardar el idioma seleccionado
                                return "menu"
