import pygame

class Ball:
    RADIUS     = 30          
    STEP       = 25          
    COLOR      = (0, 191, 255)    
    GLOW_COLOR = (0, 100, 255)

    def __init__(self, screen_width, screen_height):
        self.screen_width  = screen_width
        self.screen_height = screen_height
        self.x = screen_width  // 2
        self.y = screen_height // 2

    def move(self, direction):
        new_x, new_y = self.x, self.y
        if direction == "up":    new_y -= self.STEP
        if direction == "down":  new_y += self.STEP
        if direction == "left":  new_x -= self.STEP
        if direction == "right": new_x += self.STEP

        if self._in_bounds(new_x, new_y):
            self.x, self.y = new_x, new_y

    def _in_bounds(self, x, y):
        r = self.RADIUS
        return (r <= x <= self.screen_width - r and
                r <= y <= self.screen_height - r)

    def draw(self, screen):
        # Эффект свечения
        for i in range(3, 0, -1):
            s = pygame.Surface((self.RADIUS*2, self.RADIUS*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.GLOW_COLOR, 70 // i), (self.RADIUS, self.RADIUS), self.RADIUS + i*3)
            screen.blit(s, (self.x - self.RADIUS, self.y - self.RADIUS))
        
        pygame.draw.circle(screen, self.COLOR, (self.x, self.y), self.RADIUS)
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.RADIUS - 5, 2)

    def get_position(self):
        return (self.x, self.y)