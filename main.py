import os
import pygame  # type: ignore
import math
import json
import user_ui
from player import Player
from sprites import sprite_loader # type: ignore

def main():
    pygame.init()

    with open('config.json','r') as f:
        full_data = json.load(f)

    screen_settings = full_data['screen']
    screen_width = screen_settings['width']
    screen_height = screen_settings['height']

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Survive from Mons Ver0.1")

    clock = pygame.time.Clock()
    game_ui = user_ui.ui(screen, screen_settings)
    
    loader = sprite_loader(full_data['player_sprite'])
    player = Player(screen, loader, full_data)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    running = False
        all_sprites.update()
        screen.fill((30, 30, 30))
        all_sprites.draw(screen)
        
        clock.tick(30)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()