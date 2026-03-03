from game import Game
import pygame # type: ignore
def main():
    my_game = Game()
    while my_game.running:
        my_game.handle_events()  
        my_game.update()         
        my_game.draw()

    pygame.quit()

if __name__ == "__main__":
    main()