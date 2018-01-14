import pygame as pg
import random
from os import path

vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# game settings
WIDTH = 1280   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 720  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "SPACE SHOOTER"
BGCOLOR = BLACK
BG = 'SS/img/spacebackground.jpg'
BACKGROUNDIMAGE = pg.image.load(BG).convert_alpha()
BACKGROUNDIMAGE = pg.transform.scale(BACKGROUNDIMAGE, (1280, 720))
DONE = True

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'wall.png'

# player setings
PLAYER_HEALTH = 100
PLAYER_SPEED = 375
PLAYER_ROT_SPEED = 300
PLAYER_IMG = 'spaceship.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(35, 0)

#shoot settings
BULLET_IMG = 'bullet.png'
BULLET_SPEED = 550
BULLET_LIFETIME = 2750
BULLET_RATE = 235
BULLET_DAMAGE = 25


# mob settings
MOB_IMG = 'asteroid.png'
MOB_SPEED = random.randrange(100, 250)
MOB_HIT_RECT = pg.Rect(0, 0, 50, 50)
MOB_HEALTH = 100
MOB_DAMAGE = 25
MOB_KNOCKBACK = 20
MOB_SCORE = 50


# sounds
BG_MUSIC = 'music.mp3'
SHOOT_SOUND = ['Laser_Shoot11.wav']
MOB_HIT_SOUND = ['Explosion4.wav']


