import os
import pygame
from core.game import Game

class PlayScene:
    def __init__(self, screen, clock, change_scene_callback, transition):
        self.screen = screen
        self.clock = clock
        self.change_scene = change_scene_callback
        self.transition = transition

        self.game = Game(self.screen, self.clock)

        self.transition.start(mode="in")
        self.leaving_scene = False

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fonts_dir = os.path.join(base_dir, "assets", "fonts")
        menu_font_path = os.path.join(fonts_dir, "VCR_OSD_MONO_1.001.ttf")
        small_font_path = os.path.join(fonts_dir, "Minecraftia-Regular.ttf")

        self.font_title = pygame.font.Font(menu_font_path, 42)
        self.font_menu = pygame.font.Font(menu_font_path, 28)
        self.font_small = pygame.font.Font(small_font_path, 14)

        self.paused = False
        self.pause_items = ["RESUME", "MENU"]
        self.pause_selected = 0
        self.pause_rects = []

        self.pause_panel = pygame.Rect(0, 0, 420, 260)
        self.on_resize()

    def on_resize(self):
        self.pause_panel = pygame.Rect(0, 0, 420, 260)
        self.pause_panel.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        self._rebuild_pause_rects()

        if hasattr(self, "game"):
            self.game.on_resize(self.screen)

    def _rebuild_pause_rects(self):
        self.pause_rects = []
        start_y = self.pause_panel.y + 110
        for i in range(len(self.pause_items)):
            rect = pygame.Rect(0, 0, 240, 52)
            rect.centerx = self.pause_panel.centerx
            rect.y = start_y + i * 68
            self.pause_rects.append(rect)

    def _activate_pause_selected(self):
        choice = self.pause_items[self.pause_selected]

        if choice == "RESUME":
            self.paused = False

        elif choice == "MENU":
            self.paused = False
            self.leaving_scene = True
            self.transition.start(
                mode="out",
                on_complete=lambda: self.change_scene("menu")
            )

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False

            if self.leaving_scene:
                continue

            if event.type == pygame.KEYDOWN:
                if self.game.game_over:
                    if event.key == pygame.K_m:
                        self.leaving_scene = True
                        self.transition.start(
                            mode="out",
                            on_complete=lambda: self.change_scene("menu")
                        )
                    continue

                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                    continue

                if self.paused:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.pause_selected = (self.pause_selected - 1) % len(self.pause_items)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.pause_selected = (self.pause_selected + 1) % len(self.pause_items)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self._activate_pause_selected()

            if self.paused and event.type == pygame.MOUSEMOTION:
                for i, rect in enumerate(self.pause_rects):
                    if rect.collidepoint(event.pos):
                        self.pause_selected = i

            if self.paused and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(self.pause_rects):
                    if rect.collidepoint(event.pos):
                        self.pause_selected = i
                        self._activate_pause_selected()
                        break

        if not self.leaving_scene and not self.paused:
            self.game.handle_events(events)

    def update(self):
        if not self.leaving_scene and self.game.running and not self.paused:
            self.game.update()

        self.transition.update()

    def _draw_pause_overlay(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        shadow = self.pause_panel.move(6, 6)
        pygame.draw.rect(self.screen, (0, 0, 0), shadow, border_radius=20)

        panel_surface = pygame.Surface((self.pause_panel.width, self.pause_panel.height), pygame.SRCALPHA)
        panel_surface.fill((18, 22, 34, 230))
        self.screen.blit(panel_surface, self.pause_panel.topleft)

        pygame.draw.rect(self.screen, (140, 200, 255), self.pause_panel, width=3, border_radius=20)

        title = self.font_title.render("PAUSED", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(self.pause_panel.centerx, self.pause_panel.y + 55)))

        for i, rect in enumerate(self.pause_rects):
            selected = i == self.pause_selected
            fill = (70, 110, 200) if selected else (35, 45, 70)
            border = (180, 220, 255) if selected else (90, 110, 140)

            pygame.draw.rect(self.screen, fill, rect, border_radius=12)
            pygame.draw.rect(self.screen, border, rect, width=2, border_radius=12)

            text = self.font_menu.render(self.pause_items[i], True, (255, 255, 255))
            self.screen.blit(text, text.get_rect(center=rect.center))

        hint = self.font_small.render("ESC = Resume", True, (190, 180, 200))
        self.screen.blit(hint, hint.get_rect(center=(self.pause_panel.centerx, self.pause_panel.bottom - 16)))

    def draw(self):
        self.game.draw()

        if self.paused:
            self._draw_pause_overlay()

        self.transition.draw()