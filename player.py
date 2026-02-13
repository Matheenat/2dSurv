import pygame # type: ignore
import math
from typing import TypedDict
import constant_value # type: ignore
from sprites import sprite_loader # type: ignore
class player_config(TypedDict):
        Max_HP : int
        Speed : int
        Sprite : str
        
class Player(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, sprite_loader, config_data: player_config):
        super().__init__()
        self.config = config_data
        stats = self.config.get("player_settings",{})
        self.max_hp = stats.get("Max_HP", 100)
        self.speed = stats.get("Speed", 5)