import pygame # type: ignore
import json
import user_ui
from player import Player
from sprites import sprite_loader 
from camera import CameraGroup 
import random
from enemy import Enemy

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
    # print(f"Rect Width: {player.rect.width}")
    # print(f"Rect Height: {player.rect.height}")
    # print(f"Image Width: {player.image.get_width()}")

    all_sprites = CameraGroup()
    all_sprites.add(player)

    # for i in range(20):
    #     random_x = random.randint(-1000, 1000)
    #     random_y = random.randint(-1000, 1000)
        
    #     test_sprite = pygame.sprite.Sprite(all_sprites)
    #     test_sprite.image = pygame.Surface((50, 50))
    #     test_sprite.image.fill((100, 100, 100))
    #     test_sprite.rect = test_sprite.image.get_rect(center=(random_x, random_y))
    num_enemies = 50 
    enemy_group = pygame.sprite.Group()
    for i in range(num_enemies):
        new_enemy = Enemy(screen, loader, full_data)
        enemy_group.add(new_enemy)
        all_sprites.add(new_enemy)

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    running = False

        player.update()
        enemy_group.update(player.pos)

        screen.fill((0, 0, 0))
        all_sprites.custom_draw(player)
        
        if full_data['debug']['speed'] == "True":
            game_ui.draw_debug(screen, "speed", player.current_speed, (1,screen_width/2))

        clock.tick(60) / 1000 #seconds

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()