import pygame
import sys

from player import MusicPlayer 

def main():
    pygame.init()
    
    # Создаем небольшое окно для управления плеером
    WIDTH, HEIGHT = 800, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Music Player")
    
    clock = pygame.time.Clock()

    # Инициализируем плеер (убедитесь, что папка music существует и там есть файлы)
    player = MusicPlayer("music") 

    running = True
    while running:
        screen.fill((40, 44, 52)) # Темно-синий фон

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:     # P - играть
                    player.play()
                elif event.key == pygame.K_s:   # S - стоп
                    player.stop()
                elif event.key == pygame.K_SPACE: # Пробел - пауза
                    player.pause_resume()
                elif event.key == pygame.K_n:   # N - следующий трек
                    player.next_track()
                elif event.key == pygame.K_b:   # B - предыдущий трек
                    player.prev_track()

        # Обновление состояния плеера
        player.update()

        # Отрисовка текста
        font = pygame.font.SysFont("Arial", 20)
        
        # Статус
        status_surf = font.render(f"Status: {player.get_status()}", True, (255, 255, 255))
        screen.blit(status_surf, (50, 80))
        
        # Название трека
        name_surf = font.render(f"Track: {player.get_track_name()}", True, (0, 255, 150))
        screen.blit(name_surf, (50, 120))
        
        # Инструкция
        instr_surf = font.render("P: Play | S: Stop | Space: Pause | N: Next | B: Prev", True, (150, 150, 150))
        screen.blit(instr_surf, (50, 220))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()