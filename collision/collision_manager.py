import pygame # type: ignore
from .bruteforce import BruteForce
from .spatial_partitioning.nineneighbor import NineNeighbor
from .spatial_partitioning.offsetgrid import OffSetGrid
from .quad_tree.quadtree import QuadTree

class CollisionManager:
    def __init__(self):
        self.idx = 0
        self.screen_rect = 0
        self.modes = [
            BruteForce(),
            NineNeighbor(),
            OffSetGrid(),
            QuadTree(self.screen_rect)
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
            elif event.key == pygame.K_4:
                self.idx = 3

    def update(self, player, enemies, screen_rect):
        self.active_mode = self.modes[self.idx]
        self.active_mode.run(player, enemies, screen_rect)
        self.screen_rect = screen_rect

    def get_checks(self, player, enemies):
        return self.active_mode.checks