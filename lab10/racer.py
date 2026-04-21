import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Square Racer")

# Цвета
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FPS = 60
player_speed = 5
enemy_speed = 7
coin_speed = 4

font = pygame.font.SysFont("Verdana", 20)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 70)) 
        self.image.fill((0, 0, 255)) # Синий
        self.rect = self.image.get_rect()
        self.rect.center = (200, 520)
        # МАСКА для точных столкновений
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
        self.image = pygame.Surface((40, 70))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.spawn()
        self.mask = pygame.mask.from_surface(self.image)

    def spawn(self):
        # Появляемся выше экрана, чтобы не врезаться в игрока мгновенно
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100)

    def move(self):
        self.rect.move_ip(0, enemy_speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (15, 15), 15)
        self.rect = self.image.get_rect()
        self.spawn()
        self.mask = pygame.mask.from_surface(self.image)

    def spawn(self):
        self.rect.center = (random.randint(30, SCREEN_WIDTH-30), -50)

    def move(self):
        self.rect.move_ip(0, coin_speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()

# Создаем объекты
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

collected_coins = 0
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)
    
    # Движение
    P1.move()
    E1.move()
    C1.move()

    # Отрисовка
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    # 1. ПРОВЕРКА МОНЕТ (с маской)
    if pygame.sprite.spritecollide(P1, coins, False, pygame.sprite.collide_mask):
        collected_coins += 1
        C1.spawn()

    # 2. ПРОВЕРКА СТОЛКНОВЕНИЯ С ВРАГОМ (с маской)
    # Это решает твою проблему!
    if pygame.sprite.spritecollide(P1, enemies, False, pygame.sprite.collide_mask):
        print(f"Игра окончена! Собрано монет: {collected_coins}")
        pygame.quit()
        sys.exit()

    # Счёт
    score_text = font.render(f"Монеты: {collected_coins}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(FPS)