from .grid import Grid

class OffSetGrid(Grid):
    def __init__(self):
        super().__init__()
    
    def register(self, player, enemy_group, offset: int):
        self.cell_clear()
        temp_grid = {}
        player_coord = self.get_cell_coord(player.rect.centerx,player.rect.centery)
        enemies = enemy_group.sprites() 

        for enemy in enemies:
            key = self.get_cell_coord(enemy.rect.centerx + offset, enemy.rect.centery + offset)
            if key not in temp_grid:
                temp_grid[key] = []
            temp_grid[key].append(enemy)
        
        return temp_grid, player_coord
    
    def run(self, player, enemies):
        self.gridA , _ = self.register(player, enemies, 0)
        self.gridB , _ = self.register(player, enemies, self.cell_size//2)

        playerA = self.get_cell_coord(player.rect.centerx, player.rect.centery)
        playerB = self.get_cell_coord(player.rect.centerx + self.cell_size//2, player.rect.centery + self.cell_size//2)
        
        self.checks = 0
        checked_pair = set()

        for current_grid in [self.gridA, self.gridB]:
            for current_cell in current_grid.values():            
                for i in range(len(current_cell)):
                    for j in range(i + 1, len(current_cell)):
                        enemyA, enemyB = current_cell[i], current_cell[j]

                        pair = tuple(sorted((id(enemyA), id(enemyB))))
                        if pair not in checked_pair:
                            self.checks += 1
                            self.AABB(enemyA, enemyB)
                            checked_pair.add(pair)

            player_cellA = self.gridA.get(playerA)
            if player_cellA:
                for enemy in player_cellA:
                    if enemy is not player:
                        self.checks += 1
                        self.AABB(player, enemy)
            
            player_cellB = self.gridB.get(playerB)
            if player_cellB:
                for enemy in player_cellB:
                    if enemy is not player:
                        self.checks += 1
                        self.AABB(player, enemy)