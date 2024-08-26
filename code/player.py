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

        self.jump = False
        self.jump_height = 800

        #collision
        self.collision_sprites = collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}

        self.display_surface = pygame.display.get_surface()

    def input(self):
        keys = pygame.key.get_pressed() # Get the keys pressed
        input_vector = vector(0,0)
        if keys[pygame.K_RIGHT]: # If the key right is pressed
            input_vector.x += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x # Normalize the vector

        if keys[pygame.K_SPACE]:
            self.jump = True

    def move(self, dt):
        # horizontal
        self.rect.x += self.direction.x * self.speed * dt # Move the player
        self.collision('horizontal')

        # vertical
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])):
            self.direction.y = 0
            self.rect.y += self.gravity / 10 * dt
        else:
            self.direction.y += self.gravity / 2 * dt
            self.rect.y += self.direction.y * dt # Move the player
            self.direction.y += self.gravity / 2 * dt

        self.collision('vertical')

        # Check for jump after calculating movement
        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
            elif any((self.on_surface['left'], self.on_surface['right'])):
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface['left'] else -1
            self.jump = False

        
        self.collision('vertical')

    def check_contact(self):
        # Define rectangles for floor, right, and left collisions
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        right_rect = pygame.Rect(self.rect.topright + vector(0, self.rect.height / 4),(2,self.rect.height / 2))
        left_rect = pygame.Rect((self.rect.topleft + vector(-2, self.rect.height / 4)), (2, self.rect.height / 2))
        
        # Get collision rectangles
        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        # Check for collisions and update on_surface dictionary
        self.on_surface['floor'] = floor_rect.collidelist(collide_rects) >= 0
        self.on_surface['right'] = right_rect.collidelist(collide_rects) >= 0
        self.on_surface['left'] = left_rect.collidelist(collide_rects) >= 0 
        print(self.on_surface)
    
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
                    #bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)
        self.check_contact()