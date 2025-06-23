# src/ui/loading_screen.py
import math

from src.engine.settings import *

class LoadingScreen:
    def __init__(self):
        self.angle = 0
        self.font = pg.font.Font(None, 36)
        self.ellipsis_timer = 0
        self.ellipsis_state = 0

    def update(self, dt):
        self.angle = (self.angle + 120 * dt) % 360
        self.ellipsis_timer += dt

        if self.ellipsis_timer >= 0.5:  # update every 0.5 seconds
            self.ellipsis_timer = 0
            self.ellipsis_state = (self.ellipsis_state + 1) % 3

    def render(self, surface):
        surface.fill((20, 20, 30))
        center = (WIDTH // 2, HEIGHT // 2)
        radius = 30

        for i in range(8):
            angle = (self.angle + i * 45) % 360
            alpha = max(50, 255 - i * 30)
            point = pg.math.Vector2(1, 0).rotate(-angle) * radius
            pos = (int(center[0] + point.x), int(center[1] + point.y))
            color = (255, 255, 255, alpha)
            dot_surface = pg.Surface((12, 12), pg.SRCALPHA)
            pg.draw.circle(dot_surface, color, (6, 6), 6)
            surface.blit(dot_surface, (pos[0] - 6, pos[1] - 6))

        # Animated dots in text
        dots = "." * (self.ellipsis_state + 1)
        text = self.font.render(f"Loading world{dots}", True, (200, 200, 255))
        surface.blit(text, (center[0] - text.get_width() // 2, center[1] + 40))
