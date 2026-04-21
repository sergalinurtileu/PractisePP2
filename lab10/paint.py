import pygame
import sys

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint: 1-Brush, 2-Rect, 3-Circle, 4-Eraser | Colors: R, G, B, Y, P, W")
    clock = pygame.time.Clock()
    
    radius = 15
    current_color = (0, 0, 255) # Синий по умолчанию
    tool = 'brush' 
    
    # Цвета
    COLORS = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'purple': (255, 0, 255),
        'cyan': (0, 255, 255),
        'white': (255, 255, 255),
        'black': (0, 0, 0)
    }

    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill((0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Инструменты
                if event.key == pygame.K_1: tool = 'brush'
                if event.key == pygame.K_2: tool = 'rect'
                if event.key == pygame.K_3: tool = 'circle'
                if event.key == pygame.K_4: tool = 'eraser'
                if event.key == pygame.K_c: canvas.fill((0, 0, 0)) # Очистить
                
                # ВЫБОР ЦВЕТА (добавлены новые клавиши)
                if event.key == pygame.K_r: current_color = COLORS['red']
                elif event.key == pygame.K_g: current_color = COLORS['green']
                elif event.key == pygame.K_b: current_color = COLORS['blue']
                elif event.key == pygame.K_y: current_color = COLORS['yellow']
                elif event.key == pygame.K_p: current_color = COLORS['purple']
                elif event.key == pygame.K_w: current_color = COLORS['white']
                
                if event.key == pygame.K_ESCAPE: return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # ЛКМ
                    start_pos = event.pos
                    if tool == 'rect':
                        # Рисуем квадрат из центра
                        pygame.draw.rect(canvas, current_color, (start_pos[0]-radius, start_pos[1]-radius, radius*2, radius*2))
                    elif tool == 'circle':
                        pygame.draw.circle(canvas, current_color, start_pos, radius)
                
                # Размер кисти колесиком
                if event.button == 4: radius = min(200, radius + 2)
                elif event.button == 5: radius = max(2, radius - 2)

            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]: # Если зажата ЛКМ
                    position = event.pos
                    if tool == 'brush':
                        pygame.draw.circle(canvas, current_color, position, radius)
                    elif tool == 'eraser':
                        pygame.draw.circle(canvas, (0, 0, 0), position, radius)

        # Отрисовка
        screen.fill((30, 30, 30)) # Темно-серый фон окна
        screen.blit(canvas, (0, 0))
        
        # --- ИНТЕРФЕЙС ---
        # Предпросмотр кисти вокруг курсора
        cursor_color = (150, 150, 150) if tool != 'eraser' else (255, 0, 0)
        pygame.draw.circle(screen, cursor_color, pygame.mouse.get_pos(), radius, 1)
        
        # Индикатор текущего цвета в углу
        pygame.draw.rect(screen, (200, 200, 200), (10, 10, 40, 40)) # Рамка
        pygame.draw.rect(screen, current_color, (15, 15, 30, 30)) # Сам цвет
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()