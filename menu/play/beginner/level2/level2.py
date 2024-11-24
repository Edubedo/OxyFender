import pygame
from utilerias.configuraciones import *
from os.path import join
from pytmx import *
import sys
from utilerias.sprites import Sprite
from utilerias.jugador import Player
from utilerias.clases.barraOxigeno import BarraOxigeno
from utilerias.sprites import FiltroSprite

class Level2Beginner:
    def __init__(self, name, dificultadNivel, id, configLanguage, datosLanguage, volumen):
        self.name = name
        self.dificultadNivel = dificultadNivel
        self.id = id
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.configLanguage = configLanguage
        self.datosLanguage = datosLanguage
        self.volumen = volumen

        pygame.display.set_caption(f"{TITLE_GAME} - {name}")


        self.mostrarSuperficieNivel = pygame.display.get_surface()

        self.imagen_fondo = pygame.image.load(join("assets", "img", "Background", "menu", "fondo.png")).convert()
        self.imagen_fondo_escalada = pygame.transform.scale(self.imagen_fondo, (self.mostrarSuperficieNivel.get_width(), self.mostrarSuperficieNivel.get_height() + 300))

        self.todos_los_sprites = pygame.sprite.Group()
        self.colisiones_sprites = pygame.sprite.Group()
        self.filtro_sprites = pygame.sprite.Group()
        self.capa_verificar_gano = pygame.sprite.Group()

        self.tmx_mapa_2 = load_pygame(join("assets", "maps", "beginner", "level2", "nivel_bunker_nv.tmx"))

        self.camera_offset = pygame.Vector2(0, 0)
        self.jugador = None

        self.font = pygame.font.Font(None, 36)

        self.juegoPausado = False
        self.juegoPausadoControles = False
        self.capturarPantalla = None
        self.volver_menu = False

        self.ganoNivel = False
        self.perdioJuego = False

        self.filtros_arreglados = []  # Lista para almacenar los filtros arreglados
        self.filtro_pares = {}  # Diccionario para almacenar los pares de filtros

        tiempo_inicio = pygame.time.get_ticks()
        self.setup(self.tmx_mapa_2, tiempo_inicio)

    def setup(self, tmx_mapa_2, tiempo_inicio):
        # Cargar sonido de clic
        self.sonidoDeClick = pygame.mixer.Sound(join("assets", "audio", "utilerias", "click_madera.mp3"))
        self.sonidoDeClick.set_volume(1 if self.volumen == "on" else 0)

        # Initialize rectBarraOxigeno
        self.tiempo_inicio = tiempo_inicio

        self.rectBarraOxigeno = BarraOxigeno(20, 100, 40, 300, 200) #a
        self.rectBarraOxigeno.hp = 200
        self.rectBarraOxigeno.reiniciar()  # Llamar al método reiniciar de BarraOxigeno

        # Botón de pausa
        self.botonPausa = pygame.image.load(join("assets", "img", "BOTONES", "botones_bn", "b_tuerca_bn.png")).convert_alpha()
        self.botonPausa = pygame.transform.scale(self.botonPausa, (self.botonPausa.get_width(), self.botonPausa.get_height()))
        self.botonPausaRect = self.botonPausa.get_rect(center=(self.mostrarSuperficieNivel.get_width() - 50, 50))

        # Botón de controles
        self.botonControles = pygame.image.load(join("assets", "img", "BOTONES", "botones_bn", "b_int_naranja.png")).convert_alpha()
        self.botonControles = pygame.transform.scale(self.botonControles, (self.botonControles.get_width(), self.botonControles.get_height()))
        self.botonControlesRect = self.botonControles.get_rect(center=(self.mostrarSuperficieNivel.get_width() - 50, 500))

        self.filtro_bn = pygame.image.load(join("assets", "img", "filtros", "filtro_bn.png")).convert_alpha() # Cargar la imagen del filtro en blanco
        self.filtro_color = pygame.image.load(join("assets", "img", "filtros", "filtro_color.png")).convert_alpha() # Cargar la imagen del filtro a color

        self.filtro_bn = pygame.transform.scale(self.filtro_bn, (self.filtro_bn.get_width() + 40, self.filtro_bn.get_height() + 40)) # Escalar la imagen
        self.filtro_color = pygame.transform.scale(self.filtro_color, (self.filtro_color.get_width() + 40, self.filtro_color.get_height() + 40)) # Escalar la imagen

        self.contadorOxigenoReparado = 0
        self.metaOxigenoReparado = 2

        self.ultimoTiempoCombustible = pygame.time.get_ticks()
        # ! CODIGO 1 MOSTRAR
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) # Establecer el cursor del mouse como una flecha

        # join es una función que une las rutas de los archivos
        self.tmx_tileset = pygame.image.load(join("assets", "maps", "beginner", "level1", "lab_tileset_LITE.png")).convert_alpha() # Cargar el tileset que son las imagenes del mapa de tiled que usaremos posteriomente

        self.posicion_x_personaje = 0
        # Nos pasamos el mapa principal tmx_mapa_2 por parametros desde el init y ahora lo estamos usando para dibujar los elementos

        self.filtro_imagenes = [
            pygame.image.load(join("assets", "sprites", "filtro", f"FILTRO{i}.png")).convert_alpha()
            for i in range(1, 7)
        ]

       # Dibujamos los elementos generales del mapa
        for nombreCapa in ['base','capaVerificarGano','CapaNoPasar','Pared','escalones','fondo_tierra']:
            for x, y, superficie in tmx_mapa_2.get_layer_by_name(nombreCapa).tiles(): # obtenemos la capa por nombre que se obtiene x, y, la superficie(imagenes)
                sprite = Sprite((((x * TILE_SIZE) - self.posicion_x_personaje, y * TILE_SIZE)), superficie, self.todos_los_sprites) # Creamos un sprite con la posición x, y y la superficie
                if nombreCapa in ['Pared','escalones', 'fondo_tierra','CapaNoPasar']:
                    self.colisiones_sprites.add(sprite)
                elif nombreCapa == 'capaVerificarGano':
                    self.capa_verificar_gano.add(sprite)


        # Dibujamos los filtros de aire
        filtooo_layer = tmx_mapa_2.get_layer_by_name('filtooo')
        for obj in filtooo_layer:
            if obj.name == 'arribaFiltro1' or obj.name == 'arribaFiltro2':
                sprite = Sprite((obj.x + 550, obj.y - 30), self.filtro_imagenes[0], self.todos_los_sprites)
                sprite.name = obj.name  # Añadir el nombre al sprite
                sprite.indice_imagen = 0  # Inicializar el índice de la imagen
                sprite.ultimo_cambio = 0  # Inicializar el tiempo del último cambio
                self.filtro_sprites.add(sprite)
                # Agrupar los filtros en pares
                if 'abajoFiltro' in obj.name:
                    pair_name = obj.name.replace('abajoFiltro', 'arribaFiltro')
                    self.filtro_pares[obj.name] = pair_name
                elif 'arribaFiltro' in obj.name:
                    pair_name = obj.name.replace('arribaFiltro', 'abajoFiltro')
                    self.filtro_pares[obj.name] = pair_name


        # Dibujamos los objetos del mapa
        # for nombreObjeto in ['Objetos']:
        #     for obj in tmx_mapa_2.get_layer_by_name(nombreObjeto):
        #         sprite = Sprite((obj.x, obj.y), obj.image, self.todos_los_sprites)

        # Dibujamos el jugador
        self.jugador = Player((830,700), self.todos_los_sprites)

        # Reiniciamos configuraciones antes de inciiar el juego
        self.reiniciarConfiguraciones()

        # Empezamos con el juego
        self.run()

   
    def run(self):
        pygame.mixer.music.pause()
        pygame.mixer.music.load(join("assets", "audio", "niveles", "level2.mp3"))
        pygame.mixer.music.play(1)
        pygame.mixer.music.set_volume(0.5 if self.volumen == "on" else 0)

        clock = pygame.time.Clock()
        gravedad = PLAYER_GRAVEDAD
        maxima_velocidad_caida = 4
        jugador_velocidad_y = 1
        esta_sobre_el_piso = False
        self.tiempo_actual = 0

        while True:
            if self.volver_menu:
                self.reiniciarConfiguraciones()  # Reiniciar el nivel cuando se vuelve al menú
                break

            tiempo_actual = pygame.time.get_ticks()

            if not self.juegoPausado:
                self.tiempo_actual += 1000 // FPS
            else:
                self.tiempo_actual = self.tiempo_inicio

            # Si el juego esta pausado
            if self.tiempo_actual >= 120000:  # 120000 MILISEGUNDOS ES IGUAL 2 MINUTOS
                self.perdioJuego = True

            self.rectBarraOxigeno.actualizar_tiempo(self.tiempo_actual, self.juegoPausado)

            if self.botonPausaRect.collidepoint(pygame.mouse.get_pos()) or self.botonControlesRect.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
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
                    self.menuPausa()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Cuando de la click al boton de pausa
                    if self.botonPausaRect.collidepoint(event.pos):
                        self.sonidoDeClick.play() # Cuando hace un click dentro de las opciones del menú
                        self.menuPausa()
                    # cuando le da click al boton de controles
                    elif self.botonControlesRect.collidepoint(event.pos):
                        self.sonidoDeClick.play()
                        self.menuControles()

            if self.juegoPausado:
                self.pantallaPausar()
                continue

            if self.juegoPausadoControles:
                self.pantallaControles()
                continue

            if not self.teletransportando:
                keys = pygame.key.get_pressed()
                movimientoJugador = pygame.Vector2(0, 0)
                estaMoviendose = False
                estaSaltando = False
                direccionPersonaje = self.jugador.direction  # Mantener la dirección actual
                #esta_sobre_el_piso_K = False

                if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]: # No puede presionar las teclas izquierda y derecha al mismo tiempo
                    #esta_sobre_el_piso = False
                    #esta_sobre_el_piso_K=True
                    movimientoJugador.x -= PLAYER_VEL - 1
                    estaMoviendose = True
                    direccionPersonaje = "left"
                elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]: # No puede presionar las teclas izquierda y derecha al mismo tiempo
                    #esta_sobre_el_piso = False
                    #esta_sobre_el_piso_K=True
                    movimientoJugador.x += PLAYER_VEL
                    estaMoviendose = True
                    direccionPersonaje = "right" 
                if keys[pygame.K_SPACE] and (esta_sobre_el_piso) and not estaSaltando:
                    esta_sobre_el_piso_K=False
                    jugador_velocidad_y = PLAYER_FUERZA_SALTO
                    esta_sobre_el_piso = False
                    estaSaltando = True
                if not esta_sobre_el_piso:
                    jugador_velocidad_y += gravedad
                    if jugador_velocidad_y > maxima_velocidad_caida:
                        jugador_velocidad_y = maxima_velocidad_caida
                esta_sobre_el_piso = False
                movimientoJugador.y += jugador_velocidad_y

                # Reemplaza esta sección en el método run
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
                    else:
                        esta_sobre_el_piso = False  # Asegúrate de que el jugador no esté sobre el piso si no hay colisión

                # Reemplaza esta sección en el método run
                self.jugador.rect.x += movimientoJugador.x
            spriteColisionesCapas = pygame.sprite.spritecollide(self.jugador, self.colisiones_sprites, False)
            for sprite in spriteColisionesCapas:
                if movimientoJugador.x > 0:
                    self.jugador.rect.right = sprite.rect.left
                    # Ajustar la posición en Y para subir escalones solo si está en contacto con ellos
                    if 0 < sprite.rect.top - self.jugador.rect.bottom <= 32:
                        self.jugador.rect.bottom = sprite.rect.top
                        esta_sobre_el_piso = True
                        jugador_velocidad_y = 0
                elif movimientoJugador.x < 0:
                    self.jugador.rect.left = sprite.rect.right
                    # Ajustar la posición en Y para subir escalones solo si está en contacto con ellos
                    if 0 < sprite.rect.top - self.jugador.rect.bottom <= 32:
                        self.jugador.rect.bottom = sprite.rect.top
                        esta_sobre_el_piso = True
                        jugador_velocidad_y = 0

            # Actualizar los sprites de los filtros
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - getattr(self, 'ultimo_cambio_filtro', 0) > 1100:  # 2000 ms = 2 segundos
                for sprite in self.filtro_sprites:
                    if sprite.name not in self.filtros_arreglados:
                        # Animar los filtros no reparados
                        sprite.indice_imagen = (getattr(sprite, 'indice_imagen', 0) + 1) % 6
                        sprite.image = self.filtro_imagenes[sprite.indice_imagen]
                    else:
                        # Usar solo la imagen 0 si el filtro está reparado
                        sprite.image = self.filtro_imagenes[0]
                    self.ultimo_cambio_filtro = tiempo_actual

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

                    if keys[pygame.K_a]:
                        self.capturarPantalla = self.mostrarSuperficieNivel.copy()

                        pantalla = self.pantallaLaberinto()

                        if pantalla == 1:
                            # Arreglar ambos filtros del par
                            pair_name = self.filtro_pares[filtro.name]
                            for sprite in self.filtro_sprites:
                                if sprite.name == filtro.name or sprite.name == pair_name:
                                    self.filtros_arreglados.append(sprite)
                                    self.filtro_sprites.remove(sprite)
                                    sprite.image = self.filtro_imagenes[0]
                            break

            self.camera_offset.x = self.jugador.rect.centerx - self.mostrarSuperficieNivel.get_width() // 2
            self.camera_offset.y = self.jugador.rect.centery - self.mostrarSuperficieNivel.get_height() // 2 - 100

            self.todos_los_sprites.update(estaMoviendose, direccionPersonaje, self.juegoPausado)

            self.screen.blit(self.imagen_fondo_escalada, (0, 0))

            for capa in self.tmx_mapa_2.visible_layers:
                if hasattr(capa, 'tiles'):
                    for x, y, image in capa.tiles():
                        self.mostrarSuperficieNivel.blit(image, (x * TILE_SIZE - self.camera_offset.x, y * TILE_SIZE - self.camera_offset.y))

            for sprite in self.todos_los_sprites:
                self.mostrarSuperficieNivel.blit(sprite.image, sprite.rect.topleft - self.camera_offset)

            # Dibujar los sprites del filtro al frente
            self.filtro_sprites.draw(self.mostrarSuperficieNivel)

            if colisionesFiltros:
                self.mostrarSuperficieNivel.blit(rectTextoArreglarFiltro, (self.mostrarSuperficieNivel.get_width() // 2, (self.mostrarSuperficieNivel.get_width() // 2) - 140))

            self.rectBarraOxigeno.draw(self.screen)

            # Dibujar filtros de aire que le faltan
            self.dibujar_filtros()

            # Render the text in white color
            self.fuenteTextoOxigenosReparados = pygame.font.Font(join("assets", "fonts", "Triforce.ttf"), 50)
            self.textoOxigenosReparados = self.fuenteTextoOxigenosReparados.render(f"{self.datosLanguage[self.configLanguage]['levelsBeginner']['level1']['levelMission']}", True, (255, 255, 255))

            border_offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for offset in border_offsets:
                border_text = self.fuenteTextoOxigenosReparados.render(f"{self.datosLanguage[self.configLanguage]['levelsBeginner']['level1']['levelMission']}", True, (0, 0, 0))
                self.mostrarSuperficieNivel.blit(border_text, (10 + offset[0], 500 + offset[1]))

            self.mostrarSuperficieNivel.blit(self.textoOxigenosReparados, (10, 500))

            #Boton de pausa
            self.botonPausaRect = self.botonPausa.get_rect(center=(self.mostrarSuperficieNivel.get_width() - 50, 50))
            self.mostrarSuperficieNivel.blit(self.botonPausa, self.botonPausaRect.topleft)

            #Boton de controles
            self.botonControlesRect = self.botonControles.get_rect(center=(self.mostrarSuperficieNivel.get_width() - 50, 500))
            self.mostrarSuperficieNivel.blit(self.botonControles, self.botonControlesRect.topleft)


            pygame.display.flip()

            clock.tick(FPS)
    
    def menuPausa(self):
        self.juegoPausado = not self.juegoPausado
        if self.juegoPausado:
            self.capturarPantalla = self.mostrarSuperficieNivel.copy()
            pygame.mixer.music.pause()
            self.jugador.sonido_pasos.stop()
        else:
            pygame.mixer.music.unpause()

    def pantallaPausar(self):
        configuracionWidthPantalla = self.mostrarSuperficieNivel.get_width()
        configuracionHeightPantalla = self.mostrarSuperficieNivel.get_height()
        config_screen = pygame.Surface((configuracionWidthPantalla, configuracionHeightPantalla), pygame.SRCALPHA)

        fondoSuperior = pygame.image.load(join("assets", "img", "FONDOS", "marco_superior.png")).convert_alpha()
        fondoSuperior = pygame.transform.scale(fondoSuperior, (fondoSuperior.get_width() + 20, fondoSuperior.get_height() + 20))
        fondoSuperiorRect = fondoSuperior.get_rect(center=(configuracionWidthPantalla // 2, configuracionHeightPantalla // 2 - 80))
        config_screen.blit(fondoSuperior, fondoSuperiorRect.topleft)

        # Cargar y escalar los botones
        botonContinuarMenu = pygame.image.load(join("assets", "img", "BOTONES", "botones_bn", "b_continuar.png")).convert_alpha()
        botonContinuarMenu = pygame.transform.scale(botonContinuarMenu, (botonContinuarMenu.get_width() + 20, botonContinuarMenu.get_height() + 20))

        botonReiniciarNivel = pygame.image.load(join("assets", "img", "BOTONES", "botones_bn", "b_reiniciar.png")).convert_alpha()
        botonReiniciarNivel = pygame.transform.scale(botonReiniciarNivel, (botonReiniciarNivel.get_width() + 20, botonReiniciarNivel.get_height() + 20))

        botonSeleccionarNivel = pygame.image.load(join("assets", "img", "BOTONES", "botones_bn", "b_seleccionar.png")).convert_alpha()
        botonSeleccionarNivel = pygame.transform.scale(botonSeleccionarNivel, (botonSeleccionarNivel.get_width() + 20, botonSeleccionarNivel.get_height() + 20))

        # Calcular las posiciones de los botones para que estén alineados horizontalmente
        espacio_entre_botones = 20
        total_ancho_botones = botonContinuarMenu.get_width() + botonReiniciarNivel.get_width() + botonSeleccionarNivel.get_width() + 2 * espacio_entre_botones
        inicio_x = (configuracionWidthPantalla - total_ancho_botones) // 2
        centro_y = configuracionHeightPantalla // 2

        # Posicionar y dibujar los botones
        botonContinuarMenuRect = botonContinuarMenu.get_rect(topleft=(inicio_x, centro_y))
        config_screen.blit(botonContinuarMenu, botonContinuarMenuRect.topleft)

        botonReiniciarNivelRect = botonReiniciarNivel.get_rect(topleft=(inicio_x + botonContinuarMenu.get_width() + espacio_entre_botones, centro_y))
        config_screen.blit(botonReiniciarNivel, botonReiniciarNivelRect.topleft)

        botonSeleccionarNivelRect = botonSeleccionarNivel.get_rect(topleft=(inicio_x + botonContinuarMenu.get_width() + botonReiniciarNivel.get_width() + 2 * espacio_entre_botones, centro_y))
        config_screen.blit(botonSeleccionarNivel, botonSeleccionarNivelRect.topleft)

        fondoInferior = pygame.image.load(join("assets", "img", "FONDOS", "marco_inferior.png")).convert_alpha()
        fondoInferior = pygame.transform.scale(fondoInferior, (fondoInferior.get_width() + 20, fondoInferior.get_height() + 20))
        fondoInferiorRect = fondoInferior.get_rect(center=(configuracionWidthPantalla // 2, configuracionHeightPantalla // 2 + 140))

        config_screen.blit(fondoInferior, fondoInferiorRect.topleft)
        banderaEjecutandoNivel1 = True
        while banderaEjecutandoNivel1:
            if self.volver_menu:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.juegoPausado = False
                    banderaEjecutandoNivel1 = False
                    pygame.mixer.music.unpause()
                elif event.type == pygame.MOUSEMOTION:
                    posicionMouse = event.pos
                    if (botonReiniciarNivelRect.collidepoint(posicionMouse) or 
                        botonSeleccionarNivelRect.collidepoint(posicionMouse) or 
                        botonContinuarMenuRect.collidepoint(posicionMouse)):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    posicionMouse = event.pos
                    if botonReiniciarNivelRect.collidepoint(posicionMouse):
                        self.sonidoDeClick.play() # Cuando hace un click dentro de las opciones del menú
                        banderaEjecutandoNivel1 = False
                        self.juegoPausado = False
                        tiempo_inicio = pygame.time.get_ticks()
                        self.setup(self.tmx_mapa_2, tiempo_inicio)

                    elif botonSeleccionarNivelRect.collidepoint(posicionMouse):
                        self.sonidoDeClick.play() # Cuando hace un click dentro de las opciones del menú
                        self.volver_menu = True
                        banderaEjecutandoNivel1 = False
                        self.juegoPausado = False
                        pygame.mixer.music.stop()

                        # poner la musica de let us adore you
                        pygame.mixer.music.load(join("assets", "audio", "music", "let_us_adore_you.mp3")) # Cargar la música
                        pygame.mixer.music.play(-1) # Reproducir la música en bucle
                        pygame.mixer.music.set_volume(1 if self.volumen == "on" else 0)

                    elif botonContinuarMenuRect.collidepoint(posicionMouse):
                        self.sonidoDeClick.play() # Cuando hace un click dentro de las opciones del menú
                        self.juegoPausado = False
                        banderaEjecutandoNivel1 = False
                        pygame.mixer.music.unpause()

            if self.capturarPantalla:
                self.mostrarSuperficieNivel.blit(self.capturarPantalla, (0, 0))

            fondoOscuro = pygame.Surface(self.mostrarSuperficieNivel.get_size(), pygame.SRCALPHA)
            fondoOscuro.fill((0, 0, 0, 150))
            self.mostrarSuperficieNivel.blit(fondoOscuro, (0, 0))

            config_screen_rect = config_screen.get_rect(center=(self.mostrarSuperficieNivel.get_width() // 2, self.mostrarSuperficieNivel.get_height() // 2))
            self.mostrarSuperficieNivel.blit(config_screen, config_screen_rect.topleft)

            pygame.display.flip()

    # Pantalla de controles
    def menuControles(self):
        self.juegoPausadoControles = not self.juegoPausadoControles
        if self.juegoPausadoControles:
            self.capturarPantalla = self.mostrarSuperficieNivel.copy()
            pygame.mixer.music.pause()
            self.jugador.sonido_pasos.stop()
        else:
            pygame.mixer.music.unpause()

    def pantallaControles(self):
        configuracionWidthPantalla = self.mostrarSuperficieNivel.get_width()
        configuracionHeightPantalla = self.mostrarSuperficieNivel.get_height()
        config_screen = pygame.Surface((configuracionWidthPantalla, configuracionHeightPantalla), pygame.SRCALPHA)

        # Imagen de los controles
        fondoSuperior = pygame.image.load(join("assets", "img", "TITULOS_FONDOS", self.datosLanguage[self.configLanguage]['levelsBeginner']['level1']['controls'])).convert_alpha()
        fondoSuperior = pygame.transform.scale(fondoSuperior, (800, 450))
        fondoSuperiorRect = fondoSuperior.get_rect(center=(configuracionWidthPantalla // 2, configuracionHeightPantalla // 2 - 40))
        config_screen.blit(fondoSuperior, fondoSuperiorRect.topleft)

        # Cargar y escalar los botones
        botonContinuarMenu = pygame.image.load(join("assets", "img", "BOTONES", "botones_bn", "b_continuar.png")).convert_alpha()
        botonContinuarMenu = pygame.transform.scale(botonContinuarMenu, (botonContinuarMenu.get_width() + 5, botonContinuarMenu.get_height() + 5))


        # Calcular las posiciones de los botones para que estén alineados horizontalmente
        espacio_entre_botones = 20
        total_ancho_botones = botonContinuarMenu.get_width() + 2 * espacio_entre_botones
        inicio_x = (configuracionWidthPantalla - total_ancho_botones) // 2
        centro_y = configuracionHeightPantalla - 80

        # Posicionar y dibujar los botones
        botonContinuarMenuRect = botonContinuarMenu.get_rect(topleft=(inicio_x, centro_y))
        config_screen.blit(botonContinuarMenu, botonContinuarMenuRect.topleft)

        banderaEjecutandoNivel1 = True
        while banderaEjecutandoNivel1:
            if self.volver_menu:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.juegoPausadoControles = False
                    banderaEjecutandoNivel1 = False
                    pygame.mixer.music.unpause()
                elif event.type == pygame.MOUSEMOTION:
                    posicionMouse = event.pos
                    if (botonContinuarMenuRect.collidepoint(posicionMouse)):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    posicionMouse = event.pos
                    if botonContinuarMenuRect.collidepoint(posicionMouse):
                        self.sonidoDeClick.play() # Cuando hace un click dentro de las opciones del menú
                        self.juegoPausadoControles = False
                        banderaEjecutandoNivel1 = False
                        pygame.mixer.music.unpause()

            if self.capturarPantalla:
                self.mostrarSuperficieNivel.blit(self.capturarPantalla, (0, 0))

            fondoOscuro = pygame.Surface(self.mostrarSuperficieNivel.get_size(), pygame.SRCALPHA)
            fondoOscuro.fill((0, 0, 0, 150))
            self.mostrarSuperficieNivel.blit(fondoOscuro, (0, 0))

            config_screen_rect = config_screen.get_rect(center=(self.mostrarSuperficieNivel.get_width() // 2, self.mostrarSuperficieNivel.get_height() // 2))
            self.mostrarSuperficieNivel.blit(config_screen, config_screen_rect.topleft)

            pygame.display.flip()

    # ! CONFIGURACION INCIALES
    # level1.py
    def reiniciarConfiguraciones(self):
        # Reiniciar todos los estados relevantes
        self.contadorOxigenoReparado = 0
        self.ganoNivel = False
        self.perdioJuego = False
        self.juegoPausado = False
        self.ultimaVezTeletransportado = 0  # Maneja el tiempo de espera de los teletransportadores
        self.jugador.rect.topleft = (830,700)  # Reiniciar la posición del jugador
        self.camera_offset = pygame.Vector2(0, 0)  # Reiniciar la cámara
        self.tiempo_inicio = pygame.time.get_ticks()  # Reiniciar el tiempo de inicio
        self.tiempo_ultimo = pygame.time.get_ticks()  # Reiniciar el tiempo de inicio
        self.filtros_arreglados = []
        # imagenes del piso

        self.jugador.rect.topleft = (830,700)  # Reiniciar la posición del jugador
        self.todos_los_sprites.add(self.jugador)  # Asegurarse de que el jugador esté en el grupo de todos los sprites

        self.jugador_oculto_hasta = 0
        self.teletransportando = False
    #  ! SAHID explicar dibujar filtros
    def dibujar_filtros(self):
        # Posiciones para las imágenes de los filtros
        pos_x = -20
        pos_y = -60

         # Dependiendo de la cantidad de oxigenos, diibujamos diferentes imagenes, exactmeente las iamgenes de blanco y negro y color
        if self.contadorOxigenoReparado == 0:
            # Se dibujan los filtros en blanco y negro
            self.mostrarSuperficieNivel.blit(self.filtro_bn, (pos_x, pos_y))
            self.mostrarSuperficieNivel.blit(self.filtro_bn, (pos_x + 60, pos_y))

        elif self.contadorOxigenoReparado == 1:
            # Se dibuja un filtro a color y un filtro a blanco y negro
            self.mostrarSuperficieNivel.blit(self.filtro_color, (pos_x, pos_y))
            self.mostrarSuperficieNivel.blit(self.filtro_bn, (pos_x + 60, pos_y))

        # Se dibujan los dos filtros a color
        elif self.contadorOxigenoReparado >= 2:
            self.mostrarSuperficieNivel.blit(self.filtro_color, (pos_x, pos_y))
            self.mostrarSuperficieNivel.blit(self.filtro_color, (pos_x + 60, pos_y))

    def pantallaLaberinto(self):
        self.tmx_filtroUnoNivel2 = load_pygame(join("assets", "maps", "filtros", "filtrosNivel2", "laberinto1.tmx"))
        self.arreglo = False

        map_width = self.tmx_filtroUnoNivel2.width * self.tmx_filtroUnoNivel2.tilewidth
        map_height = self.tmx_filtroUnoNivel2.height * self.tmx_filtroUnoNivel2.tileheight
        offset_x = (self.mostrarSuperficieNivel.get_width() - map_width) // 2
        offset_y = (self.mostrarSuperficieNivel.get_height() - map_height) // 2

        banderaEjecutandoNivel2 = True
        tarea_completada = False

        # Crear el reloj para controlar la velocidad de actualización
        clock = pygame.time.Clock()

        # Inicializar la posición del personaje
        personaje_pos = None

        # Encontrar la posición inicial del personaje
        for layer in self.tmx_filtroUnoNivel2.visible_layers:
            if layer.name == 'capaInicio':
                for x, y, gid in layer:
                    tile = self.tmx_filtroUnoNivel2.get_tile_image_by_gid(gid)
                    if tile:
                        personaje_pos = pygame.Rect(x * self.tmx_filtroUnoNivel2.tilewidth + offset_x, y * self.tmx_filtroUnoNivel2.tileheight + offset_y, self.tmx_filtroUnoNivel2.tilewidth, self.tmx_filtroUnoNivel2.tileheight)
                        break

        # Verificar que se haya encontrado la posición inicial del personaje
        if personaje_pos is None:
            raise ValueError("No se encontró la posición inicial del personaje en la capa 'capaInicio'")

        while banderaEjecutandoNivel2:
            if self.volver_menu:
                break

            mouse_pos = pygame.mouse.get_pos()
            hand_cursor = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    banderaEjecutandoNivel2 = False

                elif event.type == pygame.KEYDOWN:
                    nueva_pos = personaje_pos
                    if event.key == pygame.K_UP:
                        nueva_pos = personaje_pos.move(0, -self.tmx_filtroUnoNivel2.tileheight)
                    elif event.key == pygame.K_DOWN:
                        nueva_pos = personaje_pos.move(0, self.tmx_filtroUnoNivel2.tileheight)
                    elif event.key == pygame.K_LEFT:
                        nueva_pos = personaje_pos.move(-self.tmx_filtroUnoNivel2.tilewidth, 0)
                    elif event.key == pygame.K_RIGHT:
                        nueva_pos = personaje_pos.move(self.tmx_filtroUnoNivel2.tilewidth, 0)

                    # Verificar colisiones con la capa "base"
                    colision = False
                    for layer in self.tmx_filtroUnoNivel2.visible_layers:
                        if layer.name == 'Base':
                            for x, y, gid in layer:
                                tile = self.tmx_filtroUnoNivel2.get_tile_image_by_gid(gid)
                                if tile:
                                    tile_rect = pygame.Rect(x * self.tmx_filtroUnoNivel2.tilewidth + offset_x, y * self.tmx_filtroUnoNivel2.tileheight + offset_y, self.tmx_filtroUnoNivel2.tilewidth, self.tmx_filtroUnoNivel2.tileheight)
                                    if nueva_pos.colliderect(tile_rect):
                                        colision = True
                                        break
                            if colision:
                                break

                    if not colision:
                        personaje_pos = nueva_pos

            for layer in self.tmx_filtroUnoNivel2.visible_layers:
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x, y, gid in layer:
                        tile = self.tmx_filtroUnoNivel2.get_tile_image_by_gid(gid)
                        if tile:
                            tile_rect = pygame.Rect(x * self.tmx_filtroUnoNivel2.tilewidth + offset_x, y * self.tmx_filtroUnoNivel2.tileheight + offset_y, self.tmx_filtroUnoNivel2.tilewidth, self.tmx_filtroUnoNivel2.tileheight)
                            if tile_rect.collidepoint(mouse_pos) and layer.name in ['capaInicio', 'capaFin', 'laberinto', 'base']:
                                hand_cursor = True
                            self.mostrarSuperficieNivel.blit(tile, (x * self.tmx_filtroUnoNivel2.tilewidth + offset_x, y * self.tmx_filtroUnoNivel2.tileheight + offset_y))

            if hand_cursor:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            # Dibujar el personaje
            pygame.draw.rect(self.mostrarSuperficieNivel, (255, 0, 0), personaje_pos)

            pygame.display.flip()

            # Verificar si el personaje ha llegado a la capa "capaFin"
            for layer in self.tmx_filtroUnoNivel2.visible_layers:
                if layer.name == 'CapaFin':
                    for x, y, gid in layer:
                        tile = self.tmx_filtroUnoNivel2.get_tile_image_by_gid(gid)
                        if tile:
                            tile_rect = pygame.Rect(x * self.tmx_filtroUnoNivel2.tilewidth + offset_x, y * self.tmx_filtroUnoNivel2.tileheight + offset_y, self.tmx_filtroUnoNivel2.tilewidth, self.tmx_filtroUnoNivel2.tileheight)
                            if personaje_pos.colliderect(tile_rect):
                                self.arreglo = True
                                self.contadorOxigenoReparado += 1
                                tarea_completada = True
                                banderaEjecutandoNivel2 = False
                                return 1

            clock.tick(FPS)

    def pantallaPerdioNivel(self):
        pygame.mixer.music.stop()  # Detener la música de fondo
        pygame.mixer.Sound(join("assets", "audio", "niveles", "defeat.mp3")).play()
        pygame.mixer.music.set_volume(0.5 if self.volumen == "on" else 0)

        # Crear una superficie semi-transparente
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Negro con 50% de opacidad
        self.screen.blit(overlay, (0, 0))

        # Mostrar mensaje de que el jugador perdió
        # Agregar texto de que perdió nivel
        imagePerdio = pygame.image.load(join(*self.datosLanguage[self.configLanguage]['levelsBeginner']['level1']['imgGameOver'])).convert_alpha()
        imagePerdio = pygame.transform.scale(imagePerdio, (imagePerdio.get_width(), imagePerdio.get_height()))
        self.screen.blit(imagePerdio, (0, (self.mostrarSuperficieNivel.get_height() // 2) - 100))

        # Agregar boton para reiniciar nivel 
        botonReiniciarNivel = pygame.image.load(join("assets", "img", "BOTONES","botones_bn", "b_reiniciar.png")).convert_alpha()
        botonReiniciarNivel = pygame.transform.scale(botonReiniciarNivel, (botonReiniciarNivel.get_width() + 20, botonReiniciarNivel.get_height() + 20))
        botonReiniciarNivelRect = botonReiniciarNivel.get_rect(center=((self.mostrarSuperficieNivel.get_width() // 2) - 100, (self.mostrarSuperficieNivel.get_height() // 2) + 50))
        self.screen.blit(botonReiniciarNivel, botonReiniciarNivelRect.topleft)

        # Agregar boton para volver a seleccionar nivel
        botonSeleccionarNivel = pygame.image.load(join("assets", "img", "BOTONES","botones_bn", "b_seleccionar.png")).convert_alpha()
        botonSeleccionarNivel = pygame.transform.scale(botonSeleccionarNivel, (botonSeleccionarNivel.get_width() + 20, botonSeleccionarNivel.get_height() + 20))
        botonSeleccionarNivelRect = botonSeleccionarNivel.get_rect(center=((self.mostrarSuperficieNivel.get_width() // 2) + 100, (self.mostrarSuperficieNivel.get_height() // 2) + 50))
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
                        self.setup(self.tmx_mapa_2, tiempo_inicio)  # Volvemos a cargar el mapa

                    elif botonSeleccionarNivelRect.collidepoint(posicionMouse):  # Sí hace click en volver al menú
                        self.volver_menu = True
                        banderaEjecutandoNivel1 = False
                        self.perdioJuego = False

                        # * Música de fondo 
                        pygame.mixer.music.pause()  # Pausar la música actual
                        pygame.mixer.music.load(join("assets", "audio", "music", "let_us_adore_you.mp3"))  # Cargar la música del menú
                        pygame.mixer.music.play(-1)  # Reproducir la música en bucle
                        pygame.mixer.music.set_volume(0.2 if self.volumen == "on" else 0)

    def pantallaGanoNivel(self):
        pygame.mixer.music.stop()  # Detener la música de fondo
        pygame.mixer.Sound(join("assets", "audio", "niveles", "win.mp3")).play()
        # volumen del sonido
        pygame.mixer.music.set_volume(0.5 if self.volumen == "on" else 0)

        # Crear una superficie semi-transparente
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA) # ponemo s el fondo oscuro 
        overlay.fill((0, 0, 0, 128))  # Negro con 50% de opacidad
        self.screen.blit(overlay, (0, 0))

        # Mostrar mensaje de que el jugador perdió
        # Agregar texto de que perdió nivel

        # Imagen de cuando pierde
        imagePerdio = pygame.image.load(join(*self.datosLanguage[self.configLanguage]['levelsBeginner']['level1']['imgMissionCompleted'])).convert_alpha()
        imagePerdio = pygame.transform.scale(imagePerdio, (imagePerdio.get_width(), imagePerdio.get_height()))
        self.screen.blit(imagePerdio, (0, (self.mostrarSuperficieNivel.get_height() // 2) - 100))

        # Agregar boton para volver a seleccionar nivel
        botonSeleccionarNivel = pygame.image.load(join("assets", "img", "BOTONES","botones_bn", "b_seleccionar.png")).convert_alpha()
        botonSeleccionarNivel = pygame.transform.scale(botonSeleccionarNivel, (botonSeleccionarNivel.get_width() + 20, botonSeleccionarNivel.get_height() + 20))
        botonSeleccionarNivelRect = botonSeleccionarNivel.get_rect(center=((self.mostrarSuperficieNivel.get_width() // 2), (self.mostrarSuperficieNivel.get_height() // 2) + 50))
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
                    if botonSeleccionarNivelRect.collidepoint(posicionMouse):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                # Sí le da click a los botones
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    posicionMouse = event.pos  # Rastreamos la posicion del mouse

                    if botonSeleccionarNivelRect.collidepoint(posicionMouse):  # Sí hace click en volver al menú
                        self.volver_menu = True
                        banderaEjecutandoNivel1 = False
                        self.perdioJuego = False

                        # * Música de fondo 
                        pygame.mixer.music.pause()  # Pausar la música actual
                        pygame.mixer.music.load(join("assets", "audio", "music", "let_us_adore_you.mp3"))  # Cargar la música del menú
                        pygame.mixer.music.play(-1)  # Reproducir la música en bucle
                        pygame.mixer.music.set_volume(0.2 if self.volumen == "on" else 0)