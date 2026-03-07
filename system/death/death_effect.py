import pygame
import random


class DeathEffect:
    def __init__(self):

        # slow motion
        self.slow_duration = 600
        self.slow_timer = 0

        # screen shake
        self.shake_timer = 0
        self.shake_strength = 8

        # red fade
        self.red_alpha = 0
        self.red_speed = 180

        # game over text
        self.text_alpha = 0
        self.text_delay = 400
        self.text_timer = 0

        self.active = False

    def start(self):
        self.active = True
        self.slow_timer = self.slow_duration
        self.shake_timer = 400
        self.red_alpha = 0
        self.text_alpha = 0
        self.text_timer = 0

    def update(self, dt):

        if not self.active:
            return

        if self.slow_timer > 0:
            self.slow_timer -= dt

        if self.shake_timer > 0:
            self.shake_timer -= dt

        if self.red_alpha < 160:
            self.red_alpha += self.red_speed * dt / 1000

        self.text_timer += dt

        if self.text_timer > self.text_delay and self.text_alpha < 255:
            self.text_alpha += 200 * dt / 1000

    def get_slow_multiplier(self):
        if self.slow_timer > 0:
            return 0.35
        return 1

    def get_shake_offset(self):

        if self.shake_timer <= 0:
            return 0, 0

        return (
            random.randint(-self.shake_strength, self.shake_strength),
            random.randint(-self.shake_strength, self.shake_strength),
        )

    def draw_red_overlay(self, screen):

        if self.red_alpha <= 0:
            return

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, int(self.red_alpha)))
        screen.blit(overlay, (0, 0))

    def draw_game_over(self, screen, font_big, font_small):

        if self.text_timer < self.text_delay:
            return

        title = font_big.render("GAME OVER", True, (255, 80, 80))
        hint = font_small.render("Press M to return menu", True, (230, 230, 230))

        title.set_alpha(int(self.text_alpha))
        hint.set_alpha(int(self.text_alpha))

        title_rect = title.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))
        hint_rect = hint.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 40))

        screen.blit(title, title_rect)
        screen.blit(hint, hint_rect)