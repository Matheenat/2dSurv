import pygame
import math

class Background:
    def __init__(self, tile_size=64):
        self.tile_size = tile_size
        self.color1 = (40, 40, 40)
        self.color2 = (55, 55, 55)

    def draw(self, screen, cam_x, cam_y):
        w, h = screen.get_size()
        ts = self.tile_size

        # กล้องอยู่ที่ cam_x, cam_y (เป็น offset ที่ใช้ลบตอนวาด sprite)
        # หา "ช่วงของ tile ในโลก" ที่ครอบคลุมหน้าจอ
        left_world   = cam_x
        top_world    = cam_y
        right_world  = cam_x + w
        bottom_world = cam_y + h

        start_tx = math.floor(left_world / ts) - 1
        end_tx   = math.floor(right_world / ts) + 1
        start_ty = math.floor(top_world / ts) - 1
        end_ty   = math.floor(bottom_world / ts) + 1

        for tx in range(start_tx, end_tx + 1):
            for ty in range(start_ty, end_ty + 1):
                world_x = tx * ts
                world_y = ty * ts

                # แปลง world -> screen
                screen_x = world_x - cam_x
                screen_y = world_y - cam_y

                rect = pygame.Rect(screen_x, screen_y, ts, ts)
                color = self.color1 if (tx + ty) % 2 == 0 else self.color2
                pygame.draw.rect(screen, color, rect)