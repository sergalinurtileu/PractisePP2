import pygame
import sys
import os
import math
from clock import MickeysClock

# --- Настройки стиля ---
SCREEN_WIDTH  = 700
SCREEN_HEIGHT = 800
FPS           = 1 
THEME_COLOR   = (20, 20, 30)
ACCENT_COLOR  = (0, 255, 150)

HAND_PATH = os.path.join("image", "minky.png")

def draw_clock_face_with_numbers(screen, center, font):
    """Рисуем циферблат с цифрами от 1 до 12"""
    radius = 210
    pygame.draw.circle(screen, ACCENT_COLOR, center, radius + 10, 3)
    
    for i in range(1, 13):
        # Угол для каждой цифры
        angle = math.radians(i * 30 - 90)
        
        # Координаты для цифры
        x = center[0] + (radius - 30) * math.cos(angle)
        y = center[1] + (radius - 30) * math.sin(angle)
        
        num_surf = font.render(str(i), True, (255, 255, 255))
        num_rect = num_surf.get_rect(center=(int(x), int(y)))
        screen.blit(num_surf, num_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mickey Time Pro")
    clock_tick = pygame.time.Clock()

    center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    
    # Загружаем шрифты
    number_font = pygame.font.SysFont("Arial", 34, bold=True)
    title_font = pygame.font.SysFont("Impact", 48)

    # Создаем объект часов (убедись, что clock.py в этой же папке)
    mickey = MickeysClock(screen, center, HAND_PATH)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(THEME_COLOR)
        
        # 1. Рисуем цифры (вызываем напрямую, без импорта!)
        draw_clock_face_with_numbers(screen, center, number_font)
        
        # 2. Рисуем заголовок
        title = title_font.render("TIME RUNNER", True, ACCENT_COLOR)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 50)))
        
        # 3. Рисуем стрелки из clock.py
        mickey.draw()

        pygame.display.flip()
        clock_tick.tick(FPS)

if __name__ == "__main__":
    main()