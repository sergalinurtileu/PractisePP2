import pygame
import time
import math

class MickeysClock:
    def __init__(self, screen: pygame.Surface, center: tuple):
        self.screen = screen
        self.center = center

        # Палитра
        self.RED    = (200, 0, 0)
        self.WHITE  = (255, 255, 255)
        self.BLACK  = (0, 0, 0)
        self.GREEN  = (0, 255, 100)
        self.BG_DIAL = (240, 240, 240)

        # Шрифты
        self.font_time = pygame.font.SysFont("Courier New", 60, bold=True)
        self.font_numbers = pygame.font.SysFont("Arial", 40, bold=True)

    def _draw_arrow(self, angle: float, length: int, thickness: int, color: tuple):
        """Профессиональная отрисовка стрелки с вектором смещения."""
        head_size = thickness * 2.5
        surf_w, surf_h = length + head_size, head_size * 2
        
        # Создаем временную поверхность для стрелки
        arrow_surf = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
        mid_y = surf_h // 2

        # Рисуем саму стрелку (тело и треугольник)
        pygame.draw.rect(arrow_surf, color, (0, mid_y - thickness // 2, length, thickness))
        pygame.draw.polygon(arrow_surf, color, [
            (length + head_size, mid_y),
            (length, mid_y - head_size),
            (length, mid_y + head_size)
        ])

        # Вращаем
        rotated_surf = pygame.transform.rotate(arrow_surf, angle)
        
        # Вычисляем смещение центра для вращения вокруг "плеча"
        offset = pygame.math.Vector2(surf_w / 2, 0).rotate(-angle)
        rect = rotated_surf.get_rect(center=pygame.math.Vector2(self.center) + offset)
        
        self.screen.blit(rotated_surf, rect)

    def draw_dial(self):
        """Отрисовка циферблата с делениями."""
        pygame.draw.circle(self.screen, self.BG_DIAL, self.center, 220)
        pygame.draw.circle(self.screen, (180, 180, 180), self.center, 220, 3)
        
        for i in range(60):
            angle = math.radians(i * 6 - 90)
            is_hour = i % 5 == 0
            d_start = 195 if is_hour else 208
            
            p1 = (self.center[0] + d_start * math.cos(angle), self.center[1] + d_start * math.sin(angle))
            p2 = (self.center[0] + 215 * math.cos(angle), self.center[1] + 215 * math.sin(angle))
            
            pygame.draw.line(self.screen, self.BLACK if is_hour else (150, 150, 150), p1, p2, 3 if is_hour else 1)

            if is_hour:
                num = str(i // 5 if i != 0 else 12)
                n_angle = math.radians(i * 6 - 90)
                nx = self.center[0] + 165 * math.cos(n_angle)
                ny = self.center[1] + 165 * math.sin(n_angle)
                txt = self.font_numbers.render(num, True, self.BLACK)
                self.screen.blit(txt, txt.get_rect(center=(nx, ny)))

    def update(self):
        """Главный метод отрисовки всего состояния часов."""
        t = time.localtime()
        
        # Углы (смещение +90 т.к. в pygame 0 градусов это 3 часа)
        s_ang = -(t.tm_sec * 6) + 90
        m_ang = -(t.tm_min * 6) + 90
        h_ang = -((t.tm_hour % 12) * 30 + t.tm_min * 0.5) + 90

        self.draw_dial()

        # Стрелки: Часовая, Минутная (Черные), Секундная (Красная)
        self._draw_arrow(h_ang, 100, 12, self.BLACK)
        self._draw_arrow(m_ang, 140, 8, self.BLACK)
        self._draw_arrow(s_ang, 165, 3, self.RED)

        # Центр
        pygame.draw.circle(self.screen, self.BLACK, self.center, 8)

        # Цифровой дисплей
        time_str = time.strftime("%H:%M:%S", t)
        txt = self.font_time.render(time_str, True, self.GREEN)
        self.screen.blit(txt, txt.get_rect(center=(self.center[0], self.center[1] + 290)))