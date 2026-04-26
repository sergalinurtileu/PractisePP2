import pygame
import random
import sys
import time

# --- КОНСТАНТЫ ---
WIDTH = 640
HEIGHT = 480
BLOCK_SIZE = 20

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)    # Обычная еда
GOLD  = (255, 215, 0)  # Редкая/тяжелая еда
GREEN = (0, 255, 0)
GRAY  = (40, 40, 40)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game: Food Weight & Timers")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    snake = [[100, 100], [80, 100], [60, 100]]
    direction = 'RIGHT'
    change_to = direction

    score = 0
    level = 1
    speed = 10

    # --- НОВАЯ ЛОГИКА ЕДЫ ---
    def generate_food():
        """
        Создает еду с разным весом.
        80% шанса — обычная (1 очко), 20% — золотая (3 очка).
        """
        while True:
            x = random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE
            if [x, y] not in snake:
                # Определяем тип еды
                chance = random.random()
                if chance > 0.8:
                    food_type = "heavy"
                    weight = 3
                    color = GOLD
                    lifetime = 5 # Золотая еда исчезает через 5 секунд
                else:
                    food_type = "normal"
                    weight = 1
                    color = RED
                    lifetime = 10 # Обычная еда исчезает через 10 секунд
                
                return {
                    "pos": [x, y],
                    "weight": weight,
                    "color": color,
                    "spawn_time": time.time(),
                    "lifetime": lifetime
                }

    food = generate_food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        direction = change_to

        # Движение головы
        head = list(snake[0])
        if direction == 'UP':    head[1] -= BLOCK_SIZE
        if direction == 'DOWN':  head[1] += BLOCK_SIZE
        if direction == 'LEFT':  head[0] -= BLOCK_SIZE
        if direction == 'RIGHT': head[0] += BLOCK_SIZE

        snake.insert(0, head)

        # --- ПРОВЕРКА ТАЙМЕРА ЕДЫ ---
        # Если текущее время минус время появления больше времени жизни — удаляем еду
        if time.time() - food["spawn_time"] > food["lifetime"]:
            food = generate_food()

        # --- ПРОВЕРКА ПОЕДАНИЯ ЕДЫ ---
        if head[0] == food["pos"][0] and head[1] == food["pos"][1]:
            score += food["weight"] # Добавляем вес еды к счету
            food = generate_food()
            
            # Уровни сложности
            if score // 5 >= level:
                level += 1
                speed += 2
        else:
            snake.pop()

        # Проверка столкновений
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            break

        for block in snake[1:]:
            if head == block:
                pygame.quit()
                sys.exit()

        # --- ОТРИСОВКА ---
        screen.fill(BLACK)
        
        # Сетка
        for x in range(0, WIDTH, BLOCK_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, BLOCK_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))
        
        # Змейка
        for pos in snake:
            pygame.draw.rect(screen, GREEN, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # Еда (используем цвет из словаря)
        pygame.draw.rect(screen, food["color"], (food["pos"][0], food["pos"][1], BLOCK_SIZE, BLOCK_SIZE))

        # Визуальный таймер (полоска над едой)
        time_left = food["lifetime"] - (time.time() - food["spawn_time"])
        timer_width = (time_left / food["lifetime"]) * BLOCK_SIZE
        pygame.draw.rect(screen, WHITE, (food["pos"][0], food["pos"][1] - 5, timer_width, 3))

        # Статистика
        stats = font.render(f"Score: {score}  Level: {level}", True, WHITE)
        screen.blit(stats, (10, 10))

        pygame.display.flip()
        clock.tick(speed)

    print(f"GAME OVER! Score: {score}")
    pygame.quit()

if __name__ == "__main__":
    main()