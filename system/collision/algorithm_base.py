from .rect import mycustomrect

class CollisionAlgorithm:
    def __init__(self):
        self.checks = 0
    
    def AABB(self, A, B, player=None):
        # ตรวจสอบก่อนว่า rect ของวัตถุ A และ B ซ้อนทับกันหรือไม่
        # โดยเช็กแยกตามแกน X และแกน Y
        if (A.rect.right > B.rect.left and 
            A.rect.left < B.rect.right and 
            A.rect.bottom > B.rect.top and
            A.rect.top < B.rect.bottom):

            # คำนวณระยะห่างของจุดศูนย์กลางบนแกน X และ Y
            dx = A.rect.centerx - B.rect.centerx
            dy = A.rect.centery - B.rect.centery

            # คำนวณระยะ overlap บนแกน X และ Y
            # ใช้เพื่อดูว่าควรดันวัตถุออกจากกันในแกนไหน
            overlapx = ((A.rect.width/2 + B.rect.width/2) - abs(dx))
            overlapy = ((A.rect.height/2 + B.rect.height/2) - abs(dy))


            # ถ้า overlap แกน X น้อยกว่าแกน Y
            # แปลว่าชนกันตื้นกว่าทางแกน X จึงแก้การชนด้วยการดันในแกน X
            if overlapx < overlapy:
                if A is player:
                    B.rect.x -= overlapx if dx > 0 else -overlapx
                elif B is player:
                    A.rect.x += overlapx if dx > 0 else -overlapx
                else:
                    push = overlapx / 2
                    change = push if dx > 0 else -push
                    A.rect.x += change
                    B.rect.x -= change
            # ถ้า overlap แกน Y น้อยกว่าหรือเท่ากัน
            # ให้แก้การชนด้วยการดันในแกน Y
            else:
                if A is player:
                    B.rect.y -= overlapy if dy > 0 else -overlapy
                elif B is player:
                    A.rect.y += overlapy if dy > 0 else -overlapy
                else:
                    push = overlapy / 2
                    change = push if dy > 0 else -push
                    A.rect.y += change
                    B.rect.y -= change

            # อัปเดตตำแหน่งจริงของ object ให้ตรงกับ rect หลังแก้ collision
            for obj in [A, B]:
                if hasattr(obj, 'pos'):
                    obj.pos.x, obj.pos.y = obj.rect.x, obj.rect.y

            return True
        return False
    
    def run(self, player, enemies, screen_rect):
        raise Exception("Forgot to override run()")