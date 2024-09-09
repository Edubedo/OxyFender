# Código desarrollado por (E. Escobedo, G. Solorzano, R. Lavariga, N. Laureano, A. Suarez, S. Barroso) 2024
# Este software no puede ser copiado o redistribuido sin permiso del autor.
import pygame
from utils.settings import *
from os.path import join
from pytmx.util_pygame import load_pygame # Importamos la libreria para cargar el mapa
import sys
from menu.play.beginner.level1.sprites import Sprite
from random import uniform # Importamos la libreria para generar numeros aleatorios

class Level1Beginner:
    def __init__(self,tmx_map, name, dificultadNivel, id):
        # Datos generales el nivel
        self.name = name
        self.dificultadNivel = dificultadNivel
        self.id = id

        self.display_surface = pygame.display.get_surface() # Obtenemos la superficie de la pantalla

        # Groups
        self.all_sprites = pygame.sprite.Group() # Creamos un grupo para todos los sprites(Objetos)
        self.setup(tmx_map) # Llamamos al metodo setup para cargar los objetos del nivel
       
    def setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles(): # Obtenemos un objeto de tiled llamado terrain
            Sprite((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites) # Creamos un objeto de la clase Sprite con las coordenadas y la imagen del objeto
    
    
    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update all sprites
            self.all_sprites.update()

            # Draw everything
            self.display_surface.fill(BLACK)
            self.all_sprites.draw(self.display_surface)

            pygame.display.flip()

            # Cap the frame rate
            clock.tick(60)

        
    
    
    # def setup(self, tmx_map, level_frames, audio_files):
    #     #tiles
    #     for layer in ['BG', 'Terrain', 'FG', 'Platforms']:
    #         for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
    #             groups = [self.all_sprites]
    #             if layer == 'Terrain': groups.append(self.collision_sprites)
    #             if layer == 'Platforms': groups.append(self.semi_collision_sprites)
    #             match layer:
    #                 case 'BG': z = Z_LAYERS['bg tiles']
    #                 case 'FG': z = Z_LAYERS['bg tiles']
    #                 case _: z = Z_LAYERS['main']

    #             Sprite((x * TILE_SIZE,y * TILE_SIZE), surf, groups, z)

    #     # bg details
    #     for obj in tmx_map.get_layer_by_name('BG details'):
    #         if obj.name == 'static':
    #             Sprite((obj.x, obj.y), obj.image, self.all_sprites, z = Z_LAYERS['bg tiles'])
    #         else:
    #             AnimatedSprite((obj.x, obj.y), level_frames[obj.name], self.all_sprites, Z_LAYERS['bg tiles'])
    #             if obj.name == 'candle':
    #                 AnimatedSprite((obj.x, obj.y) + vector(-20,-20), level_frames['candle_light'], self.all_sprites, Z_LAYERS['bg tiles'])
    #     # objects 
    #     for obj in tmx_map.get_layer_by_name('Objects'):
    #         if obj.name == 'player':
    #             self.player = Player(
    #                 pos = (obj.x, obj.y), 
    #                 groups = self.all_sprites, 
    #                 collision_sprites = self.collision_sprites, 
    #                 semi_collision_sprites = self.semi_collision_sprites,
    #                 frames = level_frames['player'], 
    #                 data = self.data, 
    #                 attack_sound = audio_files['attack'],
    #                 jump_sound = audio_files['jump'])
    #         else:
    #             if obj.name in ('barrel', 'crate'):
    #                 Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
    #             else:
    #                 # frames 
    #                 frames = level_frames[obj.name] if not 'palm' in obj.name else level_frames['palms'][obj.name]
    #                 if obj.name == 'floor_spike' and obj.properties['inverted']:
    #                     frames = [pygame.transform.flip(frame, False, True) for frame in frames]

    #                 # groups 
    #                 groups = [self.all_sprites]
    #                 if obj.name in('palm_small', 'palm_large'): groups.append(self.semi_collision_sprites)
    #                 if obj.name in ('saw', 'floor_spike'): groups.append(self.damage_sprites)

    #                 # z index
    #                 z = Z_LAYERS['main'] if not 'bg' in obj.name else Z_LAYERS['bg details']

    #                 # animation speed
    #                 animation_speed = PLAYER_VEL if not 'palm' in obj.name else PLAYER_VEL + uniform(-1,1)
    #                 AnimatedSprite((obj.x, obj.y), frames, groups, z, animation_speed)
    #         if obj.name == 'flag':
    #             self.level_finish_rect = pygame.FRect((obj.x, obj.y), (obj.width, obj.height))

    #             # moving objects 
    #     for obj in tmx_map.get_layer_by_name('Moving Objects'):
    #         if obj.name == 'spike':
    #             Spike(
    #                 pos = (obj.x + obj.width / 2, obj.y + obj.height / 2),
    #                 surf = level_frames['spike'],
    #                 radius = obj.properties['radius'],
    #                 speed = obj.properties['speed'],
    #                 start_angle = obj.properties['start_angle'],
    #                 end_angle = obj.properties['end_angle'],
    #                 groups = (self.all_sprites, self.damage_sprites))
    #             for radius in range(0, obj.properties['radius'], 20):
    #                 Spike(
    #                     pos = (obj.x + obj.width / 2, obj.y + obj.height / 2),
    #                     surf = level_frames['spike_chain'],
    #                     radius = radius,
    #                     speed = obj.properties['speed'],
    #                     start_angle = obj.properties['start_angle'],
    #                     end_angle = obj.properties['end_angle'],
    #                     groups = self.all_sprites,
    #                     z = Z_LAYERS['bg details'])

    #         else:
    #             frames = level_frames[obj.name]
    #             groups = (self.all_sprites, self.semi_collision_sprites) if obj.properties['platform'] else (self.all_sprites, self.damage_sprites)
    #             if obj.width > obj.height: # horizontal
    #                 move_dir = 'x'
    #                 start_pos = (obj.x, obj.y + obj.height / 2)
    #                 end_pos = (obj.x + obj.width,obj.y + obj.height / 2)
    #             else: # vertical 
    #                 move_dir = 'y'
    #                 start_pos = (obj.x + obj.width / 2, obj.y)
    #                 end_pos = (obj.x + obj.width / 2,obj.y + obj.height)
    #             speed = obj.properties['speed']
    #             MovingSprite(frames, groups, start_pos, end_pos, move_dir, speed, obj.properties['flip'])

    #             if obj.name == 'saw':
    #                 if move_dir == 'x':
    #                     y = start_pos[1] - level_frames['saw_chain'].get_height() / 2
    #                     left, right = int(start_pos[0]), int(end_pos[0])
    #                     for x in range(left, right, 20):
    #                         Sprite((x,y), level_frames['saw_chain'], self.all_sprites, Z_LAYERS['bg details'])
    #                 else:
    #                     x = start_pos[0] - level_frames['saw_chain'].get_width() / 2
    #                     top, bottom = int(start_pos[1]), int(end_pos[1])
    #                     for y in range(top, bottom, 20):
    #                         Sprite((x,y), level_frames['saw_chain'], self.all_sprites, Z_LAYERS['bg details'])

    #     # enemies 
    #     for obj in tmx_map.get_layer_by_name('Enemies'):
    #         if obj.name == 'tooth':
    #             Tooth((obj.x, obj.y), level_frames['tooth'], (self.all_sprites, self.damage_sprites, self.tooth_sprites), self.collision_sprites)
    #         if obj.name == 'shell':
    #             Shell(
    #                 pos = (obj.x, obj.y), 
    #                 frames = level_frames['shell'], 
    #                 groups = (self.all_sprites, self.collision_sprites), 
    #                 reverse = obj.properties['reverse'], 
    #                 player = self.player, 
    #                 create_pearl = self.create_pearl)

    #     # items 
    #     for obj in tmx_map.get_layer_by_name('Items'):
    #         Item(obj.name, (obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), level_frames['items'][obj.name], (self.all_sprites, self.item_sprites), self.data)

    #     # water 
    #     for obj in tmx_map.get_layer_by_name('Water'):
    #         rows = int(obj.height / TILE_SIZE) 
    #         cols = int(obj.width / TILE_SIZE) 
    #         for row in range(rows):
    #             for col in range(cols):
    #                 x = obj.x + col * TILE_SIZE
    #                 y = obj.y + row * TILE_SIZE
    #                 if row == 0:
    #                     AnimatedSprite((x,y), level_frames['water_top'], self.all_sprites, Z_LAYERS['water'])
    #                 else:
    #                     Sprite((x,y), level_frames['water_body'], self.all_sprites, Z_LAYERS['water'])
        
    # def create_pearl(self, pos, direction):
    #     Pearl(pos, (self.all_sprites, self.damage_sprites, self.pearl_sprites), self.pearl_surf, direction, 150)
    #     self.pearl_sound.play()

    # def import_assets(self):
    #         self.level_frames = {
    #             'flag': import_folder('assets','media','graphics', 'level', 'flag'),
    #             'saw': import_folder('assets','media','graphics', 'enemies', 'saw', 'animation'),
    #             'floor_spike': import_folder('assets','media','graphics','enemies', 'floor_spikes'),
    #             'palms': import_sub_folders('assets','media','graphics', 'level', 'palms'),
    #             'candle': import_folder('assets','media','graphics','level', 'candle'),
    #             'window': import_folder('assets','media','graphics','level', 'window'),
    #             'big_chain': import_folder('assets','media','graphics','level', 'big_chains'),
    #             'small_chain': import_folder('assets','media','graphics','level', 'small_chains'),
    #             'candle_light': import_folder('assets','media','graphics','level', 'candle light'),
    #             'player': import_sub_folders('assets','media','graphics','player'),
    #             'saw': import_folder('assets','media','graphics', 'enemies', 'saw', 'animation'),
    #             'saw_chain': import_image( 'assets','media','graphics', 'enemies', 'saw', 'saw_chain'),
    #             'helicopter': import_folder('assets','media','graphics', 'level', 'helicopter'),
    #             'boat': import_folder( 'assets','media','graphics', 'objects', 'boat'),
    #             'spike': import_image( 'assets','media','graphics', 'enemies', 'spike_ball', 'Spiked Ball'),
    #             'spike_chain': import_image( 'assets','media','graphics', 'enemies', 'spike_ball', 'spiked_chain'),
    #             'tooth': import_folder('assets','media','graphics','enemies', 'tooth', 'run'),
    #             'shell': import_sub_folders('assets','media','graphics','enemies', 'shell'),
    #             'pearl': import_image( 'assets','media','graphics', 'enemies', 'bullets', 'pearl'),
    #             'items': import_sub_folders('assets','media','graphics', 'items'),
    #             'particle': import_folder('assets','media','graphics', 'effects', 'particle'),
    #             'water_top': import_folder('assets','media','graphics', 'level', 'water', 'top'),
    #             'water_body': import_image('assets','media','graphics', 'level', 'water', 'body'),
    #             'bg_tiles': import_folder_dict('assets','media','graphics', 'level', 'bg', 'tiles'),
    #             'cloud_small': import_folder('assets','media','graphics','level', 'clouds', 'small'),
    #             'cloud_large': import_image('assets','media','graphics','level', 'clouds', 'large_cloud'),
    #         }
    #         self.font = pygame.font.Font(join('assets','media','graphics', 'ui', 'runescape_uf.ttf'), 40)
    #         self.ui_frames = {
    #             'heart': import_folder('assets','media','graphics', 'ui', 'heart'), 
    #             'coin':import_image('assets','media','graphics', 'ui', 'coin')
    #         }
    #         self.overworld_frames = {
    #             'palms': import_folder('assets','media','graphics', 'overworld', 'palm'),
    #             'water': import_folder('assets','media','graphics', 'overworld', 'water'),
    #             'path': import_folder_dict('assets','media','graphics', 'overworld', 'path'),
    #             'icon': import_sub_folders('assets','media','graphics', 'overworld', 'icon'),
    #         }

    #         self.audio_files = {
    #             'coin': pygame.mixer.Sound(join('assets','media','audio', 'coin.wav')),
    #             'attack': pygame.mixer.Sound(join('assets','media','audio', 'attack.wav')),
    #             'jump': pygame.mixer.Sound(join('assets','media','audio', 'jump.wav')), 
    #             'damage': pygame.mixer.Sound(join('assets','media','audio', 'damage.wav')),
    #             'pearl': pygame.mixer.Sound(join('assets','media','audio', 'pearl.wav')),
    #         }
    #         self.bg_music = pygame.mixer.Sound(join('assets','media','audio', 'starlight_city.mp3'))
    #         self.bg_music.set_volume(0.5)

    # def pearl_collision(self):
    #     for sprite in self.collision_sprites:
    #         sprite = pygame.sprite.spritecollide(sprite, self.pearl_sprites, True)
    #         if sprite:
    #             ParticleEffectSprite((sprite[0].rect.center), self.particle_frames, self.all_sprites)

    # def hit_collision(self):
    #     for sprite in self.damage_sprites:
    #         if sprite.rect.colliderect(self.player.hitbox_rect):
    #             self.player.get_damage()
    #             self.damage_sound.play()
    #             if hasattr(sprite, 'pearl'):
    #                 sprite.kill()
    #                 ParticleEffectSprite((sprite.rect.center), self.particle_frames, self.all_sprites)

    # def item_collision(self):
    #     if self.item_sprites:
    #         item_sprites = pygame.sprite.spritecollide(self.player, self.item_sprites, True)
    #         if item_sprites:
    #             item_sprites[0].activate()
    #             ParticleEffectSprite((item_sprites[0].rect.center), self.particle_frames, self.all_sprites)
    #             self.coin_sound.play()

    # def attack_collision(self):
    #     for target in self.pearl_sprites.sprites() + self.tooth_sprites.sprites():
    #         facing_target = self.player.rect.centerx < target.rect.centerx and self.player.facing_right or \
    #                         self.player.rect.centerx > target.rect.centerx and not self.player.facing_right
    #         if target.rect.colliderect(self.player.rect) and self.player.attacking and facing_target:
    #             target.reverse()

    # def check_constraint(self):
        # left right
        # if self.player.hitbox_rect.left <= 0:
        #     self.player.hitbox_rect.left = 0
        # if self.player.hitbox_rect.right >= self.level_width:
        #     self.player.hitbox_rect.right = self.level_width

        # # bottom border 
        # if self.player.hitbox_rect.bottom > self.level_bottom:
        #     self.switch_stage('overworld', -1)

        # # success 
        # if self.player.hitbox_rect.colliderect(self.level_finish_rect):
        #     self.switch_stage('overworld', self.level_unlock)