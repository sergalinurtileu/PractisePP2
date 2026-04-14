import pygame
import sys
from ball import Ball

# Настройки цветов
COLOR_BG      = (10, 10, 20)      
COLOR_GRID    = (35, 35, 55)      
COLOR_PANEL   = (25, 25, 45)      
COLOR_TEXT    = (0, 255, 200)     
COLOR_ACCENT  = (255, 0, 255)     

def draw_grid(screen):
    for x in range(0, 800, 50):
        pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, 540), 1)
    for y in range(0, 540, 50):
        pygame.draw.line(screen, COLOR_GRID, (0, y), (800, y), 1)

def draw_ui(screen, ball, font):
    pygame.draw.rect(screen, COLOR_PANEL, (0, 540, 800, 60))
    pygame.draw.line(screen, COLOR_ACCENT, (0, 540), (800, 540), 3)
    x, y = ball.get_position()
    pos_surf = font.render(f"POS: {x}, {y}", True, COLOR_TEXT)
    screen.blit(pos_surf, (20, 560))
    hint_surf = font.render("ARROWS: MOVE | R: RESET | ESC: EXIT", True, (200, 200, 200))
    screen.blit(hint_surf, (350, 560))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Neon Movement")
    clock = pygame.time.Clock()
    
    font = pygame.font.SysFont("Arial", 18, bold=True)
    ball = Ball(800, 600)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_r:
                    ball = Ball(800, 600)
                if event.key == pygame.K_UP:    ball.move("up")
                if event.key == pygame.K_DOWN:  ball.move("down")
                if event.key == pygame.K_LEFT:  ball.move("left")
                if event.key == pygame.K_RIGHT: ball.move("right")

        screen.fill(COLOR_BG)
        draw_grid(screen)
        ball.draw(screen)
        draw_ui(screen, ball, font)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()