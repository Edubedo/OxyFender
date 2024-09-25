import pygame
from utils.configuraciones import *
from os.path import join
from pytmx.util_pygame import load_pygame
import sys
from utils.sprites import Sprite
from utils.jugador import Player
from utils.clases.barraOxigeno import BarraOxigeno

class Level1Beginner:  # Creamos el nivel 1
    def __init__(self, name, dificultadNivel, id):
        self.name = name # Establcer nombre del nivel 
        self.dificultadNivel = dificultadNivel # Establecer dificultad del nivel
        self.id = id # Establecer id del nivel
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Establecer tamaño de la pantala

        pygame.display.set_caption(f"{TITLE_GAME} - {name}")  # Establecer titulo del  juego

        self.mostrarSuperficieNivel = pygame.display.get_surface()

        # Cargamos los sprites
        self.todos_los_sprites = pygame.sprite.Group()  # Creamos un grupo de sprites para todos los sprites
        self.colisiones_sprites = pygame.sprite.Group()  # Creamos un grupo de sprites para las colisiones
        self.elevador_piso1_sprites = pygame.sprite.Group()  # Creamos un grupo de sprites para los elevadores del piso 1
        self.elevador_piso2_sprites = pygame.sprite.Group()  # Creamos un grupo de sprites para los elevadores del piso 2
        self.filtro_sprites = pygame.sprite.Group()  # Creamos un grupo de sprites para los elevadores
        self.capa_verificar_gano = pygame.sprite.Group()  # Creamos un grupo de sprites para verificar si el jugador ganó
        
        #  Cargamos el mapa del nivel 1
        self.tmx_mapa_1 = load_pygame(join("assets", "maps", "beginner", "level1", "SCIENCE.tmx"))  # Cargamos el mapa del nivel 1

        self.camera_offset = pygame.Vector2(0, 0)  # Agregamos esta variable para que la camara siga al jugador

        self.jugador = None  # Agregamos esta variable para asignar el jugador jugador

        self.ultimoElevador = None  # Último elevador al que fue teletransportado
        self.tiempoEsperadoElevador = 1000  # Tiempo de espera en milisegundos
        self.ultimaVezTeletransportado = 0  # Última vez que se teletransportó

        self.font = pygame.font.Font(None, 36)  # Initialize font

        self.juegoPausado = False  # Bandara para manejar sí le dio click al botón de pausa
        self.capturarPantalla = None  # Captura de pantalla
        self.volver_menu = False  # Bandera para manejar sí le dio click al botón de volver al menu

        self.ganoNivel = False  # Bandera para manejar sí el jugador ganó
        self.perdioJuego = False  # Bandera para manejar sí el jugador perdió

        # ------------------- AGREGAMOS LA BARRA DE OXIGENO ------------------- #
        self.rectBarraCombustible = BarraOxigeno(10, 100, 40, 300, 200)
        self.rectBarraCombustible.hp = 200

        #  ------------------- Agregamos el conteo de oxigenos reparados y el objetivo x/y ------------------- #
        self.contadorOxigenoReparado = 0
        self.metaOxigenoReparado = 2

        self.ultimoTiempoCombustible = pygame.time.get_ticks()  # Tiempo inicial para el combustible


        self.setup(self.tmx_mapa_1) # Inicializamos el nivel 1

    def setup(self, tmx_mapa_1):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Establecer cursor del mouse
        
        self.tmx_tileset = pygame.image.load(join("assets", "maps", "beginner", "level1", "lab_tileset_LITE.png")).convert_alpha()  # Texturas del piso y techo

        self.posicion_x_personaje = 0  # Agregamos esta variable para la posicion del personaje

        # ------------------- AGREGAMOS LAS CAPAS Y COLISIONES DEL MAPA ------------------- #
        for nombreCapa in ['Suelo', 'Paredes', 'Techo', 'FondoPiso1', 'FondoPiso2', 'AscensorPiso1', 'AscensorPiso2', 'CapaVerificarGano']:
            for x, y, superficie in tmx_mapa_1.get_layer_by_name(nombreCapa).tiles(): # Recorremos las capas del mapa de Tiled Y obtenemos las superficies

                # Estructuras
                sprite = Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), superficie, self.todos_los_sprites) # Creamos un sprite para las estructuras(capa)

                # Colisiones de las capas del mapa para cuando interactue con el jugador
                if nombreCapa in ['Paredes', 'Suelo', 'Techo']:
                    self.colisiones_sprites.add(sprite)

                # Elevadores de las capas del mapa para cuando interactue con el jugador
                if nombreCapa == 'AscensorPiso1':
                    self.elevador_piso1_sprites.add(sprite)
                elif nombreCapa == 'AscensorPiso2':
                    self.elevador_piso2_sprites.add(sprite)
                elif nombreCapa == 'CapaVerificarGano':
                    self.capa_verificar_gano.add(sprite)

        # ------------------- AGREGAMOS EL FILTRO ------------------- #
        filtooo_layer = tmx_mapa_1.get_layer_by_name('filtooo')
        for obj in filtooo_layer: # Recorremos los objetos de la capa 'filtooo'
            sprite = Sprite((obj.x, obj.y), obj.image, self.todos_los_sprites)
            self.filtro_sprites.add(sprite)

        # ------------------- AGREGAMOS MAS OBJETOS DE TIPO IMG ------------------- #
        for nombreObjeto in ['Objetos']:
            for obj in tmx_mapa_1.get_layer_by_name(nombreObjeto):
                sprite = Sprite((obj.x, obj.y), obj.image, self.todos_los_sprites)
                
        # Personaje
        self.jugador = Player((100, 420), self.todos_los_sprites)  # ! Establecer posicion del jugador de tiled

        self.run() # Una vez cargadas las texturas y colisiones generales inicializamos el juego    

    def run(self): 
        # Pausar la música
        pygame.mixer.music.pause()

        clock = pygame.time.Clock() # Inicializamos el reloj para controlar los FPS

        # ------------------- GRAVEDAD ------------------- #
        gravedad = PLAYER_GRAVEDAD  # Ajustar la gravedad
        maxima_velocidad_caida = 4 # Ajustar la velocidad de caida
        jugador_velocidad_y = 1 # Ajustar la velocidad del jugador en y
        esta_sobre_el_piso = False

        while True:
            if self.volver_menu:
                break

            tiempoActualCombustible = pygame.time.get_ticks() # Tiempo actual del combustible

            if not self.ganoNivel: # Sí no ha ganado el nivel
                if tiempoActualCombustible - self.ultimoTiempoCombustible >= 1000:  # Reducir el oxigeno con cada segundo cada pasa de 10 en 10
                    self.rectBarraCombustible.hp -= 1
                    self.ultimoTiempoCombustible = tiempoActualCombustible
                    if self.rectBarraCombustible.hp <= 0:
                        self.perdioJuego = True

            if self.perdioJuego:
                self.pantallaPausar()
                continue

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
                            self.capturarPantalla = self.mostrarSuperficieNivel.copy()  # Capture the current screen

            if self.juegoPausado:
                self.pantallaPausar()
                continue

            # ------------------- MOVIMIENTO DEL JUGADOR ------------------- #
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
            self.jugador.rect.y += movimientoJugador.y
            spriteColisionesCapas = pygame.sprite.spritecollide(self.jugador, self.colisiones_sprites, False) # Funcion para verificar colisiones con las capas del mapa y el jugador

            for sprite in spriteColisionesCapas:
                if movimientoJugador.y > 0:  # Bajando
                    self.jugador.rect.bottom = sprite.rect.top
                    esta_sobre_el_piso = True
                    jugador_velocidad_y = 0

                elif movimientoJugador.y < 0:  # Subiendo
                    self.jugador.rect.top = sprite.rect.bottom
                    jugador_velocidad_y = 0

            # Mover al jugador y verificar colisiones horizontales
            self.jugador.rect.x += movimientoJugador.x
            spriteColisionesCapas = pygame.sprite.spritecollide(self.jugador, self.colisiones_sprites, False)
            for sprite in spriteColisionesCapas:
                if movimientoJugador.x > 0:  # Moviéndose a la derecha
                    self.jugador.rect.right = sprite.rect.left
                elif movimientoJugador.x < 0:  # Moviéndose a la izquierda
                    self.jugador.rect.left = sprite.rect.right

            # Verificar colisiones con elevadores
            tiempoActualElevadores = pygame.time.get_ticks()
            colisionesElevadoresPiso1 = pygame.sprite.spritecollide(self.jugador, self.elevador_piso1_sprites, False)
            colisionesElevadoresPiso2 = pygame.sprite.spritecollide(self.jugador, self.elevador_piso2_sprites, False)
            capaVerificarGano = pygame.sprite.spritecollide(self.jugador, self.capa_verificar_gano, False)
                
            if (colisionesElevadoresPiso1 or colisionesElevadoresPiso2) and tiempoActualElevadores - self.ultimaVezTeletransportado > self.tiempoEsperadoElevador:
                # Mostrar mensaje en pantalla
                fuenteColisionElevador = pygame.font.Font(None, 36)
                textoColisionElevador = fuenteColisionElevador.render("Click X para viajar en el elevador", True, (255, 255, 255))
                rectTextoColisionElevador = textoColisionElevador.get_rect(center=(self.mostrarSuperficieNivel.get_width() // 2, self.mostrarSuperficieNivel.get_height() // 2))

                # Verificar si se presiona la tecla 'X'
                if keys[pygame.K_x]:
                    # Teletransportar al jugador al otro elevador
                    if colisionesElevadoresPiso1:
                        for elevator in self.elevador_piso2_sprites:
                            self.jugador.rect.topleft = elevator.rect.topleft
                            self.jugador.rect.y += (self.jugador.rect.height / 3)  # Ajustar la posición para que no quede flotando
                            self.ultimoElevador = elevator
                            self.ultimaVezTeletransportado = tiempoActualElevadores
                            break
                    elif colisionesElevadoresPiso2:
                        for elevator in self.elevador_piso1_sprites:
                            self.jugador.rect.topleft = elevator.rect.topleft
                            self.jugador.rect.y += (self.jugador.rect.height / 3)  # Ajustar la posición para que no quede flotando
                            self.ultimoElevador = elevator
                            self.ultimaVezTeletransportado = tiempoActualElevadores
                            break

            # ------------------- FILTRO ------------------- #
            colisionesFiltros = pygame.sprite.spritecollide(self.jugador, self.filtro_sprites, False)

            if colisionesFiltros:
                for filtro in colisionesFiltros:
                    fuenteArreglarFiltro = pygame.font.Font(None, 36)
                    textoArreglarFiltro = fuenteArreglarFiltro.render("Click A para arreglar filtro", True, (255, 255, 255))
                    rectTextoArreglarFiltro = textoArreglarFiltro.get_rect(center=(self.mostrarSuperficieNivel.get_width() // 2, self.mostrarSuperficieNivel.get_height() // 2))

                    if keys[pygame.K_a] and not self.juegoPausado:
                        self.juegoPausado = True
                        self.capturarPantalla = self.mostrarSuperficieNivel.copy()  # Capture the current screen
                        self.pantallaArreglarAire()
                        self.juegoPausado = False

            # ------------------- MANEJO DEL VECTOR DE CÁMARA ------------------- #
            self.camera_offset.x = self.jugador.rect.centerx - self.mostrarSuperficieNivel.get_width() // 2
            self.camera_offset.y = self.jugador.rect.centery - self.mostrarSuperficieNivel.get_height() // 2

            self.todos_los_sprites.update(estaMoviendose, direccionPersonaje)

            self.mostrarSuperficieNivel.fill(BACKGROUND_COLOR)

            # Dibujar el mapa de Tiled
            for capa in self.tmx_mapa_1.visible_layers: # Recorremos las capas visibles del mapa de Tiled
                if hasattr(capa, 'tiles'):
                    for x, y, image in capa.tiles():
                        self.mostrarSuperficieNivel.blit(image, (x * TILE_SIZE - self.camera_offset.x, y * TILE_SIZE - self.camera_offset.y))

            for sprite in self.todos_los_sprites:
                self.mostrarSuperficieNivel.blit(sprite.image, sprite.rect.topleft - self.camera_offset)

            # Mostrar mensaje en pantalla si está cerca del elevador
            if (colisionesElevadoresPiso1 or colisionesElevadoresPiso2) and tiempoActualElevadores - self.ultimaVezTeletransportado > self.tiempoEsperadoElevador:
                self.mostrarSuperficieNivel.blit(textoColisionElevador, rectTextoColisionElevador)

            # Mostrar mensaje en pantalla si está cerca del filtro
            if colisionesFiltros:
                self.mostrarSuperficieNivel.blit(textoArreglarFiltro, rectTextoArreglarFiltro)

            # Dibujar la barra de combustible en la pantalla principal del juego
            self.rectBarraCombustible.draw(self.screen)

            # Mostrar en pantalla el conteo de oxigenos reparados
            textoOxigenosReparados = self.font.render(f"Oxigenos reparados: {self.contadorOxigenoReparado}/{self.metaOxigenoReparado}", True, (255, 255, 255))
            self.mostrarSuperficieNivel.blit(textoOxigenosReparados, (10, 10))
            

            pygame.display.flip()

            clock.tick(FPS)
    
    def pantallaPausar(self):
        # Posición del menú de configuración dentro del juego
        configuracionWidthPantalla = self.mostrarSuperficieNivel.get_width() - 200
        configuracionHeightPantalla = self.mostrarSuperficieNivel.get_height() - 300

        # Creamos una nueva superficie para la pantalla de configuración
        config_screen = pygame.Surface((configuracionWidthPantalla, configuracionHeightPantalla))

        config_screen.fill(DARK_BLUE) 

        # Agregar boton para reiniciar nivel
        botonReiniciarNivel = pygame.Rect(50, 50, 200, 50) # Establecer tamaño del boton
        pygame.draw.rect(config_screen, LIGHTBLUE, botonReiniciarNivel) # dibujar el boton de color azul
        text = self.font.render("Reiniciar Nivel", True, (255, 255, 255)) # Agregar texto al boton
        text_rect = text.get_rect(center=botonReiniciarNivel.center) # Centrar el texto en el boton
        config_screen.blit(text, text_rect) # Mostrar el texto en el boton

        # Agregar boton para volver a seleccionar nivel
        botonSeleccionarNivel = pygame.Rect(50, 150, 200, 50) # Establecer tamaño del boton
        pygame.draw.rect(config_screen, LIGHTBLUE, botonSeleccionarNivel) # dibujar el boton de color azul
        text = self.font.render("Seleccionar nivel", True, (255, 255, 255)) # Agregar texto al boton
        text_rect = text.get_rect(center=botonSeleccionarNivel.center) # Centrar el texto en el boton
        config_screen.blit(text, text_rect) # Mostrar el texto en el boton


        banderaEjecutandoNivel1 = True
        while banderaEjecutandoNivel1:
            if self.volver_menu: # Sí le dio click a la bandera de volver al menú, rompemos este ciclo y volvemos al anterior
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Eventos para los botones
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Sí le da click a la tecla de escape, se cierra la pantalla de configuración
                    self.juegoPausado = False
                    banderaEjecutandoNivel1 = False
                
                # Sí pasa el mouse sobre los botones
                elif event.type == pygame.MOUSEMOTION:
                    posicionMouse = event.pos # Rastreamos la posicion del mouse
                    # Revisamos sí el mouse está encima del botón
                    posicionMousePantallaConfiguración = (posicionMouse[0] - 150, posicionMouse[1] - 150) # Posición del mouse en la pantalla de configuración
                    
                    if botonReiniciarNivel.collidepoint(posicionMousePantallaConfiguración) or botonSeleccionarNivel.collidepoint(posicionMousePantallaConfiguración):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                

                # Sí le da click a los botones
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    posicionMouse = event.pos # Rastreamos la posicion del mouse
                    # Revisamos sí el mouse está encima del botón
                    posicionMousePantallaConfiguración = (posicionMouse[0] - 150, posicionMouse[1] - 150) # Posición del mouse en la pantalla de configuración
                    
                    if botonReiniciarNivel.collidepoint(posicionMousePantallaConfiguración): # Sí hace click en reiniciar nivel volvemos a cargar el nivel 1
                        banderaEjecutandoNivel1 = False
                        self.juegoPausado = False
                        self.setup(self.tmx_mapa_1) # Volvemos a cargar el mapa

                    elif botonSeleccionarNivel.collidepoint(posicionMousePantallaConfiguración): # Sí hace click en volver al menú, volv
                        self.volver_menu = True
                        banderaEjecutandoNivel1 = False
                        self.juegoPausado = False

            if self.capturarPantalla:
                self.mostrarSuperficieNivel.blit(self.capturarPantalla, (0, 0))

            # Oscurecemos la pantalla cuando le damos a pausa
            fondoOscuro = pygame.Surface(self.mostrarSuperficieNivel.get_size(), pygame.SRCALPHA) # Superficie transparente oscurecida
            fondoOscuro.fill((0, 0, 0, 150))  # Semi-transparent black
            self.mostrarSuperficieNivel.blit(fondoOscuro, (0, 0)) # Mostramos la pantalla del nivel oscura

            self.mostrarSuperficieNivel.blit(config_screen, (150, 150))  # Mostramos la pantalla de configuración

            pygame.display.flip() # Actualizamos la pantalla

    def pantallaArreglarAire(self):
        self.arreglo = False
       
       # Posición del menú de configuración dentro del juego
        configuracionWidthPantalla = self.mostrarSuperficieNivel.get_width() - 200
        configuracionHeightPantalla = self.mostrarSuperficieNivel.get_height() - 300

        # Creamos una nueva superficie para la pantalla de configuración
        config_screen = pygame.Surface((configuracionWidthPantalla, configuracionHeightPantalla))

        config_screen.fill(DARK_BLUE) 

        # Agregar boton para reiniciar nivel
        botonSolucionarNivel = pygame.Rect(50, 50, 200, 50) # Establecer tamaño del boton
        pygame.draw.rect(config_screen, LIGHTBLUE, botonSolucionarNivel) # dibujar el boton de color azul
        text = self.font.render("Arreglar Aire", True, (255, 255, 255)) # Agregar texto al boton
        text_rect = text.get_rect(center=botonSolucionarNivel.center) # Centrar el texto en el boton
        config_screen.blit(text, text_rect) # Mostrar el texto en el boton

        banderaEjecutandoNivel1 = True
        while banderaEjecutandoNivel1:
            if self.volver_menu: # Sí le dio click a la bandera de volver al menú, rompemos este ciclo y volvemos al anterior
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Eventos para los botones
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Sí le da click a la tecla de escape, se cierra la pantalla de configuración
                    self.juegoPausado = False
                    banderaEjecutandoNivel1 = False
                
                # Sí pasa el mouse sobre los botones
                elif event.type == pygame.MOUSEMOTION:
                    posicionMouse = event.pos # Rastreamos la posicion del mouse
                    # Revisamos sí el mouse está encima del botón
                    posicionMousePantallaConfiguración = (posicionMouse[0] - 150, posicionMouse[1] - 150) # Posición del mouse en la pantalla de configuración
                    
                    if botonSolucionarNivel.collidepoint(posicionMousePantallaConfiguración):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                

                # Sí le da click a los botones
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    posicionMouse = event.pos # Rastreamos la posicion del mouse
                    # Revisamos sí el mouse está encima del botón
                    posicionMousePantallaConfiguración = (posicionMouse[0] - 150, posicionMouse[1] - 150) # Posición del mouse en la pantalla de configuración
                    
                    if botonSolucionarNivel.collidepoint(posicionMousePantallaConfiguración): # Sí hace click en reiniciar nivel volvemos a cargar el nivel 1
                        print("Arreglando aire")
                        self.arreglo = True
                        banderaEjecutandoNivel1 = False
                        self.juegoPausado = False
                        pygame.event.clear()  # Limpiar la cola de eventos
                        break

            if banderaEjecutandoNivel1:  # Solo mostrar la pantalla de configuración si el bucle sigue activo
                self.mostrarSuperficieNivel.blit(config_screen, (150, 150))  # Mostramos la pantalla de configuración
                pygame.display.flip() # Actualizamos la pantalla

        if self.arreglo:
            print("Incrementando contador de oxígeno reparado.")
            self.contadorOxigenoReparado += 1
            self
    def pantallaPerdioNivel():
        pass