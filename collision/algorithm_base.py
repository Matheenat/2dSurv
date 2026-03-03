from .rect import mycustomrect

class CollisionAlgorithm:
    def __init__(self):
        self.checks = 0
    
    def AABB(self, A, B, player=None):
        if (A.rect.right > B.rect.left and 
            A.rect.left < B.rect.right and 
            A.rect.bottom > B.rect.top and
            A.rect.top < B.rect.bottom):

            dx = A.rect.centerx - B.rect.centerx
            dy = A.rect.centery - B.rect.centery

            overlapx = ((A.rect.width/2 + B.rect.width/2) - abs(dx))
            overlapy = ((A.rect.height/2 + B.rect.height/2) - abs(dy))

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

            for obj in [A, B]:
                if hasattr(obj, 'pos'):
                    obj.pos.x, obj.pos.y = obj.rect.x, obj.rect.y

            return True
        return False
    
    def run(self, player, enemies):
        raise Exception("Forgot to override run()")