from game import Game
import pygame


class PlayScene:
    def __init__(self, screen, clock, change_scene_callback, transition):
        self.screen = screen
        self.clock = clock
        self.change_scene = change_scene_callback
        self.transition = transition

        self.game = Game()
        self.game.screen = screen
        self.game.clock = clock

        self.transition.start(mode="in")
        self.leaving_scene = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False

            if event.type == pygame.KEYDOWN and not self.leaving_scene:
                if event.key == pygame.K_ESCAPE:
                    self.leaving_scene = True
                    self.transition.start(
                        mode="out",
                        on_complete=lambda: self.change_scene("menu")
                    )
                    return

        if not self.leaving_scene:
            self.game.handle_events(events)

    def update(self):
        if not self.leaving_scene and self.game.running:
            self.game.update()

        self.transition.update()

    def draw(self):
        self.game.draw()
        self.transition.draw()