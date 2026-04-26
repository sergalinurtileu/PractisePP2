import pygame
import os
import sys
from datetime import datetime

# --- КОНСТАНТЫ ---
WIDTH, HEIGHT = 1240, 750  # Немного расширили для удобства меню
CANVAS_WIDTH, CANVAS_HEIGHT = 1000, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

# Цвета (M - красный, чтобы не конфликтовать с R-Rect)
COLORS = {
    'M': (255, 0, 0), 'G': (0, 255, 0), 'B': (0, 0, 255),
    'Y': (255, 255, 0), 'P': (255, 0, 255), 'W': (255, 255, 255),
    'K': (0, 0, 0)
}

def flood_fill(surface, x, y, new_color):
    if x < 0 or x >= CANVAS_WIDTH or y < 0 or y >= CANVAS_HEIGHT: return
    target_color = surface.get_at((x, y))
    if target_color == new_color: return
    pixels = [(x, y)]
    while pixels:
        cx, cy = pixels.pop()
        if surface.get_at((cx, cy)) != target_color: continue
        surface.set_at((cx, cy), new_color)
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < CANVAS_WIDTH and 0 <= ny < CANVAS_HEIGHT:
                pixels.append((nx, ny))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint Pro - TSIS 2")
    clock = pygame.time.Clock()
    font_bold = pygame.font.SysFont("Arial", 20, bold=True)
    font_small = pygame.font.SysFont("Arial", 16)

    canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    canvas.fill(WHITE)
    
    current_color = COLORS['B']
    tool = 'pencil'
    thickness = 2
    drawing = False
    start_pos = None
    last_pos = None
    
    text_input = ""
    text_pos = None
    typing = False

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if typing:
                    if event.key == pygame.K_RETURN:
                        surf = font_small.render(text_input, True, current_color)
                        canvas.blit(surf, text_pos)
                        typing = False; text_input = ""
                    elif event.key == pygame.K_BACKSPACE: text_input = text_input[:-1]
                    elif event.key == pygame.K_ESCAPE: typing = False; text_input = ""
                    else: text_input += event.unicode
                    continue

                # --- КОРРЕКТНОЕ СОХРАНЕНИЕ В ASSETS ---
                if event.key == pygame.K_s and (pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_META)):
                    # Находим папку, где лежит сам paint.py
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    assets_dir = os.path.join(current_dir, 'assets')
                    
                    if not os.path.exists(assets_dir):
                        os.makedirs(assets_dir)
                    
                    timestamp = datetime.now().strftime('%H%M%S')
                    filename = f"paint_{timestamp}.png"
                    save_path = os.path.join(assets_dir, filename)
                    
                    pygame.image.save(canvas, save_path)
                    print(f"✅ Сохранено в папку проекта: {save_path}")
                
                # Переключение инструментов
                if event.key == pygame.K_p: tool = 'pencil'
                if event.key == pygame.K_l: tool = 'line'
                if event.key == pygame.K_r: tool = 'rect'
                if event.key == pygame.K_c: tool = 'circle'
                if event.key == pygame.K_e: tool = 'eraser'
                if event.key == pygame.K_f: tool = 'fill'
                if event.key == pygame.K_t: tool = 'text'
                if event.key == pygame.K_x: canvas.fill(WHITE)

                # Толщина
                if event.key == pygame.K_1: thickness = 2
                if event.key == pygame.K_2: thickness = 5
                if event.key == pygame.K_3: thickness = 10

                # Цвета
                key = pygame.key.name(event.key).upper()
                if key in COLORS: current_color = COLORS[key]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] < CANVAS_WIDTH and event.pos[1] < CANVAS_HEIGHT:
                    if tool == 'fill': flood_fill(canvas, *event.pos, current_color)
                    elif tool == 'text': typing = True; text_pos = event.pos; text_input = ""
                    else:
                        drawing = True
                        start_pos = event.pos
                        last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    end_pos = event.pos
                    if tool == 'line': pygame.draw.line(canvas, current_color, start_pos, end_pos, thickness)
                    elif tool == 'rect':
                        r = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                        r.normalize()
                        pygame.draw.rect(canvas, current_color, r, thickness)
                    elif tool == 'circle':
                        rad = int(((start_pos[0]-end_pos[0])**2 + (start_pos[1]-end_pos[1])**2)**0.5)
                        if rad > 0: pygame.draw.circle(canvas, current_color, start_pos, rad, thickness)
                drawing = False
                start_pos = None

            if event.type == pygame.MOUSEMOTION and drawing:
                if tool == 'pencil':
                    pygame.draw.line(canvas, current_color, last_pos, event.pos, thickness)
                    last_pos = event.pos
                elif tool == 'eraser':
                    pygame.draw.circle(canvas, WHITE, event.pos, thickness * 5)

        # --- ОТРИСОВКА ---
        screen.fill(DARK_GRAY)
        screen.blit(canvas, (0, 0))

        # Превью (только если мы на холсте)
        if drawing and tool in ['line', 'rect', 'circle'] and mouse_pos[0] < CANVAS_WIDTH:
            if tool == 'line': pygame.draw.line(screen, current_color, start_pos, mouse_pos, thickness)
            elif tool == 'rect':
                r = pygame.Rect(start_pos, (mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]))
                r.normalize()
                pygame.draw.rect(screen, current_color, r, thickness)
            elif tool == 'circle':
                rad = int(((start_pos[0]-mouse_pos[0])**2 + (start_pos[1]-mouse_pos[1])**2)**0.5)
                if rad > thickness: pygame.draw.circle(screen, current_color, start_pos, rad, thickness)

        if typing:
            txt = font_small.render(text_input + "|", True, current_color)
            screen.blit(txt, text_pos)

        # --- ПРАВОЕ МЕНЮ (ИНСТРУКЦИЯ) ---
        menu_x = CANVAS_WIDTH + 15
        pygame.draw.line(screen, WHITE, (CANVAS_WIDTH, 0), (CANVAS_WIDTH, HEIGHT), 2)
        
        labels = [
            ("ИНСТРУМЕНТЫ:", WHITE),
            ("[P] - Pencil", GRAY), ("[L] - Line", GRAY),
            ("[R] - Rect", GRAY), ("[C] - Circle", GRAY),
            ("[E] - Eraser", GRAY), ("[F] - Fill", GRAY),
            ("[T] - Text", GRAY),
            ("", WHITE),
            ("ЦВЕТА:", WHITE),
            ("[M] Red", (255, 100, 100)), ("[G] Green", (100, 255, 100)),
            ("[B] Blue", (120, 120, 255)), ("[Y] Yellow", (255, 255, 100)),
            ("[P] Purple", (255, 100, 255)), ("[W] White", WHITE), 
            ("[K] Black", BLACK),
            ("", WHITE),
            ("РАЗМЕР: [1, 2, 3]", WHITE),
            ("ОЧИСТИТЬ: [X]", (255, 50, 50)),
            ("SAVE: Ctrl+S", (100, 255, 100))
        ]

        curr_y = 20
        for text, color in labels:
            txt_surf = font_small.render(text, True, color)
            screen.blit(txt_surf, (menu_x, curr_y))
            curr_y += 24

        # Индикатор внизу меню
        pygame.draw.rect(screen, current_color, (menu_x, HEIGHT - 110, 60, 60))
        pygame.draw.rect(screen, WHITE, (menu_x, HEIGHT - 110, 60, 60), 2)
        status_txt = font_bold.render(f"TOOL: {tool.upper()}", True, WHITE)
        screen.blit(status_txt, (menu_x, HEIGHT - 40))

        pygame.display.flip()
        clock.tick(120)

if __name__ == "__main__":
    main()