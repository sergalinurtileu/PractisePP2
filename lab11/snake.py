import pygame
import random
import sys
import time

# --- CONSTANTS ---
WIDTH = 640
HEIGHT = 480
BLOCK_SIZE = 20

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)    # Normal food
GOLD  = (255, 215, 0)  # Heavy/Rare food
GREEN = (0, 255, 0)
GRAY  = (40, 40, 40)   # Grid color

def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game: Food Weight & Timers")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    # Initial Snake setup: list of segments [x, y]
    snake = [[100, 100], [80, 100], [60, 100]]
    direction = 'RIGHT'
    change_to = direction

    # Game parameters
    score = 0
    level = 1
    speed = 10

    # --- FOOD GENERATION LOGIC ---
    def generate_food():
        """
        Creates food with different weights.
        80% chance — normal (1 point), 20% — gold (3 points).
        """
        while True:
            x = random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE
            
            # Ensure food doesn't spawn inside the snake
            if [x, y] not in snake:
                chance = random.random()
                if chance > 0.8:
                    # Rare heavy food
                    food_type = "heavy"
                    weight = 3
                    color = GOLD
                    lifetime = 5  # Disappears after 5 seconds
                else:
                    # Standard food
                    food_type = "normal"
                    weight = 1
                    color = RED
                    lifetime = 10 # Disappears after 10 seconds
                
                return {
                    "pos": [x, y],
                    "weight": weight,
                    "color": color,
                    "spawn_time": time.time(),
                    "lifetime": lifetime
                }

    # Initialize first food object
    food = generate_food()

    # --- MAIN GAME LOOP ---
    while True:
        # 1. Event Handling
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

        # 2. Movement logic (Calculating new head position)
        head = list(snake[0])
        if direction == 'UP':    head[1] -= BLOCK_SIZE
        if direction == 'DOWN':  head[1] += BLOCK_SIZE
        if direction == 'LEFT':  head[0] -= BLOCK_SIZE
        if direction == 'RIGHT': head[0] += BLOCK_SIZE

        # Add new head to snake
        snake.insert(0, head)

        # 3. FOOD TIMER CHECK
        # If current time minus spawn time exceeds lifetime, generate new food
        if time.time() - food["spawn_time"] > food["lifetime"]:
            food = generate_food()

        # 4. EATING LOGIC
        if head[0] == food["pos"][0] and head[1] == food["pos"][1]:
            score += food["weight"] # Increase score by food weight
            food = generate_food()
            
            # Difficulty Level: Increase speed every 5 points
            if score // 5 >= level:
                level += 1
                speed += 2
        else:
            # If no food eaten, remove tail to maintain length
            snake.pop()

        # 5. COLLISION DETECTION (Game Over)
        # Wall collisions
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            break

        # Self-collision
        for block in snake[1:]:
            if head == block:
                pygame.quit()
                sys.exit()

        # --- DRAWING ---
        screen.fill(BLACK)
        
        # Draw background grid
        for x in range(0, WIDTH, BLOCK_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, BLOCK_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))
        
        # Draw snake body
        for pos in snake:
            pygame.draw.rect(screen, GREEN, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw food using assigned color
        pygame.draw.rect(screen, food["color"], (food["pos"][0], food["pos"][1], BLOCK_SIZE, BLOCK_SIZE))

        # Visual Timer Bar (White line above the food)
        time_left = food["lifetime"] - (time.time() - food["spawn_time"])
        timer_width = (time_left / food["lifetime"]) * BLOCK_SIZE
        pygame.draw.rect(screen, WHITE, (food["pos"][0], food["pos"][1] - 5, timer_width, 3))

        # Render Score and Level
        stats = font.render(f"Score: {score}  Level: {level}", True, WHITE)
        screen.blit(stats, (10, 10))

        # Update display and control FPS
        pygame.display.flip()
        clock.tick(speed)

    # End Game printout
    print(f"GAME OVER! Final Score: {score}")
    pygame.quit()

if __name__ == "__main__":
    main()