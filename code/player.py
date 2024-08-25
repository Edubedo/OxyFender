from setting import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups) # Call the __init__ method of the parent class
        self.image = pygame.Surface((48, 56))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)

        # movement of the player
        self.direction = vector() # Create a vector
        self.speed = 200 # Set the speed of the player

    def input(self):
        keys = pygame.key.get_pressed() # Get the keys pressed
        input_vector = vector(0,0)
        if keys[pygame.K_RIGHT]: # If the key right is pressed
            input_vector.x += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        self.direction = input_vector.normalize() if input_vector else input_vector # Normalize the vector

    def move(self, dt):
        self.rect.topleft += self.direction * self.speed * dt # Move the player

    def update(self, dt):
        self.input()
        self.move(dt)