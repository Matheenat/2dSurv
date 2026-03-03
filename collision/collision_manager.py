import pygame # type: ignore
from .bruteforce import BruteForce
from .nineneighbor import NineNeighbor
from .offsetgrid import OffSetGrid

class CollisionManager:
    def __init__(self):
        self.idx = 2
        self.modes = [
            BruteForce(),
            NineNeighbor(),
            OffSetGrid()
        ]
        self.active_mode = self.modes[0]

    def input_handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.idx = 0
            elif event.key == pygame.K_2:
                self.idx = 1
            elif event.key == pygame.K_3:
                self.idx = 2

    def update(self, player, enemies):
        self.active_mode = self.modes[self.idx]
        self.active_mode.run(player, enemies)

    def get_checks(self, player, enemies):
        return self.active_mode.checks