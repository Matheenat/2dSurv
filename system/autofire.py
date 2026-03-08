import pygame
from entities.bullet import Bullet


class AutoFire:
    def __init__(self, bullet_group, all_sprites, config):
        self.bullet_group = bullet_group
        self.all_sprites = all_sprites
        self.config = config

        self.enabled = config.get("enabled", True)
        self.cooldown = config.get("cooldown", 400)
        self.detect_range = config.get("detect_range", 450)

        self.last_shot_time = 0

    def toggle_enabled(self):
        self.enabled = not self.enabled

    def set_enabled(self, value: bool):
        self.enabled = value

    def get_nearest_enemy(self, player_pos, enemy_group):
        nearest_enemy = None
        nearest_distance = self.detect_range

        player_vec = pygame.math.Vector2(player_pos)

        for enemy in enemy_group:
            enemy_vec = pygame.math.Vector2(enemy.rect.center)
            distance = player_vec.distance_to(enemy_vec)

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_enemy = enemy

        return nearest_enemy

    def update(self, player, enemy_group):
        if not self.enabled:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time < self.cooldown:
            return

        target = self.get_nearest_enemy(player.rect.center, enemy_group)
        if target is None:
            return

        bullet = Bullet(player.rect.center, target.rect.center, self.config)
        self.bullet_group.add(bullet)
        self.all_sprites.add(bullet)

        self.last_shot_time = current_time