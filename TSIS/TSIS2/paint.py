from tools import flood_fill
import pygame
import sys
from datetime import datetime

# --- SETTINGS ---
WIDTH, HEIGHT = 1000, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Color Map
COLORS = {
    'R': (255, 0, 0), 'G': (0, 255, 0), 'B': (0, 0, 255),
    'Y': (255, 255, 0), 'P': (255, 0, 255), 'W': (255, 255, 255),
    'K': (0, 0, 0)
}

def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color: return
    pixels = [(x, y)]
    while pixels:
        cx, cy = pixels.pop()
        if surface.get_at((cx, cy)) != target_color: continue
        surface.set_at((cx, cy), new_color)
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                pixels.append((nx, ny))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS 2 Paint - Final")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)

    canvas = pygame.Surface((WIDTH, HEIGHT))
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
                        surf = font.render(text_input, True, current_color)
                        canvas.blit(surf, text_pos)
                        typing = False; text_input = ""
                    elif event.key == pygame.K_BACKSPACE: text_input = text_input[:-1]
                    elif event.key == pygame.K_ESCAPE: typing = False; text_input = ""
                    else: text_input += event.unicode
                    continue

                # Save Canvas
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    fn = f"paint_{datetime.now().strftime('%H%M%S')}.png"
                    pygame.image.save(canvas, fn)
                
                # Tool Selection
                if event.key == pygame.K_p: tool = 'pencil'
                if event.key == pygame.K_l: tool = 'line'
                if event.key == pygame.K_r: tool = 'rect'
                if event.key == pygame.K_c: tool = 'circle'
                if event.key == pygame.K_e: tool = 'eraser'
                if event.key == pygame.K_f: tool = 'fill'
                if event.key == pygame.K_t: tool = 'text'
                if event.key == pygame.K_x: canvas.fill(WHITE) # Clear

                # Thickness
                if event.key == pygame.K_1: thickness = 2
                if event.key == pygame.K_2: thickness = 5
                if event.key == pygame.K_3: thickness = 10

                # Colors
                key = pygame.key.name(event.key).upper()
                if key in COLORS: current_color = COLORS[key]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if tool == 'fill': flood_fill(canvas, *event.pos, current_color)
                elif tool == 'text': typing = True; text_pos = event.pos; text_input = ""
                else:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    end_pos = event.pos
                    if tool == 'line':
                        pygame.draw.line(canvas, current_color, start_pos, end_pos, thickness)
                    elif tool == 'rect':
                        r = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                        r.normalize()
                        pygame.draw.rect(canvas, current_color, r, thickness)
                    elif tool == 'circle':
                        rad = int(((start_pos[0]-end_pos[0])**2 + (start_pos[1]-end_pos[1])**2)**0.5)
                        if rad > 0: pygame.draw.circle(canvas, current_color, start_pos, rad, thickness)
                    drawing = False

            if event.type == pygame.MOUSEMOTION and drawing:
                if tool == 'pencil':
                    pygame.draw.line(canvas, current_color, last_pos, event.pos, thickness)
                    last_pos = event.pos
                elif tool == 'eraser':
                    pygame.draw.circle(canvas, WHITE, event.pos, thickness * 5)

        # Draw to screen
        screen.fill((60, 60, 60))
        screen.blit(canvas, (0, 0))

        # Preview shapes
        if drawing and tool in ['line', 'rect', 'circle']:
            if tool == 'line':
                pygame.draw.line(screen, current_color, start_pos, mouse_pos, thickness)
            elif tool == 'rect':
                r = pygame.Rect(start_pos, (mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]))
                r.normalize()
                pygame.draw.rect(screen, current_color, r, thickness)
            elif tool == 'circle':
                rad = int(((start_pos[0]-mouse_pos[0])**2 + (start_pos[1]-mouse_pos[1])**2)**0.5)
                if rad > thickness: # Safety check
                    pygame.draw.circle(screen, current_color, start_pos, rad, thickness)

        if typing:
            txt = font.render(text_input + "|", True, current_color)
            screen.blit(txt, text_pos)

        # UI
        pygame.draw.rect(screen, (100, 100, 100), (0, HEIGHT-40, WIDTH, 40))
        info = font.render(f"Tool: {tool.upper()} | Color: {current_color} | Size: {thickness} | 'X' to Clear", True, WHITE)
        screen.blit(info, (10, HEIGHT - 30))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()