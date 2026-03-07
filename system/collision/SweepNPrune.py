from .algorithm_base import CollisionAlgorithm

class SweepNPrune(CollisionAlgorithm):
    def __init__(self):
        super().__init__()

    def run(self, player, enemies, screen_rect):
        self.checks = 0
        enemies = enemies.sprites()
        num_enemies = len(enemies)

        enemies.sort(key=lambda e: e.rect.left)

        for enemy in enemies:
            self.checks += 1
            self.AABB(player, enemy)

        for i in range(num_enemies):
            for j in range(i + 1, num_enemies):
                if enemies[j].rect.left > enemies[i].rect.right:
                    break  
                self.checks += 1
                self.AABB(enemies[i], enemies[j])