from .bruteforce import BruteForce

class CollisionManager:
    def __init__(self):
        self.idx = 0
        self.modes = [
            BruteForce()
        ]
        self.active_mode = self.modes[self.idx]

    def update(self, player, enemies):
        self.active_mode.run(player, enemies)

    def get_checks(self, player, enemies):
        return self.active_mode.checks