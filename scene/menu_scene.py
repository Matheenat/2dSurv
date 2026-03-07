import os
import pygame

class MenuScene:
    def __init__(self, screen, clock, change_scene_callback, transition,
                 toggle_fullscreen_callback, get_fullscreen_state_callback):
        self.screen = screen
        self.clock = clock
        self.change_scene = change_scene_callback
        self.transition = transition
        self.toggle_fullscreen = toggle_fullscreen_callback
        self.get_fullscreen_state = get_fullscreen_state_callback

        self.waiting_for_change = False
        self.show_how_to_play = False
        self.show_settings = False

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fonts_dir = os.path.join(base_dir, "assets", "fonts")

        title_font_path = os.path.join(fonts_dir, "Daydream DEMO.otf")
        menu_font_path = os.path.join(fonts_dir, "VCR_OSD_MONO_1.001.ttf")
        small_font_path = os.path.join(fonts_dir, "Minecraftia-Regular.ttf")

        self.font_title = pygame.font.Font(title_font_path, 34)
        self.font_menu = pygame.font.Font(menu_font_path, 36)
        self.font_small = pygame.font.Font(small_font_path, 16)
        self.font_tiny = pygame.font.Font(small_font_path, 12)

        self.menu_items = ["PLAY", "HOW TO PLAY", "SETTINGS", "QUIT"]
        self.selected_index = 0

        self.settings_items = ["FULLSCREEN"]
        self.settings_selected = 0
        self.settings_rects = []

        self.panel_rect = pygame.Rect(0, 0, 640, 470)
        self.panel_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 30)

        self.menu_rects = []
        self._rebuild_menu_rects()

        self.bg_offset = 0

    def on_resize(self):
        self.panel_rect = pygame.Rect(0, 0, 640, 470)
        self.panel_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 30)
        self._rebuild_menu_rects()

    def _rebuild_menu_rects(self):
        self.menu_rects = []
        start_y = self.panel_rect.y + 145
        for i in range(len(self.menu_items)):
            rect = pygame.Rect(0, 0, 360, 58)
            rect.centerx = self.panel_rect.centerx
            rect.y = start_y + i * 72
            self.menu_rects.append(rect)

        self.settings_rects = []
        settings_box_y = self.panel_rect.y + 165
        for i in range(len(self.settings_items)):
            rect = pygame.Rect(0, 0, 420, 56)
            rect.centerx = self.panel_rect.centerx
            rect.y = settings_box_y + i * 72
            self.settings_rects.append(rect)

    def _activate_selected(self):
        if self.waiting_for_change:
            return

        choice = self.menu_items[self.selected_index]

        if choice == "PLAY":
            self.waiting_for_change = True
            self.transition.start(
                mode="out",
                on_complete=lambda: self.change_scene("play")
            )

        elif choice == "HOW TO PLAY":
            self.show_how_to_play = True

        elif choice == "SETTINGS":
            self.show_settings = True

        elif choice == "QUIT":
            pygame.quit()
            raise SystemExit

    def _toggle_settings_selected(self):
        choice = self.settings_items[self.settings_selected]

        if choice == "FULLSCREEN":
            self.toggle_fullscreen()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.MOUSEMOTION:
                if self.show_settings:
                    for i, rect in enumerate(self.settings_rects):
                        if rect.collidepoint(event.pos):
                            self.settings_selected = i
                elif not self.show_how_to_play:
                    for i, rect in enumerate(self.menu_rects):
                        if rect.collidepoint(event.pos):
                            self.selected_index = i

            if event.type == pygame.KEYDOWN:
                if self.show_how_to_play:
                    if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE, pygame.K_RETURN):
                        self.show_how_to_play = False
                    continue

                if self.show_settings:
                    if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                        self.show_settings = False
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        self.settings_selected = (self.settings_selected - 1) % len(self.settings_items)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.settings_selected = (self.settings_selected + 1) % len(self.settings_items)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_d):
                        self._toggle_settings_selected()
                    continue

                if event.key in (pygame.K_UP, pygame.K_w):
                    self.selected_index = (self.selected_index - 1) % len(self.menu_items)

                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected_index = (self.selected_index + 1) % len(self.menu_items)

                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self._activate_selected()

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.show_how_to_play:
                    self.show_how_to_play = False
                    continue

                if self.show_settings:
                    clicked_any = False
                    for i, rect in enumerate(self.settings_rects):
                        if rect.collidepoint(event.pos):
                            self.settings_selected = i
                            self._toggle_settings_selected()
                            clicked_any = True
                            break

                    if not clicked_any:
                        self.show_settings = False
                    continue

                for i, rect in enumerate(self.menu_rects):
                    if rect.collidepoint(event.pos):
                        self.selected_index = i
                        self._activate_selected()
                        break

        self.on_resize()

    def update(self):
        self.bg_offset = (self.bg_offset + 1) % self.screen.get_height()
        self.transition.update()

    def _draw_background(self):
        w, h = self.screen.get_size()

        top_color = (12, 18, 38)
        bottom_color = (30, 10, 46)

        for y in range(h):
            t = y / h
            r = int(top_color[0] + (bottom_color[0] - top_color[0]) * t)
            g = int(top_color[1] + (bottom_color[1] - top_color[1]) * t)
            b = int(top_color[2] + (bottom_color[2] - top_color[2]) * t)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (w, y))

        stripe_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        stripe_color = (255, 255, 255, 18)

        for i in range(-h, h, 64):
            y = i + self.bg_offset
            pygame.draw.line(stripe_surface, stripe_color, (0, y), (w, y + 120), 2)

        self.screen.blit(stripe_surface, (0, 0))

    def _draw_main_menu(self):
        shadow = self.panel_rect.move(8, 8)
        pygame.draw.rect(self.screen, (0, 0, 0), shadow, border_radius=24)

        panel_surface = pygame.Surface((self.panel_rect.width, self.panel_rect.height), pygame.SRCALPHA)
        panel_surface.fill((18, 22, 34, 220))
        self.screen.blit(panel_surface, self.panel_rect.topleft)

        pygame.draw.rect(self.screen, (120, 180, 255), self.panel_rect, width=3, border_radius=24)

        title = self.font_title.render("2D SURVIVAL", True, (245, 245, 255))
        title_rect = title.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 70))
        self.screen.blit(title, title_rect)

        subtitle = self.font_small.render("Survive the swarm.", True, (180, 210, 255))
        subtitle_rect = subtitle.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 110))
        self.screen.blit(subtitle, subtitle_rect)

        for i, rect in enumerate(self.menu_rects):
            selected = i == self.selected_index
            fill = (70, 110, 200) if selected else (35, 45, 70)
            border = (180, 220, 255) if selected else (90, 110, 140)

            pygame.draw.rect(self.screen, fill, rect, border_radius=14)
            pygame.draw.rect(self.screen, border, rect, width=2, border_radius=14)

            text = self.font_menu.render(self.menu_items[i], True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

        hint = self.font_tiny.render("Arrow / W S  •  Enter  •  Mouse  •  F11 = Fullscreen", True, (180, 180, 190))
        hint_rect = hint.get_rect(center=(self.panel_rect.centerx, self.panel_rect.bottom - 28))
        self.screen.blit(hint, hint_rect)

    def _draw_how_to_play(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        box = pygame.Rect(0, 0, 760, 430)
        box.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)

        pygame.draw.rect(self.screen, (20, 24, 36), box, border_radius=22)
        pygame.draw.rect(self.screen, (140, 190, 255), box, width=3, border_radius=22)

        title = self.font_menu.render("HOW TO PLAY", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(box.centerx, box.y + 50)))

        lines = [
            "Move with W A S D",
            "Auto fire attacks the nearest enemy",
            "Avoid getting surrounded",
            "Press ESC during gameplay to open Pause",
            "Resume returns to the game",
            "Menu goes back to the main menu",
        ]

        y = box.y + 110
        for line in lines:
            txt = self.font_small.render(line, True, (230, 230, 240))
            self.screen.blit(txt, (box.x + 55, y))
            y += 45

        close_text = self.font_tiny.render("Press ESC / ENTER / Click to go back", True, (180, 180, 190))
        close_rect = close_text.get_rect(center=(box.centerx, box.bottom - 30))
        self.screen.blit(close_text, close_rect)

    def _draw_settings(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        box = pygame.Rect(0, 0, 760, 350)
        box.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)

        pygame.draw.rect(self.screen, (20, 24, 36), box, border_radius=22)
        pygame.draw.rect(self.screen, (140, 190, 255), box, width=3, border_radius=22)

        title = self.font_menu.render("SETTINGS", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(box.centerx, box.y + 50)))

        is_fullscreen = self.get_fullscreen_state()

        for i, rect in enumerate(self.settings_rects):
            selected = i == self.settings_selected
            fill = (70, 110, 200) if selected else (35, 45, 70)
            border = (180, 220, 255) if selected else (90, 110, 140)

            pygame.draw.rect(self.screen, fill, rect, border_radius=14)
            pygame.draw.rect(self.screen, border, rect, width=2, border_radius=14)

            checkbox = "[✓]" if is_fullscreen else "[ ]"
            label = f"{self.settings_items[i]}  {checkbox}"

            text = self.font_menu.render(label, True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

        help_text = self.font_small.render("Enter / Click / D to toggle", True, (220, 220, 230))
        self.screen.blit(help_text, help_text.get_rect(center=(box.centerx, box.bottom - 60)))

        close_text = self.font_tiny.render("Press ESC / BACKSPACE to go back", True, (180, 180, 190))
        self.screen.blit(close_text, close_text.get_rect(center=(box.centerx, box.bottom - 28)))

    def draw(self):
        self._draw_background()
        self._draw_main_menu()

        if self.show_how_to_play:
            self._draw_how_to_play()

        if self.show_settings:
            self._draw_settings()

        self.transition.draw()