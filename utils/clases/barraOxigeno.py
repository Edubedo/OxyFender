from utils.configuraciones import *

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

        # Cargar imágenes de tanques de oxígeno
        self.imagenes_tanque = []
        for i in range(0, 101, 10):
            imagen = pygame.image.load(f"assets/img/BOTONES/OXIGENO/tanque_{i}%.png").convert_alpha()
            self.imagenes_tanque.append(imagen)

    def actualizar_tiempo(self, tiempo_actual):
        self.tiempo_restante = max(0, self.tiempo_total - (tiempo_actual // 1000))
        self.hp = (self.tiempo_restante / self.tiempo_total) * self.max_hp

    def obtener_imagen_tanque(self):
        # Asegurarse de que la imagen no cambie a 0% hasta que el tiempo restante sea 0
        if self.tiempo_restante == 0:
            indice = 0
        else:
            indice = max(1, int((self.hp / self.max_hp) * 10))
        return self.imagenes_tanque[indice]

    def draw(self, surface):
        imagen_tanque = self.obtener_imagen_tanque()
        surface.blit(imagen_tanque, (self.x, self.y))