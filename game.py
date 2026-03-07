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
from background import Background
from autofire import AutoFire

class Game:
    def __init__(self):
        pygame.init()
        with open('config.json', 'r') as f:
            self.data = json.load(f)
        
        self.screen_width = self.data['screen']['width']
        self.screen_height = self.data['screen']['height']
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Survive from Mons Ver0.3")
        
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = CameraGroup()
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.col_manager = CollisionManager()
        self.ui = user_ui.ui(self.screen, self.data['screen'], self.data['debug'])

        self.loader = sprite_loader(self.data['player_sprite'])
        self.player = Player(self.screen, self.loader, self.data)
        self.all_sprites.add(self.player)

        self.spawn_delay = 200
        self.last_spawn_time = pygame.time.get_ticks()
        self.num_enemies = self.data['enemy_setting']['enemy_limit']

        self.background = Background(64)

        self.autofire = AutoFire(self.bullet_group,self.all_sprites,self.data.get("autofire", {})
)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    new_enemy = Enemy(self.screen, self.loader, self.data)
                    self.all_sprites.add(new_enemy)
                    self.enemy_group.add(new_enemy)

            self.col_manager.input_handle(event)
    
    def spawn_enemies(self):
        current_time = pygame.time.get_ticks()

        if len(self.enemy_group) < self.num_enemies:
            if current_time - self.last_spawn_time > self.spawn_delay:
                new_enemy = Enemy(self.screen, self.loader, self.data)
                self.enemy_group.add(new_enemy)
                self.all_sprites.add(new_enemy)
                self.last_spawn_time = current_time

    def update(self):
        self.camera_rectx = self.all_sprites.offset.x
        self.camera_recty = self.all_sprites.offset.y
        self.screen_rect = mycustomrect(self.camera_rectx, self.camera_recty, self.screen_width, self.screen_height)

        self.player.update()
        self.enemy_group.update(self.player.pos)

        self.autofire.update(self.player, self.enemy_group)

        self.bullet_group.update()

        hits = pygame.sprite.groupcollide(self.bullet_group, self.enemy_group, True, True)

        self.col_manager.update(self.player, self.enemy_group, self.screen_rect)
        self.spawn_enemies()
        self.all_sprites.center_target_camera(self.player)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.background.draw(self.screen, self.all_sprites.offset.x, self.all_sprites.offset.y)
        self.all_sprites.custom_draw(self.player)

        fps = self.clock.get_fps()
        camera_offset = self.all_sprites.offset
        self.ui.draw_all_debug(self.player, self.col_manager, self.enemy_group, fps, camera_offset)