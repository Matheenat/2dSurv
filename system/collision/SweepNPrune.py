from .algorithm_base import CollisionAlgorithm

class SweepNPrune(CollisionAlgorithm):
    def __init__(self):
        super().__init__()

    def run(self, player, enemies, screen_rect):
        self.checks = 0
        enemies = enemies.sprites()
        num_enemies = len(enemies)

        # เรียงศัตรูตามตำแหน่งด้านซ้ายบนแกน X
        # เพื่อให้วัตถุที่อยู่ใกล้กันอยู่ติดกันในลิสต์
        enemies.sort(key=lambda e: e.rect.left)

        # ตรวจผู้เล่นกับศัตรูทุกตัว
        for enemy in enemies:
            self.checks += 1
            self.AABB(player, enemy)

        # ตรวจเฉพาะศัตรูที่มีโอกาสชนกันหลังจากเรียงลำดับแล้ว
        for i in range(num_enemies):
            for j in range(i + 1, num_enemies):
                # ถ้าศัตรูตัวถัดไปอยู่เลยขอบขวาของตัวปัจจุบันไปแล้ว
                # แปลว่าไม่มีทางชนกันบนแกน X จึงหยุดตรวจต่อได้ทันที
                if enemies[j].rect.left > enemies[i].rect.right:
                    break  
                self.checks += 1
                self.AABB(enemies[i], enemies[j])