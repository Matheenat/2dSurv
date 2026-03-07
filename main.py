import pygame
from scene_manager import SceneManager
from menu_scene import MenuScene
from play_scene import PlayScene
from transition import FadeTransition

pygame.init()


def main():
    screen_width = 1408
    screen_height = 896

    is_fullscreen = False
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("2D Survival")
    clock = pygame.time.Clock()

    transition = FadeTransition(screen, duration=600)
    manager = None

    def toggle_fullscreen():
        nonlocal screen, is_fullscreen, transition, manager

        is_fullscreen = not is_fullscreen

        if is_fullscreen:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((screen_width, screen_height))

        transition.screen = screen
        transition.overlay = pygame.Surface(screen.get_size())
        transition.overlay.fill((0, 0, 0))

        manager.scene.screen = screen

        if hasattr(manager.scene, "game"):
            manager.scene.game.screen = screen

        if hasattr(manager.scene, "on_resize"):
            manager.scene.on_resize()

    def change_scene(scene_name):
        nonlocal manager, screen

        if scene_name == "menu":
            manager.set_scene(
                MenuScene(
                    screen,
                    clock,
                    change_scene,
                    transition,
                    toggle_fullscreen,
                    lambda: is_fullscreen
                )
            )
            transition.start(mode="in")

        elif scene_name == "play":
            manager.set_scene(
                PlayScene(
                    screen,
                    clock,
                    change_scene,
                    transition
                )
            )

    first_scene = MenuScene(
        screen,
        clock,
        change_scene,
        transition,
        toggle_fullscreen,
        lambda: is_fullscreen
    )
    manager = SceneManager(first_scene)

    running = True
    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    toggle_fullscreen()

        manager.handle_events(events)
        manager.update()
        manager.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()