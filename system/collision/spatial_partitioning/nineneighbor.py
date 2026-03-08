from .grid import Grid

class NineNeighbor(Grid):
    def __init__(self):
        super().__init__()

    def run(self, player, enemies, screen_rect):
        # ลงทะเบียนศัตรูทั้งหมดลงใน grid
        self.register(player, enemies, 0)
        self.checks = 0
        playerX, playerY = self.player_coord
        
        # ตรวจการชนกันภายใน cell เดียวกันก่อน
        for (x,y) in self.grid.keys():
            current_cell = self.grid[(x,y)]
            for i in range(len(current_cell)):
                for j in range(i + 1, len(current_cell)):
                    self.checks += 1
                    self.AABB(current_cell[i], current_cell[j])
        
            # ตรวจ cell ข้างเคียงบางทิศ เพื่อไม่ให้เช็กคู่เดิมซ้ำ
            for dx, dy in [(1, 0), (1, 1), (0, 1), (-1, 1)]:
                neighbor_cell = self.grid.get((x + dx, y + dy))
                if neighbor_cell:
                    for enemyA in current_cell:
                        for enemyB in neighbor_cell:
                            self.checks += 1
                            self.AABB(enemyA, enemyB)
        
        # ตรวจผู้เล่นกับศัตรูใน 9 ช่องรอบตัวผู้เล่น
        # (ช่องตัวเอง + ช่องข้างเคียงอีก 8 ช่อง)
        for dx in range(-1,2):
            for dy in range(-1,2):
                target_cell = self.grid.get((dx + playerX, dy + playerY))
                if target_cell:
                    for enemy in target_cell:
                        self.checks += 1
                        self.AABB(player, enemy)