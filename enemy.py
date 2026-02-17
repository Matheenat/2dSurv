import pygame 
import math
from typing import TypedDict
import constant_value 
from sprites import sprite_loader 

class enemy_config(TypedDict):
    Max_HP : int
    Speed : int
    Sprite : str
        
class enemy(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, sprite_loader, config_data: enemy_config):
