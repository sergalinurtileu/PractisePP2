import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer: Advanced Level")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Global game settings
FPS = 60
player_speed = 5
enemy_speed = 7
coin_speed = 4

# Fonts for UI text
font = pygame.font.SysFont("Verdana", 20)
font_small = pygame.font.SysFont("Verdana", 15)

# --- IMAGE LOADING ---
# Loading image files from the project folder
player_img = pygame.image.load('player.png').convert_alpha()
enemy_img = pygame.image.load('enemy.png').convert_alpha()
coin_img = pygame.image.load('coin.png').convert_alpha()

# Rescaling images to fit game requirements
# Set player width to 60 to prevent the "stretched" look
player_img = pygame.transform.scale(player_img, (60, 70))
enemy_img = pygame.transform.scale(enemy_img, (40, 70))
coin_img = pygame.transform.scale(coin_img, (30, 30))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (200, 520)
        # Masks allow for pixel-perfect collision detection instead of simple rectangles
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-player_speed, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(player_speed, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.spawn()
        self.mask = pygame.mask.from_surface(self.image)

    def spawn(self):
        # Spawns enemy at a random horizontal position above the screen
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100)

    def move(self):
        global enemy_speed
        self.rect.move_ip(0, enemy_speed) # Move downward
        if self.rect.top > SCREEN_HEIGHT: # If it leaves the screen bottom, respawn at top
            self.spawn()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.weight = 1 # Variable to store the coin's point value
        self.spawn()
        self.mask = pygame.mask.from_surface(self.image)

    def spawn(self):
        # TASK: Randomly generate coin weight (1, 2, or 5 points)
        self.weight = random.choice([1, 2, 5])
        self.rect.center = (random.randint(30, SCREEN_WIDTH-30), -50)

    def move(self):
        self.rect.move_ip(0, coin_speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()

# Create sprite objects
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Organize sprites into groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Variables for score and difficulty scaling
collected_coins = 0
n_coins_threshold = 10 # Score threshold to increase enemy speed
clock = pygame.time.Clock()

# --- MAIN GAME LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE) # Fill road background
    
    # Update sprite positions
    P1.move()
    E1.move()
    C1.move()

    # Draw all entities to the screen
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    # 1. TASK: Coin collection and weight logic
    if pygame.sprite.spritecollide(P1, coins, False, pygame.sprite.collide_mask):
        collected_coins += C1.weight # Add the weight of the coin to total score
        
        # TASK: Increase enemy speed when N coins are earned
        if collected_coins >= n_coins_threshold:
            enemy_speed += 1         # Speed up the enemy
            n_coins_threshold += 10  # Set the next threshold for speed increase
        
        C1.spawn() # Respawn coin at the top

    # 2. Collision with Enemy (Game Over)
    if pygame.sprite.spritecollide(P1, enemies, False, pygame.sprite.collide_mask):
        print(f"GAME OVER! Total Coins: {collected_coins}")
        pygame.quit()
        sys.exit()

    # Display score and current speed on screen
    score_display = font.render(f"Score: {collected_coins}", True, BLACK)
    speed_display = font_small.render(f"Enemy Speed: {enemy_speed}", True, (100, 100, 100))
    
    screen.blit(score_display, (10, 10))
    screen.blit(speed_display, (10, 35))

    pygame.display.update()
    clock.tick(FPS)