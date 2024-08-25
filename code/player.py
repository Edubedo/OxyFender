from setting import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups) # Call the __init__ method of the parent class
        self.image = pygame.Surface((48, 56))
        self.image.fill('red')
        
        #rects
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()
        # movement of the player
        self.direction = vector() # Create a vector
        self.speed = 200 # Set the speed of the player
        self.gravity = 1300 # Set the gravity of the player

        #collision
        self.collision_sprites = collision_sprites
        print(self.collision_sprites)

    def input(self):
        keys = pygame.key.get_pressed() # Get the keys pressed
        input_vector = vector(0,0)
        if keys[pygame.K_RIGHT]: # If the key right is pressed
            input_vector.x += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x # Normalize the vector

    def move(self, dt):
        # horizontal
        self.rect.x += self.direction.x * self.speed * dt # Move the player
        self.collision('horizontal')

        # vertical
        self.direction.y += self.gravity / 2 * dt
        self.rect.y += self.direction.y * dt# Move the player
        self.direction.y += self.gravity / 2 * dt
        self.collision('vertical')

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    #left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    #right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                else: #Vertical
                    #top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y = 0
                    #bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y = 0
                    

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)