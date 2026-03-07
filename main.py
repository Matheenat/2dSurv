import pygame
from scene_manager import SceneManager
from menu_scene import MenuScene
from play_scene import PlayScene
from transition import FadeTransition


pygame.init()


def main():
    screen = pygame.display.set_mode((1408, 896))
    pygame.display.set_caption("Mini Survivors")
    clock = pygame.time.Clock()

    transition = FadeTransition(screen, duration=600)

    current_scene = {"name": "menu"}
    manager = None

    def change_scene(scene_name):
        nonlocal manager

        if scene_name == "menu":
            manager.set_scene(MenuScene(screen, clock, change_scene, transition))
            transition.start(mode="in")

        elif scene_name == "play":
            manager.set_scene(PlayScene(screen, clock, change_scene, transition))

    first_scene = MenuScene(screen, clock, change_scene, transition)
    manager = SceneManager(first_scene)

    running = True
    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        manager.handle_events(events)
        manager.update()
        manager.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()