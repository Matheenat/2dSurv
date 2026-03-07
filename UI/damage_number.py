import pygame


class DamageNumber:
    def __init__(self, x, y, value, font):
        self.x = float(x)
        self.y = float(y)
        self.value = value
        self.font = font

        self.lifetime = 700
        self.timer = self.lifetime

        self.float_speed = 0.08

    def update(self, dt):
        self.timer -= dt
        self.y -= self.float_speed * dt

    def is_alive(self):
        return self.timer > 0

    def draw(self, screen, camera_offset):
        alpha_ratio = max(0, self.timer / self.lifetime)
        alpha = int(255 * alpha_ratio)

        text_surface = self.font.render(f"-{self.value}", True, (255, 80, 80)).convert_alpha()
        text_surface.set_alpha(alpha)

        screen_x = int(self.x - camera_offset.x)
        screen_y = int(self.y - camera_offset.y)

        screen.blit(text_surface, (screen_x, screen_y))