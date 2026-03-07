import pygame
from typing import TypedDict
from enum import Enum, auto
from system.collision.rect import mycustomrect

class PlayerState(Enum):
    IDLE = auto()
    WALKING = auto()
    ATTACKING = auto()

class player_config(TypedDict):
    Max_HP : int
    Speed : int
    Sprite : str
        
class Player(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, sprite_loader, config_data: player_config):
        super().__init__()
        self.config = config_data
        self.screen = screen

        data = self.config.get("player_settings",{})
        sprite_name = data.get("sprite", "player/hero.png")
        self.image = sprite_loader.load(sprite_name, scale=True)

        centerX = self.screen.get_width() / 2
        centerY = self.screen.get_height() / 2

        self.rect = self.image.get_rect(center=(int(centerX), int(centerY)))
        
        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.vector = pygame.math.Vector2(0, 0)

        self.facing = 'left'
        self.max_hp = data.get("max_hp", 100)
        self.speed = data.get("speed", 5)

    def flip_image(self):
        self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)

    def handle_inputs(self):
        key = pygame.key.get_pressed()
        self.vector.update(0, 0)
        if key[pygame.K_w]: 
            self.vector.y -= 1
        if key[pygame.K_a]: 
            self.vector.x -= 1
        if key[pygame.K_s]: 
            self.vector.y += 1
        if key[pygame.K_d]: 
            self.vector.x += 1

        if self.vector.x > 0 and self.facing == 'right':
            self.facing = 'left'
            self.flip_image()

        elif self.vector.x < 0 and self.facing == 'left':
            self.facing = 'right'
            self.flip_image()

    def update(self):
        self.handle_inputs()
        if self.vector.magnitude() > 0:
            velocity = self.vector.normalize() * self.speed
            self.pos += velocity
            self.current_speed = velocity.magnitude()
        else:
            self.current_speed = 0
        
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)
        