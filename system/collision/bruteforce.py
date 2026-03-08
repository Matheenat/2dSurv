from .algorithm_base import CollisionAlgorithm

class BruteForce(CollisionAlgorithm):
    def __init__(self):
        super().__init__()
        
    def run(self, player, enemies, screen_rect):
        self.checks = 0
        enemies = enemies.sprites()
        num_enemies = len(enemies)

        # ตรวจสอบผู้เล่นกับศัตรูทุกตัว
        for enemy in enemies:
            self.checks += 1
            self.AABB(player, enemy)
        
        # ตรวจสอบศัตรูทุกตัวกับศัตรูทุกตัวแบบตรง ๆ
        # เป็นลูปซ้อน จึงเป็นแนวคิดแบบ Brute Force
        for i in range(num_enemies):
            for j in range(i + 1, len(enemies)):
                self.checks += 1
                self.AABB(enemies[i], enemies[j])