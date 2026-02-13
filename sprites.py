import os
import pygame # type: ignore
import math
import json
from typing import TypedDict
import constant_value # type: ignore
class sprite_loader_config(TypedDict):
    width: int
    height: int
    scale: int #power of 4 example 4->16->64 , 32 -> 128 -> 256

class sprite_loader(): 
    def __init__(self, config_data: sprite_loader_config):
        self.config = config_data
        self.sprite_dir = os.path.join(constant_value.ASSETS_DIR,"sprite")
        self.ui_scale = config_data.get('scale', 1)
        self.player = self.config.get('player', 1) #todo

        self.cache = {}

    def load(self, filename: str, scale: bool):
        if filename in self.cache:
            return self.cache[filename]
        path = os.path.join(self.sprite_dir,filename)
        try:
            sprite = pygame.image.load(path).convert_alpha()
            if scale and self.ui_scale != 1:
                width = int(sprite.get_width() * self.ui_scale)
                height = int(sprite.get_height() * self.ui_scale)
                sprite = pygame.transform.scale(sprite, (width, height))
                
            self.cache[filename] = sprite
            return sprite       
        
        except pygame.error:
            print(f"path : {path} มีปัญหามาแก้ด่วนๆ")
            placeholder = pygame.Surface((16, 16), pygame.SRCALPHA)
            placeholder.fill((255, 255, 255))
            return placeholder