This project is a simple 2D survival game built with Python and Pygame.
The main purpose of this project is to test and compare different collision detection algorithms used in games.

Instead of using only one collision detection method, this project allows switching between several algorithms in real time.
This helps demonstrate how different algorithms affect performance, number of collision checks, and overall FPS.

The project is designed not only as a playable game, but also as a testing environment for studying collision detection techniques in game development.

Features
- 2D survival style gameplay
- Multiple enemies spawning and chasing the player
- Automatic shooting system
- Health bar and damage system
- Pause menu
- FPS display and debug information
- Real-time switching between collision detection algorithms

The game also displays useful information for testing:

- Current FPS
- Number of enemies
- Number of collision checks
- Current algorithm being used

Collision Detection Algorithms

This project implements several different collision detection algorithms for comparison:

1. Brute Force
    The simplest method.
    Every object checks collision with every other object.

Advantages
- Easy to implement
Disadvantages
- Very slow when the number of objects increases

2. Nine Neighbor Grid
    The world is divided into grid cells.
    Each object only checks collisions with objects in its own cell and the surrounding cells.

Advantages
- Reduces unnecessary collision checks
Disadvantages
- Performance depends on grid size

3. Offset Grid
    A variation of the grid system that helps distribute objects more evenly across grid cells.

Advantages
- Reduces collision checks further in some cases

4. QuadTree
    A hierarchical spatial partitioning structure that divides space into smaller regions.

Advantages
- Efficient when there are many objects
Disadvantages
- More complex to implement

5. Sweep and Prune
    Objects are sorted along an axis, and collision checks are performed only for objects that overlap along that axis.

Advantages
- Very efficient when objects move smoothly

--------------------------Controls--------------------------
Key	                        Action
WASD	                    Move player
ESC	                        Pause / Resume
F11	                        Toggle fullscreen
1	                        Use Brute Force
2	                        Use Nine Neighbor
3	                        Use Grid
4	                        Use QuadTree
5	                        Use Sweep and Prune
P                           disable auto-fire
G                           turn on god mode
F1                          toggle debug

How to Run

1. Install Python (3.x recommended)
2. Install pygame
	-> pip install pygame
3. Run the game
	-> python main.py

Project Structure
core/        # Main game systems
entities/    # Game objects (player, enemy, bullets)
systems/     # Gameplay systems (collision, spawning, etc.)
scene/       # Game scenes
ui/          # UI elements
utils/       # Helper utilities
assets/      # Game images and fonts

Purpose of the Project
The goal of this project is to study how different collision detection algorithms behave in a real game scenario.

By switching between algorithms during gameplay, we can observe:
- Performance differences
- Collision check counts
- Impact on FPS

This helps understand which algorithm is more suitable depending on the number of objects in the game.