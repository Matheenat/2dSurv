import pygame # type: ignore
import json
import user_ui
from player import Player
from sprites import sprite_loader 
from camera import CameraGroup 
import random
from enemy import Enemy
from collision.rect import mycustomrect
from collision.collision_manager import CollisionManager

def main():
    pygame.init()

    with open('config.json','r') as f:
        full_data = json.load(f)

    screen_settings = full_data['screen']
    screen_width = screen_settings['width']
    screen_height = screen_settings['height']

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Survive from Mons Ver0.2")

    clock = pygame.time.Clock()
    game_ui = user_ui.ui(screen, screen_settings)
    
    loader = sprite_loader(full_data['player_sprite'])
    player = Player(screen, loader, full_data)

    all_sprites = CameraGroup()
    all_sprites.add(player)

    num_enemies = 100
    enemy_group = pygame.sprite.Group()
    spawn_delay = 50
    last_spawn_time = pygame.time.get_ticks()

    col_manager = CollisionManager()

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    running = False

        current_time = pygame.time.get_ticks()
        if len(enemy_group) < num_enemies:
            if current_time - last_spawn_time > spawn_delay:
                new_enemy = Enemy(screen, loader, full_data)
                enemy_group.add(new_enemy)
                all_sprites.add(new_enemy)

                last_spawn_time = current_time

        player.update()
        enemy_group.update(player.pos)
        col_manager.update(player, enemy_group)

        screen.fill((0, 0, 0))
        all_sprites.custom_draw(player)
        
        if full_data['debug']['speed'] == "True":
            game_ui.draw_debug(screen, "speed", player.current_speed, (1,screen_width/2))

        if full_data['debug']['checks'] == "True":
            game_ui.draw_debug(screen, "checks", col_manager.get_checks(), (1,(screen_width/2) + 5))

        clock.tick(60) / 1000 #seconds

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()