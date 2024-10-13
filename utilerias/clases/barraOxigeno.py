from utilerias.configuraciones import *
import pygame

class BarraOxigeno():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = 0
        self.max_hp = max_hp
        self.tiempo_total = 120  # 2 minutos en segundos
        self.tiempo_restante = self.tiempo_total
        self.tiempo_pausa = 0  # Nuevo: Variable para manejar el tiempo de pausa
        self.tiempo_ultimo = pygame.time.get_ticks()  # Tiempo cuando el juego empieza o se reanuda
        self.indice = None

        # Cargar imágenes de tanques de oxígeno
        self.imagenes_tanque = []
        for i in range(0, 101, 10):
            imagen = pygame.image.load(f"assets/img/BOTONES/OXIGENO/tanque_{i}%.png").convert_alpha()
            self.imagenes_tanque.append(imagen)

        # Inicializar la fuente para el texto
        self.font = pygame.font.Font(None, 36)  # Puedes cambiar el tamaño de la fuente según sea necesario

    def actualizar_tiempo(self, tiempo_actual, juegoPausado):
        if not juegoPausado:
            # Calcular el tiempo transcurrido considerando las pausas
            tiempo_transcurrido = (tiempo_actual - self.tiempo_ultimo) // 1000
            self.tiempo_restante = max(0, self.tiempo_total - tiempo_transcurrido)
            self.hp = (self.tiempo_restante / self.tiempo_total) * self.max_hp
        else:
            # Actualiza el último tiempo cuando el juego se pausa
            self.tiempo_ultimo = tiempo_actual

    def obtener_imagen_tanque(self):
        # Asegurarse de que la imagen no cambie a 0% hasta que el tiempo restante sea 0
        if self.tiempo_restante == 0:
            indice = 0
        else:
            indice = max(1, int((self.hp / self.max_hp) * 10))
        # Ensure indice is within the valid range
        indice = min(indice, len(self.imagenes_tanque) - 1)
        return self.imagenes_tanque[indice], indice * 10

    def draw(self, surface):
        imagen_tanque, porcentaje = self.obtener_imagen_tanque()
        surface.blit(imagen_tanque, (self.x, self.y))

        # Renderizar el texto del porcentaje
        texto = self.font.render(f"{porcentaje}%", True, (255, 255, 255))  # Texto en blanco
        texto_rect = texto.get_rect(center=((self.x + self.w // 2) + 10, self.y + self.h + 50))  # Ajustar la posición del texto
        surface.blit(texto, texto_rect)

    def reiniciar(self):
        # Reinicia los valores del temporizador y el oxígeno
        self.tiempo_restante = self.tiempo_total
        self.hp = self.max_hp
        self.tiempo_ultimo = pygame.time.get_ticks()