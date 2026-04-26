import pygame
import os
import sys
from datetime import datetime

# --- CONSTANTS & CONFIGURATION ---
WIDTH, HEIGHT = 1240, 750  # Total window size (Canvas + Sidebar)
CANVAS_WIDTH, CANVAS_HEIGHT = 1000, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

# Colors Mapping (Key: Color Value)
# Note: Red is assigned to 'M' to avoid conflict with 'R' (Rectangle)
COLORS = {
    'M': (255, 0, 0), 'G': (0, 255, 0), 'B': (0, 0, 255),
    'Y': (255, 255, 0), 'P': (255, 0, 255), 'W': (255, 255, 255),
    'K': (0, 0, 0)
}

def flood_fill(surface, x, y, new_color):
    """
    Algorithm to fill a closed area with a specific color.
    Uses iterative approach with a queue to avoid recursion depth issues.
    """
    if x < 0 or x >= CANVAS_WIDTH or y < 0 or y >= CANVAS_HEIGHT: return
    target_color = surface.get_at((x, y))
    if target_color == new_color: return
    
    pixels = [(x, y)]
    while pixels:
        cx, cy = pixels.pop()
        if surface.get_at((cx, cy)) != target_color: continue
        surface.set_at((cx, cy), new_color)
        # Check adjacent pixels (Up, Down, Right, Left)
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < CANVAS_WIDTH and 0 <= ny < CANVAS_HEIGHT:
                pixels.append((nx, ny))

def main():
    # Initialize Pygame and Screen components
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint Pro - TSIS 2")
    clock = pygame.time.Clock()
    font_bold = pygame.font.SysFont("Arial", 20, bold=True)
    font_small = pygame.font.SysFont("Arial", 16)

    # Drawing Canvas (The actual surface where we paint)
    canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    canvas.fill(WHITE)
    
    # Initial State Variables
    current_color = COLORS['B']
    tool = 'pencil'
    thickness = 2
    drawing = False
    start_pos = None
    last_pos = None
    
    # Text Tool Variables
    text_input = ""
    text_pos = None
    typing = False

    # Main Application Loop
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # --- KEYBOARD EVENT HANDLING ---
            if event.type == pygame.KEYDOWN:
                # If currently typing text
                if typing:
                    if event.key == pygame.K_RETURN: # Confirm text
                        surf = font_small.render(text_input, True, current_color)
                        canvas.blit(surf, text_pos)
                        typing = False; text_input = ""
                    elif event.key == pygame.K_BACKSPACE: text_input = text_input[:-1]
                    elif event.key == pygame.K_ESCAPE: typing = False; text_input = ""
                    else: text_input += event.unicode
                    continue

                # Save Screenshot (Ctrl+S or Cmd+S)
                # Automatically creates 'assets' folder inside the script's directory
                if event.key == pygame.K_s and (pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_META)):
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    assets_dir = os.path.join(current_dir, 'assets')
                    if not os.path.exists(assets_dir): os.makedirs(assets_dir)
                    
                    filename = f"paint_{datetime.now().strftime('%H%M%S')}.png"
                    save_path = os.path.join(assets_dir, filename)
                    pygame.image.save(canvas, save_path)
                    print(f"✅ Saved to: {save_path}")
                
                # Tool Selection Keys
                if event.key == pygame.K_p: tool = 'pencil'
                if event.key == pygame.K_l: tool = 'line'
                if event.key == pygame.K_r: tool = 'rect'
                if event.key == pygame.K_c: tool = 'circle'
                if event.key == pygame.K_e: tool = 'eraser'
                if event.key == pygame.K_f: tool = 'fill'
                if event.key == pygame.K_t: tool = 'text'
                if event.key == pygame.K_x: canvas.fill(WHITE) # Clear Canvas

                # Brush Size Selection
                if event.key == pygame.K_1: thickness = 2
                if event.key == pygame.K_2: thickness = 5
                if event.key == pygame.K_3: thickness = 10

                # Color Selection (using keys mapped in COLORS dictionary)
                key_name = pygame.key.name(event.key).upper()
                if key_name in COLORS: current_color = COLORS[key_name]

            # --- MOUSE EVENT HANDLING ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Ensure the click is within the canvas area
                if event.pos[0] < CANVAS_WIDTH and event.pos[1] < CANVAS_HEIGHT:
                    if tool == 'fill': 
                        flood_fill(canvas, *event.pos, current_color)
                    elif tool == 'text': 
                        typing = True; text_pos = event.pos; text_input = ""
                    else:
                        drawing = True
                        start_pos = event.pos
                        last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    end_pos = event.pos
                    # Finalize shape drawing on the actual canvas surface
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
                start_pos = None

            if event.type == pygame.MOUSEMOTION and drawing:
                # Free-hand drawing and erasing happens in real-time on the canvas
                if tool == 'pencil':
                    pygame.draw.line(canvas, current_color, last_pos, event.pos, thickness)
                    last_pos = event.pos
                elif tool == 'eraser':
                    pygame.draw.circle(canvas, WHITE, event.pos, thickness * 5)

        # --- RENDERING ---
        screen.fill(DARK_GRAY)
        screen.blit(canvas, (0, 0))

        # Shape Preview (Drawn on screen surface, not on canvas yet)
        if drawing and tool in ['line', 'rect', 'circle'] and mouse_pos[0] < CANVAS_WIDTH:
            if tool == 'line': pygame.draw.line(screen, current_color, start_pos, mouse_pos, thickness)
            elif tool == 'rect':
                r = pygame.Rect(start_pos, (mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]))
                r.normalize()
                pygame.draw.rect(screen, current_color, r, thickness)
            elif tool == 'circle':
                rad = int(((start_pos[0]-mouse_pos[0])**2 + (start_pos[1]-mouse_pos[1])**2)**0.5)
                if rad > thickness: pygame.draw.circle(screen, current_color, start_pos, rad, thickness)

        # Render Active Text Typing
        if typing:
            txt_surf = font_small.render(text_input + "|", True, current_color)
            screen.blit(txt_surf, text_pos)

        # --- SIDEBAR UI (INSTRUCTIONS) ---
        ui_x = CANVAS_WIDTH + 15
        pygame.draw.line(screen, WHITE, (CANVAS_WIDTH, 0), (CANVAS_WIDTH, HEIGHT), 2)
        
        ui_labels = [
            ("TOOLS:", WHITE),
            ("[P] Pencil", GRAY), ("[L] Line", GRAY),
            ("[R] Rect", GRAY), ("[C] Circle", GRAY),
            ("[E] Eraser", GRAY), ("[F] Fill", GRAY),
            ("[T] Text", GRAY),
            ("", WHITE),
            ("COLORS:", WHITE),
            ("[M] Red", (255, 100, 100)), ("[G] Green", (100, 255, 100)),
            ("[B] Blue", (120, 120, 255)), ("[Y] Yellow", (255, 255, 100)),
            ("[P] Purple", (255, 100, 255)), ("[W] White", WHITE), 
            ("[K] Black", BLACK),
            ("", WHITE),
            ("BRUSH SIZE: [1, 2, 3]", WHITE),
            ("CLEAR: [X]", (255, 50, 50)),
            ("SAVE: Ctrl+S", (100, 255, 100))
        ]

        # Draw sidebar text
        y_offset = 20
        for text, col in ui_labels:
            label_surf = font_small.render(text, True, col)
            screen.blit(label_surf, (ui_x, y_offset))
            y_offset += 24

        # Current Status Display (Color Box and Tool Name)
        pygame.draw.rect(screen, current_color, (ui_x, HEIGHT - 110, 60, 60))
        pygame.draw.rect(screen, WHITE, (ui_x, HEIGHT - 110, 60, 60), 2)
        status_label = font_bold.render(f"TOOL: {tool.upper()}", True, WHITE)
        screen.blit(status_label, (ui_x, HEIGHT - 40))

        pygame.display.flip()
        clock.tick(120) # 120 FPS for smooth drawing

if __name__ == "__main__":
    main()