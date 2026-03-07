import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, config):
        super().__init__()

        size = config.get("bullet_size", 10)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 220, 80), (size // 2, size // 2), size // 2)

        self.rect = self.image.get_rect(center=(int(start_pos[0]), int(start_pos[1])))
        self.pos = pygame.math.Vector2(self.rect.center)

        self.speed = config.get("bullet_speed", 14)
        self.damage = config.get("bullet_damage", 1)
        self.lifetime = config.get("bullet_lifetime", 50)
        self.age = 0

        direction = pygame.math.Vector2(target_pos) - pygame.math.Vector2(start_pos)
        if direction.length() == 0:
            direction = pygame.math.Vector2(1, 0)

        self.direction = direction.normalize()

    def update(self):
        self.pos += self.direction * self.speed
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        self.age += 1
        if self.age >= self.lifetime:
            self.kill()