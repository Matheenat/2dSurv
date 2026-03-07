import pygame
import os
import core.constant_value as constant_value


class GameOverUI:
    def __init__(self):
        font_dir = os.path.join(constant_value.ASSETS_DIR, "fonts")

        title_path = os.path.join(font_dir, "VCR_OSD_MONO_1.001.ttf")
        small_path = os.path.join(font_dir, "Minecraftia-Regular.ttf")

        self.title_font = pygame.font.Font(title_path, 52)
        self.small_font = pygame.font.Font(small_path, 20)

    def draw(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = self.title_font.render("GAME OVER", True, (255, 80, 80))
        hint = self.small_font.render("Press M to return menu", True, (230, 230, 230))

        title_rect = title.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 20))
        hint_rect = hint.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 35))

        screen.blit(title, title_rect)
        screen.blit(hint, hint_rect)