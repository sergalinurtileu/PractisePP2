import pygame
import sys
import math

def main():
    # Initialize Pygame modules
    pygame.init()
    
    # Window dimensions
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Paint: 1-Brush, 2-Rect, 3-Circle, 4-Eraser, 5-Square, 6-Right Tri, 7-Eq Tri, 8-Rhombus")
    clock = pygame.time.Clock()
    
    # Default brush settings
    radius = 15
    current_color = (0, 0, 255) # Default Blue
    tool = 'brush' 
    
    # Color palette dictionary
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

    # Create the drawing surface (canvas) and fill it with WHITE
    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill((255, 255, 255))

    while True:
        # Track current mouse position for drawing and preview
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # --- TOOL SELECTION ---
                if event.key == pygame.K_1: tool = 'brush'
                if event.key == pygame.K_2: tool = 'rect'
                if event.key == pygame.K_3: tool = 'circle'
                if event.key == pygame.K_4: tool = 'eraser'
                if event.key == pygame.K_5: tool = 'square'
                if event.key == pygame.K_6: tool = 'right_triangle'
                if event.key == pygame.K_7: tool = 'eq_triangle'
                if event.key == pygame.K_8: tool = 'rhombus'
                
                # Clear canvas: fills the surface with white again
                if event.key == pygame.K_c: canvas.fill((255, 255, 255)) 
                
                # --- COLOR SELECTION ---
                if event.key == pygame.K_r: current_color = COLORS['red']
                elif event.key == pygame.K_g: current_color = COLORS['green']
                elif event.key == pygame.K_b: current_color = COLORS['blue']
                elif event.key == pygame.K_y: current_color = COLORS['yellow']
                elif event.key == pygame.K_p: current_color = COLORS['purple']
                elif event.key == pygame.K_w: current_color = COLORS['white']
                
                # Exit the loop/application
                if event.key == pygame.K_ESCAPE: return

            # Change brush size using the mouse wheel
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: # Scroll Up
                    radius = min(200, radius + 2)
                elif event.button == 5: # Scroll Down
                    radius = max(2, radius - 2)

        # --- DRAWING LOGIC (Triggers while Left Mouse Button is held) ---
        if pygame.mouse.get_pressed()[0]:
            x, y = pos
            
            if tool == 'brush':
                pygame.draw.circle(canvas, current_color, pos, radius)
            
            elif tool == 'eraser':
                # Eraser paints WHITE to match the background
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

        # --- RENDERING ---
        screen.fill((200, 200, 200)) # Light gray background for the window padding
        screen.blit(canvas, (0, 0))  # Draw the canvas surface onto the screen
        
        # Cursor Preview: shows the brush size or a target square
        cursor_color = (100, 100, 100)
        if tool in ['brush', 'eraser', 'circle']:
            pygame.draw.circle(screen, cursor_color, pos, radius, 1)
        else:
            pygame.draw.rect(screen, cursor_color, (pos[0]-5, pos[1]-5, 10, 10), 1)
        
        # Color Indicator UI: displays the currently selected color in the corner
        pygame.draw.rect(screen, (50, 50, 50), (10, 10, 40, 40)) # Border
        pygame.draw.rect(screen, current_color, (15, 15, 30, 30)) # Current color
        
        # Refresh screen
        pygame.display.flip()
        # Cap at 60 Frames Per Second for smooth drawing
        clock.tick(60) 

if __name__ == "__main__":
    main()