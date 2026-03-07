import pygame
import json
import UI.user_ui as user_ui
from entities.player import Player
from utils.sprites import sprite_loader
from core.camera import CameraGroup
from entities.enemy import Enemy
from system.collision.rect import mycustomrect
from system.collision.collision_manager import CollisionManager
from system.background import Background
from system.autofire import AutoFire
import core.constant_value as constant_value
from UI.game_over_ui import GameOverUI
from UI.health_bar_ui import HealthBarUI
from UI.damage_number_manager import DamageNumberManager

class Game:
    def __init__(self, screen, clock):
        with open(constant_value.CONFIG_PATH, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.screen = screen
        self.clock = clock
        self.running = True

        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        pygame.display.set_caption("Survive from Mons Ver0.3")

        self.all_sprites = CameraGroup()
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.col_manager = CollisionManager()

        screen_cfg = dict(self.data['screen'])
        screen_cfg["width"] = self.screen_width
        screen_cfg["height"] = self.screen_height

        self.ui = user_ui.ui(self.screen, screen_cfg, self.data['debug'])

        self.loader = sprite_loader(self.data['player_sprite'])
        self.player = Player(self.screen, self.loader, self.data)
        self.all_sprites.add(self.player)

        self.spawn_delay = 200
        self.last_spawn_time = pygame.time.get_ticks()
        self.num_enemies = self.data['enemy_setting']['enemy_limit']

        self.background = Background(64)

        self.autofire = AutoFire(self.bullet_group,self.all_sprites,self.data.get("autofire", {}))

        self.game_over = False
        self.game_over_ui = GameOverUI()

        self.health_bar_ui = HealthBarUI(self.ui.fonts['ui'])
        self.damage_number_manager = DamageNumberManager(self.ui.fonts['ui'])
        self.damage_flash_timer = 0
        self.damage_flash_duration = 150

    def on_resize(self, new_screen):
        self.screen = new_screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.ui.screen = self.screen
        self.ui.screen_width = self.screen_width
        self.ui.screen_height = self.screen_height

        self.all_sprites.refresh_display_size()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    for _ in range(10):
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
        self.screen_rect = mycustomrect(self.camera_rectx,self.camera_recty,self.screen_width,self.screen_height)

        if self.game_over:
            self.all_sprites.center_target_camera(self.player)
            self.damage_number_manager.update(16)
            self.health_bar_ui.update(16,self.player.health.hp,self.player.health.max_hp)
            return

        self.player.update()
        self.enemy_group.update(self.player.pos)

        self.autofire.update(self.player, self.enemy_group)
        self.bullet_group.update()

        pygame.sprite.groupcollide(self.bullet_group, self.enemy_group, True, True)

        self.check_player_enemy_collision()

        if self.player.health.dead:
            self.game_over = True

        self.col_manager.update(self.player, self.enemy_group, self.screen_rect)
        self.spawn_enemies()
        self.all_sprites.center_target_camera(self.player)

        self.damage_number_manager.update(16)
        self.health_bar_ui.update(16,self.player.health.hp,self.player.health.max_hp)

        if self.damage_flash_timer > 0:
            self.damage_flash_timer -= 16
            if self.damage_flash_timer < 0:
                self.damage_flash_timer = 0

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.background.draw(self.screen, self.all_sprites.offset.x, self.all_sprites.offset.y)
        self.all_sprites.custom_draw(self.player)

        fps = self.clock.get_fps()
        camera_offset = self.all_sprites.offset
        self.ui.draw_all_debug(self.player, self.col_manager, self.enemy_group, fps, camera_offset)

        self.health_bar_ui.draw(self.screen,self.player.health.hp,self.player.health.max_hp)

        self.damage_number_manager.draw(self.screen, self.all_sprites.offset)

        if self.damage_flash_timer > 0:
            alpha_ratio = self.damage_flash_timer / self.damage_flash_duration
            alpha = int(90 * alpha_ratio)

            flash = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            flash.fill((255, 0, 0, alpha))
            self.screen.blit(flash, (0, 0))

        if self.game_over:
            self.game_over_ui.draw(self.screen)

    def check_player_enemy_collision(self):
        if self.player.health.dead:
            return

        hit_enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)
        if hit_enemy:
            did_take = self.player.health.take_damage(hit_enemy.damage)

            if did_take:
                self.damage_flash_timer = self.damage_flash_duration

                self.damage_number_manager.spawn(
                    self.player.rect.centerx,
                    self.player.rect.top - 10,
                    hit_enemy.damage
                )
        