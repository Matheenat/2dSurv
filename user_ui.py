import os
import pygame # type: ignore
from typing import TypedDict
import constant_value 
from sprites import sprite_loader 
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
        self.font_dir = os.path.join(constant_value.ASSETS_DIR,"fonts")

        self.sprite_loader = sprite_loader(self.config)

        self.ui_scale = self.config.get('ui_scale', 1)
        self.fonts = {
            'ui': self.load_font("Minecraftia-Regular.ttf", int(18 * self.ui_scale)),
            'med': self.load_font("VCR_OSD_MONO_1.001.ttf", int(28 * self.ui_scale)),
            'big': self.load_font("Daydream DEMO.otf", int(54 * self.ui_scale)),
            'warn': self.load_font("VCR_OSD_MONO_1.001.ttf", int(36 * self.ui_scale)),
            'win': self.load_font("Daydream DEMO.otf", int(64 * self.ui_scale))
        }
        
    
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
    
    def draw_all_debug(self, player, col_manager, enemy_group, fps):
        self.current_y = 20
        x_pos = 50

        if self.debug_settings.get('speed') == "True":
            self.draw_debug(self.screen, "Speed", player.current_speed, (x_pos, self.current_y))
            self.current_y += 30

        if self.debug_settings.get('checks') == "True":
            self.draw_debug(self.screen, "Checks", col_manager.get_checks(player, enemy_group), (x_pos, self.current_y))
            self.current_y += 30

        if self.debug_settings.get('current_mode') == "True":
            self.draw_mode(self.screen, "Current Mode", col_manager.active_mode.__class__.__name__, (x_pos, self.current_y))
            self.current_y += 30

        if self.debug_settings.get('9Ngrid') == "True":
            self.draw_grid(self.screen_height, self.screen_width, self.screen)

        if self.debug_settings.get('fps') == "True":
            self.draw_debug(self.screen, "FPS", fps, (x_pos, self.current_y))
            self.current_y += 30