import pygame
from entities.player.player import Player
from entities.items.objects import Block, Fire
from utils.functions import get_background
from general.settings import *

class Level1Beginner:
    def __init__(self, name, difficulty, id):
        self.name = name
        self.difficulty = difficulty
        self.id = id

    def handle_vertical_collision(self, player, objects, dy):
        collided_objects = []
        for obj in objects:
            if pygame.sprite.collide_mask(player, obj):
                if dy > 0:
                    player.rect.bottom = obj.rect.top
                    player.landed()
                elif dy < 0:
                    player.rect.top = obj.rect.bottom
                    player.hit_head()

                collided_objects.append(obj)

        return collided_objects

    def collide(self, player, objects, dx):
        player.move(dx, 0)
        player.update()
        collided_object = None
        for obj in objects:
            if pygame.sprite.collide_mask(player, obj):
                collided_object = obj
                break

        player.move(-dx, 0)
        player.update()
        return collided_object

    def handle_move(self, player, objects):
        keys = pygame.key.get_pressed()

        player.x_vel = 0
        collide_left = self.collide(player, objects, -PLAYER_VEL * 2)
        collide_right = self.collide(player, objects, PLAYER_VEL * 2)

        if keys[pygame.K_LEFT] and not collide_left:
            player.move_left(PLAYER_VEL)
        if keys[pygame.K_RIGHT] and not collide_right:
            player.move_right(PLAYER_VEL)

        vertical_collide = self.handle_vertical_collision(player, objects, player.y_vel)
        to_check = [collide_left, collide_right, *vertical_collide]

        for obj in to_check:
            if obj and obj.name == "fire":
                player.make_hit()

    def draw(self, window, background, bg_image, player, objects, offset_x):
        for tile in background:
            window.blit(bg_image, tile)

        for obj in objects:
            obj.draw(window, offset_x)

        player.draw(window, offset_x)

        pygame.display.update()

    def run(self, window):
        clock = pygame.time.Clock()
        background, bg_image = get_background("Blue.png")

        block_size = 96

        player = Player(100, 100, 50, 50)
        fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
        fire.on()
        floor = [Block(i * block_size, HEIGHT - block_size, block_size)
                 for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
        objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size),
                   Block(block_size * 3, HEIGHT - block_size * 4, block_size), fire]

        offset_x = 0
        scroll_area_width = 200

        run = True
        while run:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player.jump_count < 2:
                        player.jump()

            player.loop(FPS)
            fire.loop()
            self.handle_move(player, objects)
            self.draw(window, background, bg_image, player, objects, offset_x)

            if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                    (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
                offset_x += player.x_vel

        pygame.quit()
        quit()

if __name__ == "__main__":
    level = Level1Beginner("Level 1", "Beginner", 1)
    level.main(window)