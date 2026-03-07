import pygame


class MenuScene:
    def __init__(self, screen, clock, change_scene_callback, transition):
        self.screen = screen
        self.clock = clock
        self.change_scene = change_scene_callback
        self.transition = transition

        self.font_big = pygame.font.SysFont(None, 72)
        self.font_small = pygame.font.SysFont(None, 36)

        self.title_text = self.font_big.render("Mini Survivors", True, (255, 255, 255))
        self.start_text = self.font_small.render("Press ENTER to Start", True, (220, 220, 220))

        self.waiting_for_change = False

        self.start_button = pygame.Rect(540, 420, 320, 70)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN and not self.waiting_for_change:
                if event.key == pygame.K_RETURN:
                    self.waiting_for_change = True

                    self.transition.start(
                        mode="out",
                        on_complete=lambda: self.change_scene("play")
                    )
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.start_button.collidepoint(event.pos) and not self.waiting_for_change:
                    self.waiting_for_change = True
                    self.transition.start(
                        mode="out",
                        on_complete=lambda: self.change_scene("play")
                    )

    def update(self):
        self.transition.update()

    def draw(self):
        self.screen.fill((20, 20, 35))

        title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 220))
        start_rect = self.start_text.get_rect(center=(self.screen.get_width() // 2, 340))

        self.screen.blit(self.title_text, title_rect)
        self.screen.blit(self.start_text, start_rect)

        self.transition.draw()

        pygame.draw.rect(self.screen, (70, 70, 120), self.start_button, border_radius=12)

        button_text = self.font_small.render("START", True, (255, 255, 255))
        button_rect = button_text.get_rect(center=self.start_button.center)
        self.screen.blit(button_text, button_rect)