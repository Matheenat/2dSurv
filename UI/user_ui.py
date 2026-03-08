import os
import pygame
from typing import TypedDict
import core.constant_value as constant_value
from utils.sprites import sprite_loader

#
# FILE USER UI สำหรับ UI อย่างเดียวใครทำอย่างอื่นขอให้แฟนไม่รัก
#


class Screen_Config(TypedDict):
    width: int
    height: int
    fullScreen: bool


class ui():
    def __init__(self, surface: pygame.Surface, screen_config: Screen_Config, debug_config):
        self.screen = surface
        self.config = screen_config
        self.debug_settings = debug_config
        self.screen_height = self.screen.get_height()
        self.screen_width = self.screen.get_width()

        self.font_cache = {}
        self.font_dir = os.path.join(constant_value.ASSETS_DIR, "fonts")

        self.sprite_loader = sprite_loader(self.config)

        self.ui_scale = self.config.get('ui_scale', 1)
        self.fonts = {
            'ui': self.load_font("Minecraftia-Regular.ttf", int(18 * self.ui_scale)),
            'med': self.load_font("VCR_OSD_MONO_1.001.ttf", int(28 * self.ui_scale)),
            'big': self.load_font("Daydream DEMO.otf", int(54 * self.ui_scale)),
            'warn': self.load_font("VCR_OSD_MONO_1.001.ttf", int(36 * self.ui_scale)),
            'win': self.load_font("Daydream DEMO.otf", int(64 * self.ui_scale))
        }

        # ===== Debug Panel Settings =====
        self.show_debug = True
        self.debug_x = 18
        self.debug_y = 18
        self.debug_padding = 12
        self.debug_line_gap = 8
        self.debug_text_color = (255, 255, 255)
        self.debug_bg_color = (0, 0, 0, 150)
        self.debug_border_color = (255, 255, 255, 70)

    def load_font(self, filename, size):
        font_key = f"{filename}_{size}"
        if font_key in self.font_cache:
            return self.font_cache[font_key]

        path = os.path.join(self.font_dir, filename)

        if os.path.exists(path):
            font_obj = pygame.font.Font(path, size)
        else:
            font_obj = pygame.font.SysFont(None, size)

        self.font_cache[font_key] = font_obj
        return font_obj

    def toggle_debug(self):
        self.show_debug = not self.show_debug

    def draw_debug(self, surface, label, value, position):
        text_surface = self.fonts['ui'].render(f"{label}: {round(value, 2)}", True, (255, 255, 255))
        surface.blit(text_surface, position)

    def draw_mode(self, surface, label, text, position):
        text_surface = self.fonts['ui'].render(f"{label}: {text}", True, (255, 255, 255))
        surface.blit(text_surface, position)

    def draw_grid(self, height, width, surface):
        self.cell_size = 128
        for x in range(0, width, self.cell_size):
            pygame.draw.line(surface, (100, 100, 100), (x, 0), (x, height))

        for y in range(0, height, self.cell_size):
            pygame.draw.line(surface, (100, 100, 100), (0, y), (width, y))

    def build_debug_lines(self, player, col_manager, enemy_group, fps, god_mode, autofire_enabled):
        lines = []

        if self.debug_settings.get('fps'):
            lines.append(f"FPS: {round(fps, 2)}")

        if self.debug_settings.get('enemy'):
            lines.append(f"Enemy: {len(enemy_group)}")

        if self.debug_settings.get('speed'):
            lines.append(f"Speed: {round(player.current_speed, 2)}")

        if self.debug_settings.get('checks'):
            lines.append(f"Checks: {col_manager.get_checks()}")

        if self.debug_settings.get('current_mode'):
            lines.append(f"Current Mode: {col_manager.get_current_mode_name()}")

        lines.append(f"God Mode [G]: {'ON' if god_mode else 'OFF'}")
        lines.append(f"Auto Fire [P]: {'ON' if autofire_enabled else 'OFF'}")
        lines.append("Toggle Debug [F1]")

        return lines

    def draw_debug_panel(self, lines):
        if not lines:
            return

        font = self.fonts['ui']
        line_height = font.get_height() + self.debug_line_gap

        max_width = 0
        for line in lines:
            text_width, _ = font.size(line)
            if text_width > max_width:
                max_width = text_width

        panel_width = max_width + (self.debug_padding * 2)
        panel_height = (len(lines) * line_height) + (self.debug_padding * 2) - self.debug_line_gap

        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill(self.debug_bg_color)

        pygame.draw.rect(
            panel_surface,
            self.debug_border_color,
            panel_surface.get_rect(),
            width=1,
            border_radius=10
        )

        self.screen.blit(panel_surface, (self.debug_x, self.debug_y))

        text_x = self.debug_x + self.debug_padding
        text_y = self.debug_y + self.debug_padding

        for line in lines:
            text_surface = font.render(line, True, self.debug_text_color)
            self.screen.blit(text_surface, (text_x, text_y))
            text_y += line_height

    def draw_all_debug(self, player, col_manager, enemy_group, fps, camera_offset, god_mode, autofire_enabled):
        if self.show_debug:
            debug_lines = self.build_debug_lines(
                player,
                col_manager,
                enemy_group,
                fps,
                god_mode,
                autofire_enabled
            )
            self.draw_debug_panel(debug_lines)

        if self.debug_settings.get('9Ngrid'):
            self.draw_grid(self.screen_height, self.screen_width, self.screen)

        if self.debug_settings.get('quad_tree'):
            active_mode = col_manager.active_mode
            if hasattr(active_mode, 'root') and active_mode.root:
                active_mode.root.draw_debug(self.screen, camera_offset)