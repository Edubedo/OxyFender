import pygame
from utils.configuraciones import *
from os.path import join
from pytmx import *
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

        # Cargar y escalar la imagen de fondo
        self.imagen_fondo = pygame.image.load(join("assets", "img", "Background", "menu", "BackgroundCiudad.png")).convert()
        self.imagen_fondo_escalada = pygame.transform.scale(self.imagen_fondo, (self.mostrarSuperficieNivel.get_width(), self.mostrarSuperficieNivel.get_height() + 300))

        # Cargamos los sprites
        self.todos_los_sprites = pygame.sprite.Group()  # grupo de sprites para todos los sprites
        self.colisiones_sprites = pygame.sprite.Group()  # grupo de sprites para las colisiones
        self.elevador_piso1_sprites = pygame.sprite.Group()  # grupo de sprites para los elevadores del piso 1
        self.elevador_piso2_sprites = pygame.sprite.Group()  # grupo de sprites para los elevadores del piso 2
        self.filtro_sprites = pygame.sprite.Group()  # grupo de sprites para los elevadores
        self.capa_verificar_gano = pygame.sprite.Group()  # grupo de sprites para verificar si el jugador ganó
        
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

        tiempo_inicio = pygame.time.get_ticks()  # Tiempo de inicio del nivel
        self.setup(self.tmx_mapa_1, tiempo_inicio) # Inicializamos el nivel 1

    def setup(self, tmx_mapa_1, tiempo_inicio):
        self.tiempo_inicio = tiempo_inicio  # Guardar el tiempo de inicio

        # ------------------- AGREGAMOS LA BARRA DE OXIGENO ------------------- #
        self.rectBarraOxigeno = BarraOxigeno(10, 100, 40, 300, 200)
        self.rectBarraOxigeno.hp = 200

        # ------------------- BOTON DE PAUSA ------------------- #
        self.botonPausa = pygame.image.load(join("assets", "img", "BOTONES", "b_tuerca.png")).convert_alpha()
        self.botonPausa = pygame.transform.scale(self.botonPausa, (self.botonPausa.get_width(), self.botonPausa.get_height()))

        #  ------------------- Agregamos el conteo de Oxygens repaired y el objetivo x/y ------------------- #
        self.contadorOxigenoReparado = 0
        self.metaOxigenoReparado = 2

        self.ultimoTiempoCombustible = pygame.time.get_ticks()  # Tiempo inicial para el oxigeno

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Establecer cursor del mouse
        
        self.tmx_tileset = pygame.image.load(join("assets", "maps", "beginner", "level1", "lab_tileset_LITE.png")).convert_alpha()  # Texturas del piso y techo

        self.posicion_x_personaje = 0  # Agregamos esta variable para la posicion del personaje

        # ------------------- AGREGAMOS LAS CAPAS Y COLISIONES DEL MAPA ------------------- #
        for nombreCapa in ['Suelo', 'Paredes', 'Techo', 'FondoPiso1', 'FondoPiso2', 'AscensorPiso1', 'AscensorPiso2', 'capaVerificarGano', 'ParedDetener', 'Extra']:
            for x, y, superficie in tmx_mapa_1.get_layer_by_name(nombreCapa).tiles(): # Recorremos las capas del mapa de Tiled Y obtenemos las superficies

                # Estructuras
                sprite = Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), superficie, self.todos_los_sprites) # Creamos un sprite para las estructuras(capa)

                # Colisiones de las capas del mapa para cuando interactue con el jugador
                if nombreCapa in ['Paredes', 'Suelo', 'Techo', 'piso','ParedDetener']:
                    self.colisiones_sprites.add(sprite)

                # Elevadores de las capas del mapa para cuando interactue con el jugador
                if nombreCapa == 'AscensorPiso1':
                    self.elevador_piso1_sprites.add(sprite)
                elif nombreCapa == 'AscensorPiso2':
                    self.elevador_piso2_sprites.add(sprite)
                elif nombreCapa == 'capaVerificarGano':
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
        self.jugador = Player((800, 420), self.todos_los_sprites)  # Establecemos la pisición del jugador

        self.run() # Una vez cargadas las texturas y colisiones generales inicializamos el juego    

    def reset(self):
        # Reiniciar todos los estados relevantes
        self.rectBarraOxigeno.hp = 200
        self.contadorOxigenoReparado = 0
        self.ganoNivel = False
        self.perdioJuego = False
        self.juegoPausado = False
        self.ultimaVezTeletransportado = 0
        self.jugador.rect.topleft = (800, 420)  # Reiniciar la posición del jugador
        self.camera_offset = pygame.Vector2(0, 0)
        self.tiempo_inicio = pygame.time.get_ticks()  # Reiniciar el tiempo de inicio

    def run(self):
        pygame.mixer.music.pause()
        pygame.mixer.music.load(join("assets", "audio", "niveles", "musica_nivel_1.mp3"))
        pygame.mixer.music.play(1)
        pygame.mixer.music.set_volume(0.5)

        clock = pygame.time.Clock()
        gravedad = PLAYER_GRAVEDAD
        maxima_velocidad_caida = 4
        jugador_velocidad_y = 1
        esta_sobre_el_piso = False

        while True:
            if self.volver_menu:
                self.reset()  # Reiniciar el nivel cuando se vuelve al menú
                break

            tiempo_actual = pygame.time.get_ticks() - self.tiempo_inicio

            if tiempo_actual >= 120000:  # 120000 MILISEGUNDOS ES IGUAL 2 MINUTOS
                self.perdioJuego = True

            self.rectBarraOxigeno.actualizar_tiempo(tiempo_actual, self.juegoPausado)

            if self.perdioJuego:
                self.pantallaPerdioNivel()
                continue

            if self.ganoNivel:
                self.pantallaGanoNivel()
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
                            self.capturarPantalla = self.mostrarSuperficieNivel.copy()
                            pygame.mixer.music.pause()
                            self.jugador.sonido_pasos.stop()
                        else:
                            pygame.mixer.music.unpause()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.botonPausaRect.collidepoint(event.pos):
                        self.juegoPausado = not self.juegoPausado
                        if self.juegoPausado:
                            self.capturarPantalla = self.mostrarSuperficieNivel.copy()
                            pygame.mixer.music.pause()
                            self.jugador.sonido_pasos.stop()
                        else:
                            pygame.mixer.music.unpause()

            if self.juegoPausado:
                self.pantallaPausar()
                continue

            keys = pygame.key.get_pressed()
            movimientoJugador = pygame.Vector2(0, 0)
            estaMoviendose = False
            direccionPersonaje = "right"

            if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                movimientoJugador.x -= PLAYER_VEL
                estaMoviendose = True
                direccionPersonaje = "left"
            elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                movimientoJugador.x += PLAYER_VEL
                estaMoviendose = True
                direccionPersonaje = "right"
            if keys[pygame.K_SPACE] and esta_sobre_el_piso:
                jugador_velocidad_y = PLAYER_FUERZA_SALTO
                esta_sobre_el_piso = False
            if not esta_sobre_el_piso:
                jugador_velocidad_y += gravedad
                if jugador_velocidad_y > maxima_velocidad_caida:
                    jugador_velocidad_y = maxima_velocidad_caida
            movimientoJugador.y += jugador_velocidad_y

            self.jugador.rect.y += movimientoJugador.y
            spriteColisionesCapas = pygame.sprite.spritecollide(self.jugador, self.colisiones_sprites, False)

            for sprite in spriteColisionesCapas:
                if movimientoJugador.y > 0:
                    self.jugador.rect.bottom = sprite.rect.top
                    esta_sobre_el_piso = True
                    jugador_velocidad_y = 0
                elif movimientoJugador.y < 0:
                    self.jugador.rect.top = sprite.rect.bottom
                    jugador_velocidad_y = 0

            self.jugador.rect.x += movimientoJugador.x
            spriteColisionesCapas = pygame.sprite.spritecollide(self.jugador, self.colisiones_sprites, False)
            for sprite in spriteColisionesCapas:
                if movimientoJugador.x > 0:
                    self.jugador.rect.right = sprite.rect.left
                elif movimientoJugador.x < 0:
                    self.jugador.rect.left = sprite.rect.right

            tiempoActualElevadores = pygame.time.get_ticks()
            colisionesElevadoresPiso1 = pygame.sprite.spritecollide(self.jugador, self.elevador_piso1_sprites, False)
            colisionesElevadoresPiso2 = pygame.sprite.spritecollide(self.jugador, self.elevador_piso2_sprites, False)

            if (colisionesElevadoresPiso1 or colisionesElevadoresPiso2) and tiempoActualElevadores - self.ultimaVezTeletransportado > self.tiempoEsperadoElevador:
                rectTextoColisionElevador = pygame.image.load(join("assets", "img", "BOTONES", "img_click_x.png")).convert_alpha()
                rectTextoColisionElevador = pygame.transform.scale(rectTextoColisionElevador, (rectTextoColisionElevador.get_width() - 70, rectTextoColisionElevador.get_height() - 70))

                if keys[pygame.K_x]:
                    if colisionesElevadoresPiso1:
                        for elevator in self.elevador_piso2_sprites:
                            self.jugador.rect.topleft = elevator.rect.topleft
                            self.jugador.rect.y += (self.jugador.rect.height / 3)
                            self.ultimoElevador = elevator
                            self.ultimaVezTeletransportado = tiempoActualElevadores
                            break
                    elif colisionesElevadoresPiso2:
                        for elevator in self.elevador_piso1_sprites:
                            self.jugador.rect.topleft = elevator.rect.topleft
                            self.jugador.rect.y += (self.jugador.rect.height / 3)
                            self.ultimoElevador = elevator
                            self.ultimaVezTeletransportado = tiempoActualElevadores
                            break

            colisionesVerificarGano = pygame.sprite.spritecollide(self.jugador, self.capa_verificar_gano, False)

            if colisionesVerificarGano:
                for gano in colisionesVerificarGano:
                    if gano and self.contadorOxigenoReparado >= self.metaOxigenoReparado:
                        self.ganoNivel = True
                        break

            colisionesFiltros = pygame.sprite.spritecollide(self.jugador, self.filtro_sprites, False)

            if colisionesFiltros:
                for filtro in colisionesFiltros:
                    rectTextoArreglarFiltro = pygame.image.load(join("assets", "img", "BOTONES", "img_click_a.png")).convert_alpha()
                    rectTextoArreglarFiltro = pygame.transform.scale(rectTextoArreglarFiltro, (rectTextoArreglarFiltro.get_width() - 70, rectTextoArreglarFiltro.get_height() - 70))

                    if keys[pygame.K_a] and not self.juegoPausado:
                        self.juegoPausado = True
                        self.capturarPantalla = self.mostrarSuperficieNivel.copy()
                        self.pantallaArreglarAire()
                        self.juegoPausado = False

            self.camera_offset.x = self.jugador.rect.centerx - self.mostrarSuperficieNivel.get_width() // 2
            self.camera_offset.y = self.jugador.rect.centery - self.mostrarSuperficieNivel.get_height() // 2 - 40

            self.todos_los_sprites.update(estaMoviendose, direccionPersonaje, self.juegoPausado)

            self.screen.blit(self.imagen_fondo_escalada, (0, 0))

            for capa in self.tmx_mapa_1.visible_layers:
                if hasattr(capa, 'tiles'):
                    for x, y, image in capa.tiles():
                        self.mostrarSuperficieNivel.blit(image, (x * TILE_SIZE - self.camera_offset.x, y * TILE_SIZE - self.camera_offset.y))

            for sprite in self.todos_los_sprites:
                self.mostrarSuperficieNivel.blit(sprite.image, sprite.rect.topleft - self.camera_offset)

            if (colisionesElevadoresPiso1 or colisionesElevadoresPiso2) and tiempoActualElevadores - self.ultimaVezTeletransportado > self.tiempoEsperadoElevador:
                self.mostrarSuperficieNivel.blit(rectTextoColisionElevador, (self.mostrarSuperficieNivel.get_width() // 2, (self.mostrarSuperficieNivel.get_height() // 2) + 80))

            if colisionesFiltros:
                self.mostrarSuperficieNivel.blit(rectTextoArreglarFiltro, (self.mostrarSuperficieNivel.get_width() // 2, (self.mostrarSuperficieNivel.get_width() // 2) - 140))

            self.rectBarraOxigeno.draw(self.screen)

            self.fuenteTextoOxigenosReparados = pygame.font.Font(join("assets", "fonts", "Font_Menu_Options.ttf"), 25)
            self.textoOxigenosReparados = self.fuenteTextoOxigenosReparados.render(f"Oxygens repaired: {self.contadorOxigenoReparado}/{self.metaOxigenoReparado}", True, (255, 255, 255))
            self.mostrarSuperficieNivel.blit(self.textoOxigenosReparados, (10, 550))


            self.botonPausaRect = self.botonPausa.get_rect(center=(self.mostrarSuperficieNivel.get_width() - 50, 50))
            self.mostrarSuperficieNivel.blit(self.botonPausa, self.botonPausaRect.topleft)

            pygame.display.flip()

            clock.tick(FPS)

    def pantallaArreglarAire(self):
        self.tmx_filtroUnoNivel1 = load_pygame(join("assets", "maps", "filtros", "filtrosNivel1", "tuberia1.tmx"))  # Cargamos el mapa del nivel 1
        self.arreglo = False

        # Calcular el desplazamiento para centrar el mapa
        map_width = self.tmx_filtroUnoNivel1.width * self.tmx_filtroUnoNivel1.tilewidth
        map_height = self.tmx_filtroUnoNivel1.height * self.tmx_filtroUnoNivel1.tileheight
        offset_x = (self.mostrarSuperficieNivel.get_width() - map_width) // 2
        offset_y = (self.mostrarSuperficieNivel.get_height() - map_height) // 2

        # Crear botón "Fix filter"
        button_font = pygame.font.Font(None, 36)
        button_text = button_font.render("Fix filter", True, (255, 255, 255))
        button_rect = button_text.get_rect(center=(self.mostrarSuperficieNivel.get_width() // 2, self.mostrarSuperficieNivel.get_height() - 50))
        banderaEjecutandoNivel1 = True
        while banderaEjecutandoNivel1:
            if self.volver_menu:  # Sí le dio click a la bandera de volver al menú, rompemos este ciclo y volvemos al anterior
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Eventos para los botones
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Sí le da click a la tecla de escape, se cierra la pantalla de configuración
                    banderaEjecutandoNivel1 = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        self.arreglo = True
                        banderaEjecutandoNivel1 = False

            # Cambiar cursor si el mouse está sobre el botón
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if banderaEjecutandoNivel1:  # Solo mostrar la pantalla de configuración si el bucle sigue activo
                # Dibujar el mapa en la superficie principal
                for layer in self.tmx_filtroUnoNivel1.visible_layers:
                    if isinstance(layer, pytmx.TiledTileLayer):  # Si su instancia es de tipo Tile
                        for x, y, gid in layer:
                            tile = self.tmx_filtroUnoNivel1.get_tile_image_by_gid(gid)
                            if tile:
                                self.mostrarSuperficieNivel.blit(tile, (x * self.tmx_filtroUnoNivel1.tilewidth + offset_x, y * self.tmx_filtroUnoNivel1.tileheight + offset_y))

                # Dibujar el botón
                self.mostrarSuperficieNivel.blit(button_text, button_rect.topleft)

                pygame.display.flip()  # Actualizamos la pantalla

        if self.arreglo:
            self.contadorOxigenoReparado += 1  # Incrementar el contador de oxígeno reparado
             
    def pantallaPausar(self):
        # Posición del menú de configuración dentro del juego
        configuracionWidthPantalla = self.mostrarSuperficieNivel.get_width() - 100
        configuracionHeightPantalla = self.mostrarSuperficieNivel.get_height() - 250

        # Creamos una nueva superficie para la pantalla de configuración
        config_screen = pygame.Surface((configuracionWidthPantalla, configuracionHeightPantalla), pygame.SRCALPHA)

        imgFondoMenu = pygame.image.load(join("assets", "img", "FONDOS", "dificultad_fondo-removebg-preview.png")).convert_alpha()
        imgFondoMenu = pygame.transform.scale(imgFondoMenu, (configuracionWidthPantalla, configuracionHeightPantalla))
        config_screen.blit(imgFondoMenu, (0, 0))

        # Agregar título "Menú"
        fontTitulo = pygame.font.Font(join("assets", "fonts", "Transformers Movie.ttf"), 100)
        titulo = fontTitulo.render("Menu", True, AZUL_TITULO)
        titulo_rect = titulo.get_rect(center=(configuracionWidthPantalla // 2, 100))
        config_screen.blit(titulo, titulo_rect)

        # Agregar boton para reiniciar nivel 
        botonReiniciarNivel = pygame.image.load(join("assets", "img", "BOTONES", "b_reiniciar.png")).convert_alpha()
        botonReiniciarNivel = pygame.transform.scale(botonReiniciarNivel, (botonReiniciarNivel.get_width() + 20, botonReiniciarNivel.get_height() + 20))
        botonReiniciarNivelRect = botonReiniciarNivel.get_rect()
        botonReiniciarNivelRect.center = ((configuracionWidthPantalla // 2) - 50, configuracionHeightPantalla // 2 + 50)
        config_screen.blit(botonReiniciarNivel, botonReiniciarNivelRect.topleft)

        # Agregar boton para volver a seleccionar nivel
        botonSeleccionarNivel = pygame.image.load(join("assets", "img", "BOTONES", "b_seleccionar.png")).convert_alpha()
        botonSeleccionarNivel = pygame.transform.scale(botonSeleccionarNivel, (botonSeleccionarNivel.get_width() + 20, botonSeleccionarNivel.get_height() + 20))
        botonSeleccionarNivelRect = botonSeleccionarNivel.get_rect()
        botonSeleccionarNivelRect.center = ((configuracionWidthPantalla // 2) + 50, configuracionHeightPantalla // 2 + 50)
        config_screen.blit(botonSeleccionarNivel, botonSeleccionarNivelRect.topleft)

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
                    pygame.mixer.music.unpause()  # Reanudar la música
                
                # Sí pasa el mouse sobre los botones
                elif event.type == pygame.MOUSEMOTION:
                    posicionMouse = event.pos # Rastreamos la posicion del mouse
                    # Revisamos sí el mouse está encima del botón
                    posicionMousePantallaConfiguración = (posicionMouse[0] - 150, posicionMouse[1] - 150) # Posición del mouse en la pantalla de configuración
                    
                    if botonReiniciarNivelRect.collidepoint(posicionMousePantallaConfiguración) or botonSeleccionarNivelRect.collidepoint(posicionMousePantallaConfiguración):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                

                # Sí le da click a los botones
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    posicionMouse = event.pos # Rastreamos la posicion del mouse
                    # Revisamos sí el mouse está encima del botón
                    posicionMousePantallaConfiguración = (posicionMouse[0] - 150, posicionMouse[1] - 150) # Posición del mouse en la pantalla de configuración
                    
                    if botonReiniciarNivelRect.collidepoint(posicionMousePantallaConfiguración): # Sí hace click en reiniciar nivel volvemos a cargar el nivel 1
                        banderaEjecutandoNivel1 = False
                        self.juegoPausado = False
                        tiempo_inicio = pygame.time.get_ticks()  # Tiempo de inicio del nivel
                        self.setup(self.tmx_mapa_1, tiempo_inicio) # Volvemos a cargar el mapa

                    elif botonSeleccionarNivelRect.collidepoint(posicionMousePantallaConfiguración): # Sí hace click en volver al menú, volv
                        self.volver_menu = True
                        banderaEjecutandoNivel1 = False
                        self.juegoPausado = False

                        # * Música de fondo 
                        pygame.mixer.music.stop() # Pausar la música actual
                        # pygame.mixer.music.load(join("assets", "audio", "music", "let_us_adore_you.mp3")) # Cargar la música del menú
                        # pygame.mixer.music.play(-1) # Reproducir la música en bucle
                        # pygame.mixer.music.set_volume(0.2)

            if self.capturarPantalla:
                self.mostrarSuperficieNivel.blit(self.capturarPantalla, (0, 0))

            # Oscurecemos la pantalla cuando le damos a pausa
            fondoOscuro = pygame.Surface(self.mostrarSuperficieNivel.get_size(), pygame.SRCALPHA) # Superficie transparente oscurecida
            fondoOscuro.fill((0, 0, 0, 150))  # Semi-transparent black
            self.mostrarSuperficieNivel.blit(fondoOscuro, (0, 0)) # Mostramos la pantalla del nivel oscura

            self.mostrarSuperficieNivel.blit(config_screen, (150, 150))  # Mostramos la pantalla de configuración

            pygame.display.flip() # Actualizamos la pantalla

    def pantallaPerdioNivel(self):
        # Crear una superficie semi-transparente
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Negro con 50% de opacidad
        self.screen.blit(overlay, (0, 0))

        # Mostrar mensaje de que el jugador perdió
        # Agregar texto de que perdió nivel
        imagePerdio = pygame.image.load(join("assets", "img", "PantallasFinales", "gameOver_en.png")).convert_alpha()
        imagePerdio = pygame.transform.scale(imagePerdio, (imagePerdio.get_width(), imagePerdio.get_height()))
        self.screen.blit(imagePerdio, (0, self.mostrarSuperficieNivel.get_height() // 2))

        # Agregar boton para reiniciar nivel 
        botonReiniciarNivel = pygame.image.load(join("assets", "img", "BOTONES", "b_reiniciar.png")).convert_alpha()
        botonReiniciarNivel = pygame.transform.scale(botonReiniciarNivel, (botonReiniciarNivel.get_width() + 20, botonReiniciarNivel.get_height() + 20))
        botonReiniciarNivelRect = botonReiniciarNivel.get_rect(center=((self.mostrarSuperficieNivel.get_width() // 2) - 100, (self.mostrarSuperficieNivel.get_height() // 2) + 150))
        self.screen.blit(botonReiniciarNivel, botonReiniciarNivelRect.topleft)

        # Agregar boton para volver a seleccionar nivel
        botonSeleccionarNivel = pygame.image.load(join("assets", "img", "BOTONES", "b_seleccionar.png")).convert_alpha()
        botonSeleccionarNivel = pygame.transform.scale(botonSeleccionarNivel, (botonSeleccionarNivel.get_width() + 20, botonSeleccionarNivel.get_height() + 20))
        botonSeleccionarNivelRect = botonSeleccionarNivel.get_rect(center=((self.mostrarSuperficieNivel.get_width() // 2) + 100, (self.mostrarSuperficieNivel.get_height() // 2) + 150))
        self.screen.blit(botonSeleccionarNivel, botonSeleccionarNivelRect.topleft)

        pygame.display.flip()

        banderaEjecutandoNivel1 = True
        while banderaEjecutandoNivel1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Sí pasa el mouse sobre los botones
                elif event.type == pygame.MOUSEMOTION:
                    posicionMouse = event.pos  # Rastreamos la posicion del mouse
                    if botonReiniciarNivelRect.collidepoint(posicionMouse) or botonSeleccionarNivelRect.collidepoint(posicionMouse):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                # Sí le da click a los botones
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    posicionMouse = event.pos  # Rastreamos la posicion del mouse
                    if botonReiniciarNivelRect.collidepoint(posicionMouse):  # Sí hace click en reiniciar nivel volvemos a cargar el nivel 1
                        banderaEjecutandoNivel1 = False
                        self.perdioJuego = False
                        tiempo_inicio = pygame.time.get_ticks()  # Tiempo de inicio del nivel
                        self.setup(self.tmx_mapa_1, tiempo_inicio)  # Volvemos a cargar el mapa

                    elif botonSeleccionarNivelRect.collidepoint(posicionMouse):  # Sí hace click en volver al menú
                        self.volver_menu = True
                        banderaEjecutandoNivel1 = False
                        self.perdioJuego = False

                        # * Música de fondo 
                        pygame.mixer.music.pause()  # Pausar la música actual
                        pygame.mixer.music.load(join("assets", "audio", "music", "let_us_adore_you.mp3"))  # Cargar la música del menú
                        pygame.mixer.music.play(-1)  # Reproducir la música en bucle
                        pygame.mixer.music.set_volume(0.2)

    def pantallaGanoNivel(self):
        # Crear una superficie semi-transparente
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA) # ponemo s el fondo oscuro 
        overlay.fill((0, 0, 0, 128))  # Negro con 50% de opacidad
        self.screen.blit(overlay, (0, 0))

        # Mostrar mensaje de que el jugador perdió
        # Agregar texto de que perdió nivel
        imagePerdio = pygame.image.load(join("assets", "img", "PantallasFinales", "missionCompleted_en.png")).convert_alpha()
        imagePerdio = pygame.transform.scale(imagePerdio, (imagePerdio.get_width(), imagePerdio.get_height()))
        self.screen.blit(imagePerdio, (0, self.mostrarSuperficieNivel.get_height() // 2))

        # Agregar boton para siguiente nivel 
        botonSiguienteNivel = pygame.image.load(join("assets", "img", "BOTONES", "b_siguiente.png")).convert_alpha()
        botonSiguienteNivel = pygame.transform.scale(botonSiguienteNivel, (botonSiguienteNivel.get_width() + 20, botonSiguienteNivel.get_height() + 20))
        botonSiguienteNivelRect = botonSiguienteNivel.get_rect(center=((self.mostrarSuperficieNivel.get_width() // 2) - 100, (self.mostrarSuperficieNivel.get_height() // 2) + 150))
        self.screen.blit(botonSiguienteNivel, botonSiguienteNivelRect.topleft)

        # Agregar boton para volver a seleccionar nivel
        botonSeleccionarNivel = pygame.image.load(join("assets", "img", "BOTONES", "b_seleccionar.png")).convert_alpha()
        botonSeleccionarNivel = pygame.transform.scale(botonSeleccionarNivel, (botonSeleccionarNivel.get_width() + 20, botonSeleccionarNivel.get_height() + 20))
        botonSeleccionarNivelRect = botonSeleccionarNivel.get_rect(center=((self.mostrarSuperficieNivel.get_width() // 2) + 100, (self.mostrarSuperficieNivel.get_height() // 2) + 150))
        self.screen.blit(botonSeleccionarNivel, botonSeleccionarNivelRect.topleft)

        pygame.display.flip()

        banderaEjecutandoNivel1 = True
        while banderaEjecutandoNivel1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Sí pasa el mouse sobre los botones
                elif event.type == pygame.MOUSEMOTION:
                    posicionMouse = event.pos  # Rastreamos la posicion del mouse
                    if botonSiguienteNivelRect.collidepoint(posicionMouse) or botonSeleccionarNivelRect.collidepoint(posicionMouse):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                # Sí le da click a los botones
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    posicionMouse = event.pos  # Rastreamos la posicion del mouse
                    if botonSiguienteNivelRect.collidepoint(posicionMouse):  # Sí hace click en siguiente nivel volvemos a cargar el nivel 1
                        self.volver_menu = True
                        banderaEjecutandoNivel1 = False
                        self.perdioJuego = False

                        # * Música de fondo 
                        pygame.mixer.music.pause()  # Pausar la música actual
                        pygame.mixer.music.load(join("assets", "audio", "music", "let_us_adore_you.mp3"))  # Cargar la música del menú
                        pygame.mixer.music.play(-1)  # Reproducir la música en bucle
                        pygame.mixer.music.set_volume(0.2)

                    elif botonSeleccionarNivelRect.collidepoint(posicionMouse):  # Sí hace click en volver al menú
                        self.volver_menu = True
                        banderaEjecutandoNivel1 = False
                        self.perdioJuego = False

                        # * Música de fondo 
                        pygame.mixer.music.pause()  # Pausar la música actual
                        pygame.mixer.music.load(join("assets", "audio", "music", "let_us_adore_you.mp3"))  # Cargar la música del menú
                        pygame.mixer.music.play(-1)  # Reproducir la música en bucle
                        pygame.mixer.music.set_volume(0.2)

    