import pygame
from typing import TypedDict
from enum import Enum, auto
import random
import math

class EnemyState(Enum):
    Idle = auto()
    Chase = auto()

class enemy_config(TypedDict):
    Max_HP: int
    Speed: int
    Sprite: str

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, sprite_loader, config_data: enemy_config, player_pos):
        super().__init__()
        self.config = config_data
        self.screen = screen

        screen_data = self.config.get("screen", {"width": 1280, "height": 768})
        width = screen_data["width"]
        height = screen_data["height"]

        data = self.config.get("enemy_setting", {})
        sprite_name = data.get("sprite", "enemy/slime.png")
        self.image = sprite_loader.load(sprite_name, scale=True)

        spawn_x, spawn_y = self.get_spawn_position(width, height, player_pos)

        self.rect = self.image.get_rect(topleft=(int(spawn_x), int(spawn_y)))

        self.state = EnemyState.Chase
        self.speed = data.get("speed", 1)
        self.damage = data.get("damage",10)
        self.direction = pygame.math.Vector2(0, 0)

    def get_spawn_position(self, width, height, player_pos):
        data = self.config.get("enemy_setting", {})
        margin = data.get("spawn_margin", 120)
        min_distance = data.get("min_spawn_distance", 220)

        player_vec = pygame.math.Vector2(player_pos)

        for _ in range(50):
            side = random.choice(["top", "bottom", "left", "right"])

            if side == "top":
                x = random.randint(0, width - self.image.get_width())
                y = -self.image.get_height() - margin

            elif side == "bottom":
                x = random.randint(0, width - self.image.get_width())
                y = height + margin

            elif side == "left":
                x = -self.image.get_width() - margin
                y = random.randint(0, height - self.image.get_height())

            else:  # right
                x = width + margin
                y = random.randint(0, height - self.image.get_height())

            enemy_center = pygame.math.Vector2(
                x + self.image.get_width() / 2,
                y + self.image.get_height() / 2
            )

            if enemy_center.distance_to(player_vec) >= min_distance:
                return x, y

        return width + margin, random.randint(0, height - self.image.get_height())

    def update(self, player_pos):
        if self.state == EnemyState.Chase:
            enemy_vec = pygame.math.Vector2(self.rect.center)
            player_vec = pygame.math.Vector2(player_pos)

            if enemy_vec.distance_to(player_vec) > 5:
                self.direction = (player_vec - enemy_vec).normalize()
                self.rect.x += int(self.direction.x * self.speed)
                self.rect.y += int(self.direction.y * self.speed)