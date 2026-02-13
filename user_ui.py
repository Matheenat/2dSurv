import os
import pygame # type: ignore
import math
from typing import TypedDict
import constant_value # type: ignore
from sprites import sprite_loader # type: ignore
#
# FILE USER UI สำหรับค่าที่ล็อกจอ ห้าม implement ของที่ขยับไปมา เช่น กล้อง, world gen
#
class Screen_Config(TypedDict):
    width: int
    height: int
    fullScreen: bool

class ui():
    def __init__(self, screen: pygame.Surface, config_data: Screen_Config): 
        self.display_surface = screen
        self.config = config_data
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
    
    
    
#     screen = pygame.display.set_mode((WIN_W, WIN_H), FLAGS_WINDOWED)
#     def draw_player_hp_bar(surface, player_rect_screen, hp, hp_max):
#     w = player_rect_screen.width
#     h = 7
#     x = player_rect_screen.left
#     y = player_rect_screen.bottom + 6
#     ratio = 0.0 if hp_max <= 0 else max(0.0, min(1.0, hp / hp_max))
#     pygame.draw.rect(surface, (20, 20, 20), (x, y, w, h), border_radius=4)
#     pygame.draw.rect(surface, (70, 220, 90), (x, y, int(w * ratio), h), border_radius=4)
#     pygame.draw.rect(surface, (230, 230, 230), (x, y, w, h), 1, border_radius=4)

#     def draw_dash_cd_bar(surface, player_rect_screen, cd, cd_max):
#     w = player_rect_screen.width
#     h = 6
#     x = player_rect_screen.left
#     y = player_rect_screen.bottom + 6 + 7 + 5  # ใต้ HP bar

#     if cd_max <= 0:
#         ratio = 1.0
#     else:
#         ratio = 1.0 - max(0.0, min(1.0, cd / cd_max))  # cd=0 -> เต็มหลอด

#     pygame.draw.rect(surface, (20, 20, 20), (x, y, w, h), border_radius=4)
#     pygame.draw.rect(surface, (120, 210, 255), (x, y, int(w * ratio), h), border_radius=4)
#     pygame.draw.rect(surface, (230, 230, 230), (x, y, w, h), 1, border_radius=4)

#     def draw_stamina_bar(surface, player_rect_screen, stamina, stamina_max):
#     w = player_rect_screen.width
#     h = 5
#     x = player_rect_screen.left
#     y = player_rect_screen.bottom + 6 + 7 + 5 + 6 + 4  # ใต้ dash bar
#     ratio = 0.0 if stamina_max <= 0 else max(0.0, min(1.0, stamina / stamina_max))
#     pygame.draw.rect(surface, (20, 20, 20), (x, y, w, h), border_radius=4)
#     pygame.draw.rect(surface, (255, 240, 120), (x, y, int(w * ratio), h), border_radius=4)
#     pygame.draw.rect(surface, (230, 230, 230), (x, y, w, h), 1, border_radius=4)







# from typing import TypedDict 
# class ProgressData(TypedDict):
#     exp: int
#     exp_need: int
#     level: int

# class AnimData(TypedDict):
#     fill_ratio: float
#     t: float

# def draw_exp_bar_fancy(
#     surface: pygame.Surface, 
#     prog: ProgressData, 
#     anim: AnimData, 
#     dt: float, 
#     height: int = 14, 
#     pad: int = 14
# ) -> None:
#     vw, vh = surface.get_size()
    
#     # 1. Update Logic
#     target = max(0.0, min(1.0, prog["exp"] / prog["exp_need"])) if prog["exp_need"] > 0 else 0.0
#     anim["fill_ratio"] += (target - anim["fill_ratio"]) * min(1.0, 10.0 * dt)
#     anim["t"] += dt
        
#     r = anim["fill_ratio"]
#     bar_rect = pygame.Rect(pad, vh - height - pad, vw - pad * 2, height)
#     fill_w = int(bar_rect.w * r)

#     # 2. Colors & Pulsing
#     pulse = (math.sin(anim["t"] * 8.0) * 0.5 + 0.5) if r >= 0.8 else 0.0
#     boost = int(30 * pulse)
#     fill_col = [min(255, c + boost) for c in (90, 170, 255)]

#     # 3. Draw Background & Fill
#     pygame.draw.rect(surface, (18, 18, 22), bar_rect, border_radius=10)
    
#     if fill_w > 4:
#         fill_rect = pygame.Rect(bar_rect.x, bar_rect.y, fill_w, bar_rect.h)
#         pygame.draw.rect(surface, fill_col, fill_rect, border_radius=10)

#         # 4. Sheen Overlay
#         sheen_w = bar_rect.w // 8
#         sheen_x = bar_rect.x + (anim["t"] * 220 % (bar_rect.w + sheen_w)) - sheen_w
#         sheen_rect = pygame.Rect(sheen_x, bar_rect.y, sheen_w, bar_rect.h).clip(fill_rect)
        
#         if sheen_rect.width > 0:
#             surface.fill((40, 40, 40), sheen_rect, special_flags=pygame.BLEND_RGB_ADD)

#         # 5. Border & Text
#         pygame.draw.rect(surface, (210, 210, 210), bar_rect, 2, border_radius=10)
        
#         label = f"Lv {prog['level']} EXP {prog['exp']}/{prog['exp_need']}"
#         # Assuming FONT_UI is defined globally as a pygame.font.Font object
#         text_surf = FONT_UI.render(label, True, (235, 235, 235))
#         surface.blit(text_surf, (bar_rect.x, bar_rect.y - 20))
        