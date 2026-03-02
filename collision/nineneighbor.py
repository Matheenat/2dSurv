from .grid import Grid

class NineNeighbor(Grid):
    def __init__(self):
        super().__init__()

    def run(self, player, enemies):
        self.checks = 0
        self.grid.clear()
        enemies = enemies.sprites()