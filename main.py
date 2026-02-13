import os
import pygame  # type: ignore
import math
import json
import user_ui

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

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    running = False

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()