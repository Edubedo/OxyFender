from utilerias.configuraciones import *
import pygame

class BarraOxigenoAdvanced():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = 0
        self.max_hp = max_hp
        self.tiempo_total = 60  # minuto en segundos
        self.tiempo_restante = self.tiempo_total
        self.tiempo_pausa = 0  # Nuevo: Variable para manejar el tiempo de pausa
        self.tiempo_ultimo = pygame.time.get_ticks()  # Tiempo cuando el juego empieza o se reanuda
        self.ultimo_cambio_imagen = self.tiempo_ultimo  # Nuevo: Tiempo del último cambio de imagen
        self.indice = 10  # Inicialmente en 100%

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

            print("tiempo_actual", tiempo_actual)
            print("self.ultimo_cambio_imagen", self.ultimo_cambio_imagen)
            # Verificar si han pasado 12,000 segundos desde el último cambio de imagen
            if (tiempo_actual - self.ultimo_cambio_imagen) >= 12000:
                self.ultimo_cambio_imagen = tiempo_actual
                # Actualizar el índice de la imagen
                self.indice = max(0, self.indice - 1)
        else:
            # Actualiza el último tiempo cuando el juego se pausa
            self.tiempo_ultimo = tiempo_actual

        if tiempo_actual >= 119000:
            self.hp = 0
            self.tiempo_restante = 0
            self.indice = 0

    def obtener_imagen_tanque(self):
        # Asegurarse de que la imagen no cambie a 0% hasta que el tiempo restante sea 0
        if self.tiempo_restante == 0:
            indice = 0
        else:
            indice = max(1, int((self.hp / self.max_hp) * 10))
        print("indice", indice)
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
        self.ultimo_cambio_imagen = 0  # Reiniciar el tiempo del último cambio de imagen
        self.indice = 10  # Reiniciar el índice de la imagen a 100%