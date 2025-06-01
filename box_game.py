import pygame
import os
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen setup
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Box Game")

# Clock
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
FLASH_COLOR = (255, 50, 50)

# Load assets
def load_image(name):
    path = os.path.join('image', name)
    return pygame.image.load(path)

# Box class
class Box:
    def __init__(self, x, y, image_path, name):
        self.x = x
        self.y = y
        self.name = name
        self.health = 10
        self.speed_x = random.choice([3, 5, 7])
        self.speed_y = random.choice([3, 5, 7])
        self.image = pygame.image.load(image_path).convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.bounce()

    def bounce(self):
        if self.x <= 0 or self.x + self.width >= width:
            self.speed_x *= -1
            self.speed_y += random.choice([-1, 1])
        if self.y <= 0 or self.y + self.height >= height:
            self.speed_y *= -1
            self.speed_x += random.choice([-1, 1])

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def take_damage(self):
        self.health -= 1
        scale = max(0.4, 1 - 0.05 * (10 - self.health))  # kecilkan jika damage
        new_w = int(self.image.get_width() * scale)
        new_h = int(self.image.get_height() * scale)
        self.image = pygame.transform.scale(self.image, (new_w, new_h))
        self.width = new_w
        self.height = new_h

# Create boxes
box_A = Box(1, 0, 'image/A.png', "A")
box_B = Box(400, 550, 'image/B.png', "B")

# Collision timer
collision_cooldown = 500  # ms
last_collision_time = 0

# Game loop
isRunning = True
flash_timer = 0

while isRunning:
    screen.fill(BLACK if flash_timer <= 0 else FLASH_COLOR)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

    # Move and draw boxes
    box_A.move()
    box_B.move()
    box_A.draw()
    box_B.draw()

    # Collision detection
    if box_A.rect().colliderect(box_B.rect()) and current_time - last_collision_time > collision_cooldown:
        dx = (box_A.x + box_A.width / 2) - (box_B.x + box_B.width / 2)
        dy = (box_A.y + box_A.height / 2) - (box_B.y + box_B.height / 2)

        # Verify collision 
        if abs(dx) > abs(dy):
            box_A.take_damage()
            box_A.speed_x *= -1
            box_B.speed_x *= -1
            box_A.x += box_A.speed_x * 2
        
        # Horizontal collision
        else:
            box_B.take_damage()
            box_A.speed_y *= -1
            box_B.speed_y *= -1
            box_A.y += box_A.speed_y * 2

        last_collision_time = current_time
        flash_timer = 5  # show flash effect for short time

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Box A Health:", box_A.health)
        print("Box B Health:", box_B.health)

    if flash_timer > 0:
        flash_timer -= 1

    # Check game over
    if box_A.health <= 0 or box_B.health <= 0:
        if box_A.health <= 0:
            print("Box A is destroyed!")
        if box_B.health <= 0:
            print("Box B is destroyed!")
        print("Game Over!")
        pygame.time.delay(1000)
        isRunning = False

    pygame.display.update()
    clock.tick(30)

pygame.quit()
exit()
