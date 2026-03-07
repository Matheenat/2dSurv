import pygame


class FadeTransition:
    def __init__(self, screen, duration=500):
        self.screen = screen
        self.duration = duration
        self.active = False
        self.start_time = 0
        self.mode = "in"   # "in" หรือ "out"
        self.on_complete = None

        self.overlay = pygame.Surface(self.screen.get_size())
        self.overlay.fill((0, 0, 0))

    def start(self, mode="in", on_complete=None):
        self.active = True
        self.start_time = pygame.time.get_ticks()
        self.mode = mode
        self.on_complete = on_complete

    def update(self):
        if not self.active:
            return

        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time

        if elapsed >= self.duration:
            self.active = False
            if self.on_complete:
                callback = self.on_complete
                self.on_complete = None
                callback()

    def draw(self):
        if not self.active:
            return

        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        progress = min(elapsed / self.duration, 1)

        if self.mode == "out":
            alpha = int(progress * 255)
        else:
            alpha = int((1 - progress) * 255)

        self.overlay.set_alpha(alpha)
        self.screen.blit(self.overlay, (0, 0))