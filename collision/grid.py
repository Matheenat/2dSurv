from .algorithm_base import CollisionAlgorithm

class Grid(CollisionAlgorithm):
    def __init__(self, cell_size = 128):
        super().__init__()
        self.cell_size = cell_size
        self.grid = {}

    def get_cell_coord(self, x, y):
        return (int(x//self.cell_size), int(y//self.cell_size))
    
    def cell_clear(self):
        self.grid.clear()

    def register(self):
        enemies = enemies.sprites()

    def run(self):
        raise Exception("Forgot to override run() in child") 
    