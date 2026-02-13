import pygame # type: ignore
import math
from typing import TypedDict
import constant_value # type: ignore
from sprites import sprite_loader # type: ignore
from enum import Enum, auto
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
        
        screen = self.config.get("screen", {})
        centerX = screen.get("width")/2
        centerY = screen.get("height")/2
        self.rect = self.image.get_rect(centerX, centerY)

        self.pos = pygame.math.Vector2(self.rect(centerX, centerY))
        self.direction = pygame.math.Vector2(0, 0)
        
        stats = self.config.get("player_settings",{})
        sprite_name = stats.get("sprite", "hero.png")
        self.image = sprite_loader.load(sprite_name, scale=True)
        self.facing = 'left'
        self.max_hp = stats.get("max_hp", 100)
        self.speed = stats.get("speed", 5)

    def flip_image(self):
        self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)

    def handle_inputs(self):
         key = pygame.key.get_pressed()
         self.direction.update(0, 0)