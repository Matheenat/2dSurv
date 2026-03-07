class mycustomrect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

    @property
    def left(self):
        return self.x
    
    @property
    def right(self):
        return self.x + self.width
    
    @property
    def top(self):
        return self.y
    
    @property
    def bottom(self):
        return self.y + self.height
    
    @property
    def centerx(self): 
        return self.x + (self.width / 2)

    @property
    def centery(self): 
        return self.y + (self.height / 2)
    
    @property
    def center(self):
        return (self.x + self.width / 2, self.y + self.height / 2)
    
    @property
    def topleft(self):
        return (self.x, self.y)
    
    @property
    def topright(self):
        return (self.x + self.width, self.y)
    
    @property
    def bottomleft(self):
        return (self.x, self.y + self.height)

    @property
    def bottomright(self):
        return (self.x + self.width, self.y + self.height)
    
    def contains(self, other): #aabb
        return (other.left >= self.left and
                other.right <= self.right and
                other.top >= self.top and
                other.bottom <= self.bottom)
    
    def intersects(self, other):
        return not (other.left > self.right or 
                    other.right < self.left or 
                    other.top > self.bottom or 
                    other.bottom < self.top)