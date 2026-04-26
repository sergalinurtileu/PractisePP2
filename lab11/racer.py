import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Параметры экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer: Advanced Level")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Глобальные настройки игры
FPS = 60
player_speed = 5
enemy_speed = 7
coin_speed = 4

# Шрифты для текста
font = pygame.font.SysFont("Verdana", 20)
font_small = pygame.font.SysFont("Verdana", 15)

# --- ЗАГРУЗКА ИЗОБРАЖЕНИЙ ---
# Загружаем файлы, которые ты добавил в папку
player_img = pygame.image.load('player.png').convert_alpha()
enemy_img = pygame.image.load('enemy.png').convert_alpha()
coin_img = pygame.image.load('coin.png').convert_alpha()


player_img = pygame.transform.scale(player_img, (60, 70))
enemy_img = pygame.transform.scale(enemy_img, (40, 70))
coin_img = pygame.transform.scale(coin_img, (30, 30))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (200, 520)
        # Маска нужна для проверки столкновений по пикселям, а не по квадратам
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
        # Появление врага в случайном месте по горизонтали выше экрана
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100)

    def move(self):
        global enemy_speed
        self.rect.move_ip(0, enemy_speed) # Движение вниз
        if self.rect.top > SCREEN_HEIGHT: # Если уехал за экран - пересоздаем сверху
            self.spawn()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.weight = 1 # Переменная для веса монеты
        self.spawn()
        self.mask = pygame.mask.from_surface(self.image)

    def spawn(self):
        # ЗАДАНИЕ: Рандомная генерация веса монеты (1, 2 или 5 очков)
        self.weight = random.choice([1, 2, 5])
        self.rect.center = (random.randint(30, SCREEN_WIDTH-30), -50)

    def move(self):
        self.rect.move_ip(0, coin_speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()

# Создание групп спрайтов
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Переменные для счета и сложности
collected_coins = 0
n_coins_threshold = 10 # Порог очков, после которого враг ускоряется
clock = pygame.time.Clock()

# --- ОСНОВНОЙ ИГРОВОЙ ЦИКЛ ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE) # Белый фон дороги
    
    # Обновление позиций
    P1.move()
    E1.move()
    C1.move()

    # Отрисовка всех объектов
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    # 1. ЗАДАНИЕ: Сбор монет и логика веса
    if pygame.sprite.spritecollide(P1, coins, False, pygame.sprite.collide_mask):
        collected_coins += C1.weight # Прибавляем вес монеты к общему счету
        
        # ЗАДАНИЕ: Увеличение скорости врага при наборе N очков
        if collected_coins >= n_coins_threshold:
            enemy_speed += 1         # Ускоряем врага
            n_coins_threshold += 10  # Увеличиваем следующий порог
        
        C1.spawn() # Создаем новую монетку сверху

    # 2. Столкновение с врагом (Конец игры)
    if pygame.sprite.spritecollide(P1, enemies, False, pygame.sprite.collide_mask):
        print(f"GAME OVER! Total Coins: {collected_coins}")
        pygame.quit()
        sys.exit()

    # Отображение счета
    score_display = font.render(f"Score: {collected_coins}", True, BLACK)
    speed_display = font_small.render(f"Enemy Speed: {enemy_speed}", True, (100, 100, 100))
    
    screen.blit(score_display, (10, 10))
    screen.blit(speed_display, (10, 35))

    pygame.display.update()
    clock.tick(FPS)