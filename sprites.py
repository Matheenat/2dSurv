import os
import pygame # type: ignore
import math
import json
from typing import TypedDict
class player():
    class player_sprite_config(TypedDict):
        width: int
        height: int
        scale: int #power of 4 example 4->16->64 , 32 -> 128 -> 256
    
    def __init__(self):
        self.base_dir = os.path.dirname(__file__)
        self.asset_dir = os.path.join(self.base_dir, "assets/sprite")