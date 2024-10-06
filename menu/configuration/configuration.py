# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
# Este software no puede ser copiado o redistribuido sin permiso del autor.
import json
import pygame
from utilerias.configuraciones import *
import sys

class Configuration:
    def __init__(self, config_file="language.json"):
        self.config_file = config_file
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.sonidoDeClick = pygame.mixer.Sound(join("assets", "audio", "utilerias", "click_madera.mp3"))

    def setup(self):
        pygame.display.set_caption(f"Configuration - {TITLE_GAME}")  # Establecer titulo del nivel

        self.fondoMenuDificultad = pygame.image.load(join("assets", "img", "FONDOS", "secciones_nivel_fondo.png")).convert_alpha()  # Fondo para menu de selección de dificultad
        self.fondoMenuDificultad = pygame.transform.scale(self.fondoMenuDificultad, (WIDTH, HEIGHT))
        
        self.screen.blit(self.fondoMenuDificultad, [0, 0])

        # Agregar el título de mostrar dificultad
        fontTitulo = pygame.font.Font(join("assets", "fonts", "Transformers Movie.ttf"), 100)
        titulo = fontTitulo.render("Configuration", True, AZUL_TITULO)
        titulo_rect = titulo.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(titulo, titulo_rect)
        
        # Mostrar mensaje de "Under construction"
        fontMensaje = pygame.font.Font(join("assets", "fonts", "Transformers Movie.ttf"), 50)
        mensaje = fontMensaje.render("Under construction", True, AZUL_TITULO)
        mensaje_rect = mensaje.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(mensaje, mensaje_rect)
        
        # Crear botón de regreso
        back_button = pygame.image.load(join("assets","img","BOTONES","b_regreso2.png")).convert_alpha()
        back_button = pygame.transform.scale(back_button, (back_button.get_width() - 10, back_button.get_height() - 10))
        back_button_rect = back_button.get_rect(topleft=(40, HEIGHT - 100))
        self.screen.blit(back_button, back_button_rect)
        
        # Agregar nombre de la empresa
        fontTextoInferiorDerecha = pygame.font.Font(join("assets", "fonts", "Font_Name_Enterprise.ttf"), 24)  # Fuente
        textoInferiorDerecha = fontTextoInferiorDerecha.render(NAME_ENTERPRISE, True, WHITE)  # Texto
        texto_rect = textoInferiorDerecha.get_rect(bottomright=(self.screen.get_width() - 45, self.screen.get_height() - 45))  # Rectangulo para mostrar el texto en la pantalla
        self.screen.blit(textoInferiorDerecha, texto_rect)  # Mostrar texto en la pantalla

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Cuando hace hover con el mouse
                elif event.type == pygame.MOUSEMOTION:
                    # Verificamos si el mouse está encima del botón de regreso para ponerle el curso de mano o de flecha
                    if back_button_rect.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                # Cuando hace click con el mouse                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.sonidoDeClick.play() # Cuando hace un click dentro de las opciones del menú

                    # Si se hace clic en el botón de regreso
                    if back_button_rect.collidepoint(event.pos):
                        return

            # Pintar el fondo y el título en la pantalla
            self.screen.blit(self.fondoMenuDificultad, [0, 0])
            self.screen.blit(titulo, titulo_rect)
            self.screen.blit(mensaje, mensaje_rect)
            
            # Pintar el botón de regreso
            self.screen.blit(back_button, back_button_rect)
            # Pinta el texto de la empresa
            self.screen.blit(textoInferiorDerecha, texto_rect)

            pygame.display.flip()