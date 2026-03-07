import pygame
from system.collision.bruteforce import BruteForce
from system.collision.spatial_partitioning.nineneighbor import NineNeighbor
from system.collision.spatial_partitioning.offsetgrid import OffSetGrid
from system.collision.quad_tree.quadtree import QuadTree
from system.collision.SweepNPrune import SweepNPrune

class CollisionManager:
    def __init__(self):
        self.idx = 0
        self.screen_rect = 0
        self.modes = [
            BruteForce(),
            NineNeighbor(),
            OffSetGrid(),
            QuadTree(self.screen_rect),
            SweepNPrune()
        ]
        self.names = [
            "Bruteforce",
            "NineNeighbor",
            "Grid",
            "QuadTree",
            "SweepNPrune"
        ]
        self.active_mode = self.modes[0]
        self.results = {
            "Bruteforce": {"fps": [], "checks": []},
            "NineNeighbor": {"fps": [], "checks": []},
            "Grid": {"fps": [], "checks": []},
            "QuadTree": {"fps": [], "checks": []},
            "SweepNPrune": {"fps": [], "checks": []}
        }

    def input_handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_1, pygame.K_KP1):
                self.idx = 0
            elif event.key in (pygame.K_2, pygame.K_KP2):
                self.idx = 1
            elif event.key in (pygame.K_3, pygame.K_KP3):
                self.idx = 2
            elif event.key in (pygame.K_4, pygame.K_KP4):
                self.idx = 3
            elif event.key in (pygame.K_5, pygame.K_KP5):
                self.idx = 4

    def update(self, player, enemies, screen_rect, clock):
        self.active_mode = self.modes[self.idx]
        self.active_mode.run(player, enemies, screen_rect)
        self.screen_rect = screen_rect
        fps = clock.get_fps()
        checks = self.active_mode.checks
        name = self.names[self.idx]
        self.results[name]["fps"].append(fps)
        self.results[name]["checks"].append(checks)

    def get_checks(self):
        return self.active_mode.checks
    
    def get_current_mode_name(self):
        return self.names[self.idx]