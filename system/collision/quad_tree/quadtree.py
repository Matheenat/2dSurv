from system.collision.algorithm_base import CollisionAlgorithm
from .node import Node

class QuadTree(CollisionAlgorithm):
    def __init__(self, screen_rect, max_depth = 7, capacity = 3):
        super().__init__()
        self.screen = screen_rect
        self.max_depth = max_depth
        self.capacity = capacity
      
    def run(self, player, enemies_group, current_screen_rect):
        self.checks = 0
        self.screen = current_screen_rect
        enemies = enemies_group.sprites()
        self.root = Node(self.screen, depth=0, max_depth=self.max_depth, capacity=self.capacity)

        self.root.insert(player)
        for enemy in enemies:
            self.root.insert(enemy)

        player_potential_hit = self.root.query(player.rect)
        for other in player_potential_hit:
            if other is not player:
                self.checks += 1
                self.AABB(player, other)

        checked_pair = set()
        for enemy in enemies:
            potential_neighbors = self.root.query(enemy.rect)
            for neighbor in potential_neighbors:
                if neighbor is enemy or neighbor is player:
                    continue

                pair = tuple(sorted((id(enemy), id(neighbor))))
                if pair not in checked_pair:
                    self.checks += 1
                    self.AABB(enemy, neighbor)
                    checked_pair.add(pair)