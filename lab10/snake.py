import pygame
import random
import sys

# --- КОНСТАНТЫ (Определяем в самом начале) ---
WIDTH = 640
HEIGHT = 480
BLOCK_SIZE = 20

# Цвета (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY  = (40, 40, 40) # Для сетки

def main():
    # Инициализация Pygame
    pygame.init()
    
    # Создание окна
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game: Level Up")
    
    # Инструменты
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    # Состояние змейки: список сегментов [x, y]
    # Начинаем с трех сегментов
    snake = [[100, 100], [80, 100], [60, 100]]
    direction = 'RIGHT'
    change_to = direction

    # Параметры игры
    score = 0
    level = 1
    speed = 10

    def generate_food():
        """Создает координаты еды, которые не заняты змейкой"""
        while True:
            x = random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE
            if [x, y] not in snake:
                return [x, y]

    food_pos = generate_food()

    # Основной цикл игры
    while True:
        # 1. Обработка ввода (События)
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
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        direction = change_to

        # 2. Логика движения
        head = list(snake[0])
        if direction == 'UP':    head[1] -= BLOCK_SIZE
        if direction == 'DOWN':  head[1] += BLOCK_SIZE
        if direction == 'LEFT':  head[0] -= BLOCK_SIZE
        if direction == 'RIGHT': head[0] += BLOCK_SIZE

        # Добавляем новую голову
        snake.insert(0, head)

        # 3. Проверка еды
        if head[0] == food_pos[0] and head[1] == food_pos[1]:
            score += 1
            food_pos = generate_food()
            # Уровни: каждые 3 порции еды повышают уровень и скорость
            if score % 3 == 0:
                level += 1
                speed += 3
        else:
            # Если не съели еду, удаляем хвост (движение)
            snake.pop()

        # 4. Проверка столкновений (Конец игры)
        # Столкновение со стенами (границами)
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            break # Выход из цикла

        # Столкновение с самим собой
        for block in snake[1:]:
            if head == block:
                break
        else:
            # Это продолжение цикла, если столкновений не было
            
            # 5. ОТРИСОВКА
            screen.fill(BLACK) # Фон
            
            # Рисуем сетку
            for x in range(0, WIDTH, BLOCK_SIZE):
                pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, BLOCK_SIZE):
                pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))
            
            # Рисуем змейку
            for pos in snake:
                pygame.draw.rect(screen, GREEN, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
            
            # Рисуем еду
            pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

            # Отображаем счет и уровень
            stats = font.render(f"Score: {score}  Level: {level}", True, WHITE)
            screen.blit(stats, (10, 10))

            pygame.display.flip() # Обновляем экран
            clock.tick(speed)    # Задержка (FPS)
            continue
        
        # Если произошел break из-за столкновения:
        break

    print(f"GAME OVER! Final Score: {score}")
    pygame.quit()

if __name__ == "__main__":
    main()