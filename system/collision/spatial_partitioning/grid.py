from system.collision.algorithm_base import CollisionAlgorithm

class Grid(CollisionAlgorithm):
    def __init__(self, cell_size = 128):
        super().__init__()
        self.cell_size = cell_size
        self.grid = {}

    def get_cell_coord(self, x, y):
        return (int(x//self.cell_size), int(y//self.cell_size))
    
    def cell_clear(self):
        self.grid.clear()

    def register(self, player, enemy_group, offset: int):
        self.cell_clear()
        self.player_coord = self.get_cell_coord(player.rect.centerx,player.rect.centery)
        enemies = enemy_group.sprites() 

        for enemy in enemies:
            key = self.get_cell_coord(enemy.rect.centerx + offset, enemy.rect.centery + offset)
            if key not in self.grid:
                self.grid[key] = []
            self.grid[key].append(enemy)
        
    def run(self):
        raise Exception("Forgot to override run() in child") 
    