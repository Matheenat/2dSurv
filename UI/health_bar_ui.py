import pygame


class HealthBarUI:
    def __init__(self, font):
        self.font = font

        self.bar_width = 240
        self.bar_height = 22

        self.margin_x = 40
        self.margin_y = 35

        self.bg_color = (45, 45, 45)
        self.fill_color = (200, 50, 50)
        self.low_hp_color = (255, 70, 70)
        self.border_color = (255, 255, 255)
        self.text_color = (255, 255, 255)
        self.shadow_color = (0, 0, 0, 110)

        self.segment_count = 10
        self.segment_gap = 3

        self.low_hp_threshold = 0.3
        self.blink_interval = 250 
        self.blink_timer = 0
        self.blink_on = True

    def update(self, dt):
        self.blink_timer += dt
        if self.blink_timer >= self.blink_interval:
            self.blink_timer = 0
            self.blink_on = not self.blink_on

    def draw(self, screen, hp, max_hp):
        if max_hp <= 0:
            return

        ratio = hp / max_hp
        ratio = max(0, min(1, ratio))

        x = screen.get_width() - self.bar_width - self.margin_x
        y = self.margin_y

        current_fill_color = self.fill_color
        is_low_hp = ratio <= self.low_hp_threshold

        if is_low_hp:
            if self.blink_on:
                current_fill_color = self.low_hp_color
            else:
                current_fill_color = (170, 35, 35)

        heart_surface = self.font.render("❤", True, (255, 80, 80))
        text_surface = self.font.render(f" HP: {hp} / {max_hp}", True, self.text_color)

        total_width = heart_surface.get_width() + text_surface.get_width()
        text_x = screen.get_width() - total_width - self.margin_x
        text_y = y

        heart_shadow = self.font.render("❤", True, (0, 0, 0))
        text_shadow = self.font.render(f" HP: {hp} / {max_hp}", True, (0, 0, 0))

        screen.blit(heart_shadow, (text_x + 2, text_y + 2))
        screen.blit(text_shadow, (text_x + heart_surface.get_width() + 2, text_y + 2))

        screen.blit(heart_surface, (text_x, text_y))
        screen.blit(text_surface, (text_x + heart_surface.get_width(), text_y))

        bar_y = y + 32
        bar_rect = pygame.Rect(x, bar_y, self.bar_width, self.bar_height)

        shadow_surf = pygame.Surface((self.bar_width, self.bar_height), pygame.SRCALPHA)
        shadow_surf.fill(self.shadow_color)
        screen.blit(shadow_surf, (x + 3, bar_y + 3))

        pygame.draw.rect(screen, self.bg_color, bar_rect, border_radius=8)

        total_gap = self.segment_gap * (self.segment_count - 1)
        segment_width = (self.bar_width - total_gap) / self.segment_count

        filled_segments = ratio * self.segment_count

        for i in range(self.segment_count):
            seg_x = x + i * (segment_width + self.segment_gap)
            seg_rect = pygame.Rect(int(seg_x), bar_y, int(segment_width), self.bar_height)

            pygame.draw.rect(screen, (65, 65, 65), seg_rect, border_radius=4)

            fill_amount = max(0, min(1, filled_segments - i))
            if fill_amount > 0:
                inner_width = int(segment_width * fill_amount)
                fill_rect = pygame.Rect(int(seg_x), bar_y, inner_width, self.bar_height)
                pygame.draw.rect(screen, current_fill_color, fill_rect, border_radius=4)

        pygame.draw.rect(screen, self.border_color, bar_rect, width=2, border_radius=8)