import enum
import pygame  # type: ignore
import math
from typing import TypedDict
import constant_value 
from sprites import sprite_loader 
from enum import Enum, auto
import random

class EnemyState(Enum):
    Idle = auto()
    Chase = auto()
    
class enemy_config(TypedDict):
    Max_HP : int
    Speed : int
    Sprite : str
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, sprite_loader, config_data: enemy_config):
        super().__init__()
        self.config = config_data
        self.screen = screen

        screen_data = self.config.get("screen", {"width": 1280, "height": 800})
        width = screen_data['width']
        height = screen_data['height']

        data = self.config.get("enemy_setting",{})
        sprite_name = data.get("sprite", "enemy/slime.png")
        self.image = sprite_loader.load(sprite_name, scale=True)

        screen_cfg = self.config.get("screen", {})

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(0, height - self.rect.height)

        self.state = random.choice([EnemyState.Idle, EnemyState.Chase])

        self.speed = data.get("Speed", 2)
        self.direction = pygame.math.Vector2(0, 0)
    
    def update(self, player_pos):
        if self.state == EnemyState.Chase:
            enemy_vec = pygame.math.Vector2(self.rect.center)
            player_vec = pygame.math.Vector2(player_pos)

            if enemy_vec.distance_to(player_vec) > 5:
                self.direction = (player_vec - enemy_vec).normalize()
                self.rect.x += self.direction.x * self.speed
                self.rect.y += self.direction.y * self.speed
        else:
            pass