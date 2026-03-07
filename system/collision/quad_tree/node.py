from system.collision.rect import mycustomrect
import pygame
class Node:
    def __init__(self, screen, depth = 0, max_depth = 7, capacity = 3):
        self.rect = screen
        self.objects = []
        self.children = []
        self.depth = depth
        self.max_depth = max_depth
        self.capacity = capacity
        self.divided = False

    def split(self):
        height = self.rect.height
        width = self.rect.width
        h_height = height/2
        h_width = width/2

        NW = mycustomrect(self.rect.x, self.rect.y, h_width, h_height)
        NE = mycustomrect(self.rect.x + h_width, self.rect.y, h_width, h_height)
        SW = mycustomrect(self.rect.x, self.rect.y + h_height, h_width, h_height)
        SE = mycustomrect(self.rect.x + h_width, self.rect.y + h_height, h_width, h_height)

        self.children.append(Node(NW, self.depth + 1))
        self.children.append(Node(NE, self.depth + 1))
        self.children.append(Node(SW, self.depth + 1))
        self.children.append(Node(SE, self.depth + 1))

        self.divided = True
    
    def insert(self, object):
        if not self.rect.intersects(object.rect):
            return False
        
        if self.depth < self.max_depth:

            if len(self.objects) < self.capacity and not self.divided:
                self.objects.append(object)
                return True
            
            if not self.divided:
                self.split()

        for child in self.children:
            if child.insert(object):
                return True
            
        self.objects.append(object)
        return True
        
    
    def query(self, object):
        found = []

        if not self.rect.intersects(object):
            return found
        
        for obj in self.objects:
            found.append(obj)

        if self.divided:
            for child in self.children:
                found.extend(child.query(object))

        return found
    
    def draw_debug(self, screen, camera_offset):
        rect_to_draw = pygame.Rect(
            self.rect.x - camera_offset.x,
            self.rect.y - camera_offset.y,
            self.rect.width,
            self.rect.height
        )
        pygame.draw.rect(screen, (0, 255, 0), rect_to_draw, 1)

        if self.divided:
            for child in self.children:
                child.draw_debug(screen, camera_offset)