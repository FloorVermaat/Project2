# game options/settings
from CTT.platforms import *
TITLE = "Jump"
WIDTH = 1280
HEIGHT = 720
FPS = 60
FONT_NAME = 'arial'

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.05
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# Starting platforms
#PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
#                 (WIDTH / 2 - 250, HEIGHT * 3 / 4, 500, 20),
#                 (125, HEIGHT - 350, 100, 20),
#                 (350, 200, 100, 20),
#                 (175, 100, 50, 20)]

PLATFORM_LIST = [(100, HEIGHT - 20), (45, HEIGHT - 200), (200, HEIGHT - 350), (28, HEIGHT - 450), (45, HEIGHT - 660)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = BLACK

PLATFORMS = 6