import pygame
import random
import os
from config import *

# Path to the assets folder
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

def get_random_pos(snake, obstacles, head=None):
    """Generates a random position aligned to the grid, avoiding collisions."""
    while True:
        pos = [random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
               random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
        
        # Ensure item doesn't spawn inside the snake or on an obstacle
        if pos in snake or pos in obstacles:
            continue
        
        # "No-Trap" check: Don't spawn obstacles too close to the snake's head
        if head and abs(pos[0] - head[0]) < BLOCK_SIZE * 3 and abs(pos[1] - head[1]) < BLOCK_SIZE * 3:
            continue
            
        return pos

def spawn_item(snake, obstacles, itype):
    """Spawns either food (normal/poison) or a power-up (speed/shield/slow)."""
    pos = get_random_pos(snake, obstacles)
    if itype == "food":
        # 15% chance to spawn poison food
        kind = "poison" if random.random() < 0.15 else "normal"
        color = RED if kind == "poison" else GREEN
        return {"pos": pos, "type": kind, "color": color}
    elif itype == "powerup":
        # Randomly choose between three power-up types
        kind = random.choice(["speed", "shield", "slow"])
        colors = {"speed": BLUE, "shield": ORANGE, "slow": CYAN}
        return {"pos": pos, "type": kind, "color": colors[kind]}

def run_game(screen, clock, settings, best_score=0):
    # --- Load Sound Assets ---
    sound_enabled = settings.get("sound", True)
    try:
        eat_snd = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "food_G1U6tlb.mp3"))
        pygame.mixer.music.load(os.path.join(ASSETS_DIR, "SNAKEY GAME MUSIC.mp3"))
        if sound_enabled:
            pygame.mixer.music.play(-1) # Loop background music
    except:
        eat_snd = None

    # --- Initial Game State ---
    snake_color = settings.get("snake_color", [0, 255, 0])
    snake = [[200, 200], [180, 200], [160, 200]]
    direction = "RIGHT"
    score = 0
    level = 1
    obstacles = []
    
    food = spawn_item(snake, obstacles, "food")
    powerup = None
    
    speed_base = 10
    current_speed = speed_base
    shield = False
    effect_end_time = 0 # Timer for temporary power-ups (in ms)
    
    font = pygame.font.SysFont("Arial", 20)

    # --- Main Game Loop ---
    while True:
        current_time = pygame.time.get_ticks()

        # 1. Event Handling (Input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.mixer.music.stop()
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN": direction = "UP"
                if event.key == pygame.K_DOWN and direction != "UP": direction = "DOWN"
                if event.key == pygame.K_LEFT and direction != "RIGHT": direction = "LEFT"
                if event.key == pygame.K_RIGHT and direction != "LEFT": direction = "RIGHT"

        # 2. Movement Logic
        head = list(snake[0])
        if direction == "UP": head[1] -= BLOCK_SIZE
        if direction == "DOWN": head[1] += BLOCK_SIZE
        if direction == "LEFT": head[0] -= BLOCK_SIZE
        if direction == "RIGHT": head[0] += BLOCK_SIZE
        snake.insert(0, head) # Add new head position

        # 3. Collision Detection
        dead = False
        # Wall collision
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT: dead = True
        # Self or obstacle collision
        if head in snake[1:] or head in obstacles: dead = True

        if dead:
            if shield: 
                shield = False # Consume shield to survive
                snake.pop() 
            else:
                pygame.mixer.music.stop()
                return {"score": score, "level": level}
        
        # 4. Consumption Logic (Food)
        if head == food["pos"]:
            if sound_enabled and eat_snd: eat_snd.play()
            
            if food["type"] == "poison":
                # Poison shrinks the snake or ends game if too short
                if len(snake) > 2: 
                    snake.pop(); snake.pop()
                else: 
                    pygame.mixer.music.stop()
                    return {"score": score, "level": level}
            else:
                score += 1
                if score % 5 == 0:
                    level += 1
                    speed_base += 2
                    # Add a new permanent obstacle every level up
                    obstacles.append(get_random_pos(snake, obstacles, head))
            
            food = spawn_item(snake, obstacles, "food")
            # 30% chance to spawn a power-up after eating food
            if not powerup and random.random() < 0.3:
                powerup = spawn_item(snake, obstacles, "powerup")
        else:
            # If no food eaten, remove tail to simulate movement
            snake.pop()

        # 5. Power-up Mechanics
        if powerup and head == powerup["pos"]:
            if sound_enabled and eat_snd: eat_snd.play()
            
            if powerup["type"] == "speed":
                current_speed = speed_base + 7
            elif powerup["type"] == "slow":
                current_speed = speed_base - 4
            elif powerup["type"] == "shield":
                shield = True
            
            effect_end_time = current_time + 5000 # Effects last 5 seconds
            powerup = None

        # Reset speed once the power-up timer expires
        if effect_end_time > 0 and current_time > effect_end_time:
            current_speed = speed_base
            effect_end_time = 0

        # 6. Rendering (Drawing)
        screen.fill(DARK)
        
        # Optional Grid
        if settings.get("grid"):
            for x in range(0, WIDTH, BLOCK_SIZE): pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, BLOCK_SIZE): pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

        # Draw Food and Power-ups
        pygame.draw.rect(screen, food["color"], (*food["pos"], BLOCK_SIZE, BLOCK_SIZE))
        if powerup: pygame.draw.rect(screen, powerup["color"], (*powerup["pos"], BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw Obstacles
        for obs in obstacles: pygame.draw.rect(screen, BROWN, (*obs, BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw Snake (Head is WHITE, Body is custom color)
        for i, p in enumerate(snake):
            color = WHITE if i == 0 else snake_color
            pygame.draw.rect(screen, color, (*p, BLOCK_SIZE-1, BLOCK_SIZE-1))

        # 7. UI / HUD
        score_txt = font.render(f"Score: {score}  Lvl: {level}", True, WHITE)
        best_txt = font.render(f"Best: {max(best_score, score)}", True, LGRAY)
        shield_status = "SHIELD ACTIVE" if shield else ""
        shield_txt = font.render(shield_status, True, ORANGE)
        
        screen.blit(score_txt, (10, 10))
        screen.blit(best_txt, (10, 35))
        screen.blit(shield_txt, (WIDTH - 150, 10))

        pygame.display.flip()
        clock.tick(current_speed)