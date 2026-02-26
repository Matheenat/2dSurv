from .rect import mycustomrect

class CollisionAlgorithm:
    def __init__(self):
        self.checks = 0
    
    def AABB(self, A, B):
        if (A.rect.right > B.rect.left and 
            A.rect.left < B.rect.right and 
            A.rect.bottom > B.rect.top and
            A.rect.top < B.rect.bottom):

            dx = A.rect.centerx - B.rect.centerx
            dy = A.rect.centery - B.rect.centery

            overlapx = ((A.rect.width/2 + B.rect.width/2) - abs(dx))
            overlapy = ((A.rect.height/2 + B.rect.height/2) - abs(dy))

            if overlapx < overlapy:
                if dx > 0: 
                    A.rect.x += overlapx
                else: 
                    A.rect.x -= overlapx
                    
            else:
                if dy > 0:
                    A.rect.y += overlapy
                else: 
                    A.rect.y -= overlapy

            if hasattr(A, 'pos'):
                A.pos.x = A.rect.x
                A.pos.y = A.rect.y
            if hasattr(B, 'pos'):
                B.pos.x = B.rect.x
                B.pos.y = B.rect.y

            return True
        return False
    
    def run(self, player, enemies):
        raise Exception("Forgot to override run()")