import pygame
import sys
import math

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint: 1-Brush, 2-Rect, 3-Circle, 4-Eraser, 5-Square, 6-Right Tri, 7-Eq Tri, 8-Rhombus")
    clock = pygame.time.Clock()
    
    radius = 15
    current_color = (0, 0, 255) 
    tool = 'brush' 
    
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

    # Создаем холст и заливаем его БЕЛЫМ цветом
    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill((255, 255, 255))

    while True:
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # ВЫБОР ИНСТРУМЕНТОВ
                if event.key == pygame.K_1: tool = 'brush'
                if event.key == pygame.K_2: tool = 'rect'
                if event.key == pygame.K_3: tool = 'circle'
                if event.key == pygame.K_4: tool = 'eraser'
                if event.key == pygame.K_5: tool = 'square'
                if event.key == pygame.K_6: tool = 'right_triangle'
                if event.key == pygame.K_7: tool = 'eq_triangle'
                if event.key == pygame.K_8: tool = 'rhombus'
                
                # Очистка холста теперь тоже в белый
                if event.key == pygame.K_c: canvas.fill((255, 255, 255)) 
                
                # ВЫБОР ЦВЕТА
                if event.key == pygame.K_r: current_color = COLORS['red']
                elif event.key == pygame.K_g: current_color = COLORS['green']
                elif event.key == pygame.K_b: current_color = COLORS['blue']
                elif event.key == pygame.K_y: current_color = COLORS['yellow']
                elif event.key == pygame.K_p: current_color = COLORS['purple']
                elif event.key == pygame.K_w: current_color = COLORS['white']
                
                if event.key == pygame.K_ESCAPE: return

            # Изменение размера кисти колесиком
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: radius = min(200, radius + 2)
                elif event.button == 5: radius = max(2, radius - 2)

        # --- ЛОГИКА РИСОВАНИЯ (срабатывает при зажатой ЛКМ) ---
        if pygame.mouse.get_pressed()[0]:
            x, y = pos
            
            if tool == 'brush':
                pygame.draw.circle(canvas, current_color, pos, radius)
            
            elif tool == 'eraser':
                # Ластик теперь рисует БЕЛЫМ цветом
                pygame.draw.circle(canvas, (255, 255, 255), pos, radius)
            
            elif tool == 'circle':
                pygame.draw.circle(canvas, current_color, pos, radius)
            
            elif tool == 'rect':
                pygame.draw.rect(canvas, current_color, (x - radius, y - radius//2, radius * 2, radius))
            
            elif tool == 'square':
                pygame.draw.rect(canvas, current_color, (x - radius, y - radius, radius * 2, radius * 2))
            
            elif tool == 'right_triangle':
                points = [(x, y - radius), (x, y + radius), (x + radius * 2, y + radius)]
                pygame.draw.polygon(canvas, current_color, points)
            
            elif tool == 'eq_triangle':
                h = radius * math.sqrt(3)
                points = [(x, y - radius), (x - radius, y + h/2), (x + radius, y + h/2)]
                pygame.draw.polygon(canvas, current_color, points)
            
            elif tool == 'rhombus':
                points = [(x, y - radius), (x + radius * 1.5, y), (x, y + radius), (x - radius * 1.5, y)]
                pygame.draw.polygon(canvas, current_color, points)

        # Отрисовка на экран
        screen.fill((200, 200, 200)) # Светло-серый фон окна (вокруг холста)
        screen.blit(canvas, (0, 0))
        
        # Предпросмотр кисти
        cursor_color = (100, 100, 100)
        if tool in ['brush', 'eraser', 'circle']:
            pygame.draw.circle(screen, cursor_color, pos, radius, 1)
        else:
            pygame.draw.rect(screen, cursor_color, (pos[0]-5, pos[1]-5, 10, 10), 1)
        
        # Индикатор цвета
        pygame.draw.rect(screen, (50, 50, 50), (10, 10, 40, 40))
        pygame.draw.rect(screen, current_color, (15, 15, 30, 30))
        
        pygame.display.flip()
        clock.tick(60) # Увеличил FPS до 60 для более плавного рисования

if __name__ == "__main__":
    main()