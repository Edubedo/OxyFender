import pygame
from utils.settings import *
from os.path import join
from pytmx.util_pygame import load_pygame
import sys
from utils.sprites import Sprite
from utils.player import Player

class Level1Beginner:  # Creamos el nivel 1
    def __init__(self, name, dificultadNivel, id):
        self.name = name
        self.dificultadNivel = dificultadNivel
        self.id = id

        pygame.display.set_caption(f"{TITLE_GAME} - {name}")  # Set the game title

        self.mostrar_superficie = pygame.display.get_surface()

        self.todos_los_sprites = pygame.sprite.Group()  # Creamos un grupo de sprites para todos los sprites
        self.colisiones_sprites = pygame.sprite.Group()  # Creamos un grupo de sprites para las colisiones
        self.elevador_sprites = pygame.sprite.Group()  # Creamos un grupo de sprites para los elevadores

        self.tmx_mapa_1 = load_pygame(join("assets", "maps", "beginner", "level1", "SCIENCE.tmx"))  # Cargamos el mapa del nivel 1

        self.camera_offset = pygame.Vector2(0, 0)  # Agregamos esta variable para que la camara siga al jugador

        self.player = None  # Agregamos esta variable para asignar el jugador jugador

        self.last_elevator = None  # Último elevador al que fue teletransportado
        self.teleport_cooldown = 1000  # Tiempo de espera en milisegundos
        self.last_teleport_time = 0  # Última vez que se teletransportó

        self.font = pygame.font.Font(None, 36)  # Initialize font

        self.juegoPausado = False  # Flag to track if the game is juegoPausado
        self.screen_capture = None  # Variable to store screen capture

        self.setup(self.tmx_mapa_1)

    def setup(self, tmx_mapa_1):
        self.tmx_tileset = pygame.image.load(join("assets", "maps", "beginner", "level1", "lab_tileset_LITE.png")).convert_alpha()  # Texturas del piso y techo

        self.posicion_x_personaje = 0  # Agregamos esta variable para la posicion del personaje

        # Agregamos las colisiones de las capas del mapa
        for layer_name in ['prtatras', 'Suelo', 'Paredes', 'Techo', 'FondoPiso1', 'FondoPiso2', 'Ascensor']:
            for x, y, surf in tmx_mapa_1.get_layer_by_name(layer_name).tiles():

                # Estructuras
                sprite = Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), surf, self.todos_los_sprites)

                # Colisiones
                if layer_name in ['Paredes', 'Suelo', 'Techo']:
                    self.colisiones_sprites.add(sprite)
                # Elevadores
                if layer_name == 'Ascensor':
                    self.elevador_sprites.add(sprite)

        # Cargar objetos de la capa 'filtooo'
        filtooo_layer = tmx_mapa_1.get_layer_by_name('filtooo')
        print("filtooo_layer", filtooo_layer)
        for obj in filtooo_layer:
            print(f"Object: {obj.name}, x: {obj.x}, y: {obj.y}, width: {obj.width}, height: {obj.height}")
            for key, value in obj.properties.items():
                print(f"  Property: {key} = {value}")
            if isinstance(obj.image, pygame.Surface):
                image = obj.image
            else:
                image = pygame.image.load(join("assets", "sprites", obj.image)).convert_alpha()
            sprite = Sprite((obj.x, obj.y), image, self.todos_los_sprites)

        # Personaje
        self.player = Player((100, 420), self.todos_los_sprites)  # ! Establecer posicion del jugador de tiled

        self.run()

    def run(self):
        clock = pygame.time.Clock()
        gravedad = PLAYER_GRAVEDAD  # Ajustar la gravedad
        maxima_velocidad_caida = 4
        jugador_velocidad_y = 0
        esta_sobre_el_piso = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.juegoPausado:
                        pygame.quit()
                        sys.exit()
                    else:
                        self.juegoPausado = not self.juegoPausado
                        if self.juegoPausado:
                            self.screen_capture = self.mostrar_superficie.copy()  # Capture the current screen

            if self.juegoPausado:
                self.pantallaConfiguracion()
                continue

            keys = pygame.key.get_pressed()  # Tenemos que agregar esta funciona para hacer que el jugador se mueva
            movimientoJugador = pygame.Vector2(0, 0)
            estaMoviendose = False
            direccionPersonaje = "right"  

            if keys[pygame.K_LEFT]:
                movimientoJugador.x -= PLAYER_VEL
                estaMoviendose = True
                direccionPersonaje = "left"
            if keys[pygame.K_RIGHT]:
                movimientoJugador.x += PLAYER_VEL
                estaMoviendose = True
                direccionPersonaje = "right"
            if keys[pygame.K_SPACE] and esta_sobre_el_piso:
                jugador_velocidad_y = PLAYER_FUERZA_SALTO
                esta_sobre_el_piso = False  # El jugador ya no está en el suelo después de saltar

            # Aplicar gravedad solo si no está en el suelo
            if not esta_sobre_el_piso:
                jugador_velocidad_y += gravedad
                if jugador_velocidad_y > maxima_velocidad_caida:
                    jugador_velocidad_y = maxima_velocidad_caida
            movimientoJugador.y += jugador_velocidad_y

            # Mover al jugador y verificar colisiones verticales
            self.player.rect.y += movimientoJugador.y
            colisionesSprite = pygame.sprite.spritecollide(self.player, self.colisiones_sprites, False)
            for sprite in colisionesSprite:
                if movimientoJugador.y > 0:  # Bajando
                    self.player.rect.bottom = sprite.rect.top
                    esta_sobre_el_piso = True
                    jugador_velocidad_y = 0
                elif movimientoJugador.y < 0:  # Subiendo
                    self.player.rect.top = sprite.rect.bottom
                    jugador_velocidad_y = 0

            # Mover al jugador y verificar colisiones horizontales
            self.player.rect.x += movimientoJugador.x
            colisionesSprite = pygame.sprite.spritecollide(self.player, self.colisiones_sprites, False)
            for sprite in colisionesSprite:
                if movimientoJugador.x > 0:  # Moviéndose a la derecha
                    self.player.rect.right = sprite.rect.left
                elif movimientoJugador.x < 0:  # Moviéndose a la izquierda
                    self.player.rect.left = sprite.rect.right

            # Verificar colisiones con elevadores
            tiempo_actual = pygame.time.get_ticks()
            colisiones_elevadores = pygame.sprite.spritecollide(self.player, self.elevador_sprites, False)
            if colisiones_elevadores and tiempo_actual - self.last_teleport_time > self.teleport_cooldown:
                # Mostrar mensaje en pantalla
                font = pygame.font.Font(None, 36)
                text = font.render("Click X para viajar en el elevador", True, (255, 255, 255))
                text_rect = text.get_rect(center=(self.mostrar_superficie.get_width() // 2, self.mostrar_superficie.get_height() // 2))

                # Verificar si se presiona la tecla 'X'
                if keys[pygame.K_x]:
                    # Teletransportar al jugador al otro elevador
                    for elevator in self.elevador_sprites:
                        if elevator not in colisiones_elevadores and elevator != self.last_elevator:
                            self.player.rect.topleft = elevator.rect.topleft
                            self.last_elevator = elevator
                            self.last_teleport_time = tiempo_actual
                            break

            self.camera_offset.x = self.player.rect.centerx - self.mostrar_superficie.get_width() // 2
            self.camera_offset.y = self.player.rect.centery - self.mostrar_superficie.get_height() // 2

            self.todos_los_sprites.update(estaMoviendose, direccionPersonaje)

            self.mostrar_superficie.fill(BACKGROUND_COLOR)

            # Dibujar el mapa de Tiled
            for layer in self.tmx_mapa_1.visible_layers:
                if hasattr(layer, 'tiles'):
                    for x, y, image in layer.tiles():
                        self.mostrar_superficie.blit(image, (x * TILE_SIZE - self.camera_offset.x, y * TILE_SIZE - self.camera_offset.y))

            for sprite in self.todos_los_sprites:
                self.mostrar_superficie.blit(sprite.image, sprite.rect.topleft - self.camera_offset)

            # Mostrar mensaje en pantalla si está cerca del elevador
            if colisiones_elevadores and tiempo_actual - self.last_teleport_time > self.teleport_cooldown:
                self.mostrar_superficie.blit(text, text_rect)

            pygame.display.flip()

            clock.tick(FPS)

    def pantallaConfiguracion(self):
        configuracionWidthPantalla = self.mostrar_superficie.get_width() - 200
        configuracionHeightPantalla = self.mostrar_superficie.get_height() - 200

        # Creamos una nueva superficie para la pantalla de configuración
        config_screen = pygame.Surface((configuracionWidthPantalla, configuracionHeightPantalla))
        config_screen.fill((50, 50, 50)) 

        # Agregar boton para reiniciar nivel
        botonReiniciarNivel = pygame.Rect(50, 50, 200, 50)
        pygame.draw.rect(config_screen, (255, 0, 0), botonReiniciarNivel)

        font = pygame.font.Font(None, 36)
        text = font.render("Reiniciar Nivel", True, (255, 255, 255))
        text_rect = text.get_rect(center=botonReiniciarNivel.center)
        config_screen.blit(text, text_rect)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.juegoPausado = False
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    # Revisamos sí el mouse está encima del botón
                    relative_mouse_pos = (mouse_pos[0] - 150, mouse_pos[1] - 150)
                    if botonReiniciarNivel.collidepoint(relative_mouse_pos):
                        print("Reiniciar Nivel")
                        self.setup(self.tmx_mapa_1)
                        running = False
                        self.juegoPausado = False

            if self.screen_capture:
                self.mostrar_superficie.blit(self.screen_capture, (0, 0))

            # Oscurecemos la pantalla cuando le damos a pausa
            dark_overlay = pygame.Surface(self.mostrar_superficie.get_size(), pygame.SRCALPHA) # Superficie transparente
            dark_overlay.fill((0, 0, 0, 150))  # Semi-transparent black
            self.mostrar_superficie.blit(dark_overlay, (0, 0))

            self.mostrar_superficie.blit(config_screen, (150, 150))

            pygame.display.flip() # Actualizamos la pantalla