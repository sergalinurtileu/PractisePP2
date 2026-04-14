import pygame
import time

class MickeysClock:
    def __init__(self, screen, center, hand_image_path):
        self.screen = screen
        self.center = center

        try:
            # Загружаем "руку"
            img = pygame.image.load(hand_image_path).convert_alpha()
            # Делаем её вытянутой (важно, чтобы пальцы смотрели ВВЕРХ на исходнике)
            self.hand_img = pygame.transform.scale(img, (50, 160))
        except:
            # Заглушка, если файла нет
            self.hand_img = pygame.Surface((20, 140), pygame.SRCALPHA)
            self.hand_img.fill((255, 255, 255))

        # Свои шрифты для уникальности
        self.font_time = pygame.font.SysFont("Courier New", 60, bold=True)
        self.font_info = pygame.font.SysFont("Courier New", 18)

    def _blit_rotate_center(self, image, angle):
        """Хитрая функция вращения вокруг основания (плеча) руки"""
        # Вращаем
        rotated_image = pygame.transform.rotate(image, angle)
        # Находим новый центр, чтобы основание оставалось в self.center
        new_rect = rotated_image.get_rect(center=self.center)
        self.screen.blit(rotated_image, new_rect)

    def draw(self):
        now = time.localtime()
        # Углы: 1 секунда = 6 градусов. В pygame вращение идет против часовой,
        # поэтому ставим минус, чтобы шло по часовой.
        sec_angle = -(now.tm_sec * 6)
        min_angle = -(now.tm_min * 6)

        # Рисуем руки с разным размером
        # Минутная (Правая) - чуть шире
        hand_min = pygame.transform.scale(self.hand_img, (60, 170))
        self._blit_rotate_center(hand_min, min_angle)

        # Секундная (Левая) - чуть уже
        hand_sec = pygame.transform.scale(self.hand_img, (40, 140))
        self._blit_rotate_center(hand_sec, sec_angle)

        # Красивая заклепка в центре
        pygame.draw.circle(self.screen, (200, 0, 0), self.center, 12)
        pygame.draw.circle(self.screen, (0, 0, 0), self.center, 12, 2)

        # Цифровое время в другом стиле
        current_time = time.strftime("%H:%M:%S", now)
        time_surf = self.font_time.render(current_time, True, (0, 255, 100))
        time_rect = time_surf.get_rect(center=(self.center[0], self.center[1] + 240))
        self.screen.blit(time_surf, time_rect)