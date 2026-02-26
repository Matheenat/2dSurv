from .bruteforce import BruteForce

class CollisionManager:
    def __init__(self):
        self.idx = 0
        self.modes = {
            "brute": BruteForce(),
            #"grid": SpatialGrid()
        }
        self.active_mode = self.modes["brute"]

    def update(self, player, enemies):
        self.active_mode.run(player, enemies)

    def get_checks(self):
        return self.active_mode.checks