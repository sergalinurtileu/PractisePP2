import pygame
import sys
from clock import MickeysClock

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 850
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey Clock v2.0 Pro")
    
    center = (WIDTH // 2, HEIGHT // 2 - 40)
    
    # ИСПРАВЛЕНО: только 2 аргумента!
    clock_engine = MickeysClock(screen, center)
    
    timer = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((25, 25, 30)) # Глубокий темный фон
        
        clock_engine.update()
        
        pygame.display.flip()
        timer.tick(30)

if __name__ == "__main__":
    main()