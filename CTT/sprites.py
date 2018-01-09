# Sprite classes for platform game
import pygame as pg
from CTT.settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.sprites_left = pg.image.load("CTT/sprites/player_l.png")
        self.sprites_idle = pg.image.load("CTT/sprites/player_idle.png")
        self.sprites_right = pg.image.load("CTT/sprites/player_r.png")
        self.sprites_jump = pg.image.load("CTT/sprites/player_jump.png")

        self.game = game
        self.image = self.sprites_idle
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 1.5)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.land = False

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP


    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.image = self.sprites_right
        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            self.image = self.sprites_left
        else:
            self.image = self.sprites_idle


        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
    def __init__(self, rotation, y, Color):
        pg.sprite.Sprite.__init__(self)
        self.rotation = rotation
        self.color = Color

        self.y = y


        # Add some offset to make platforms line up with tower
        self.offset = 40


        # Lookup Right Coord from table
        self.lookup = Platform_3D_Array[self.rotation]

        x = self.lookup[0] + self.offset
        w = (self.lookup[1] + self.offset) - (self.lookup[0] + self.offset)
        h = 20

        self.image = pg.Surface((w, h))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Done

        self.rot = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.rot.x = self.rotation



    def update(self):
        self.acc = vec(0, 0)

        self.y = self.rect.y

        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = -PLAYER_ACC / 10
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = PLAYER_ACC / 10

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # equations of motion
        self.vel += self.acc
        self.rot += self.vel + 0.5 * self.acc

        # Make sure that image is not out of bounds
        if self.rot.x > 208:
            self.rot.x += -208
        if self.rot.x < 1:
            self.rot.x += 208

        self.rotation = int(self.rot.x)

        # Lookup Right Coord from table
        self.lookup = Platform_3D_Array[self.rotation]

        x = self.lookup[0] + self.offset
        w = (self.lookup[1] + self.offset) - (self.lookup[0] + self.offset)
        h = 30

        self.image = pg.Surface((w, h))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = self.y
        # Done

        pg.display.set_caption("Vel: " + str(self.vel.x) + " - Acc: " + str(self.acc.x))




class Tower(pg.sprite.Sprite):
    def __init__(self, sprites, rotation, column):
        pg.sprite.Sprite.__init__(self)
        self.rotation = rotation
        self.sprites = sprites

        self.image = self.sprites[self.rotation]
        self.rect = self.image.get_rect()
        self.rect.centerx = (WIDTH / 2)
        self.rect.y = HEIGHT - 65 * column

        self.rot = vec(0, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.rot.x = self.rotation



    def update(self):
        self.acc = vec(0, 0)

        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = -PLAYER_ACC/10
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = PLAYER_ACC/10

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # equations of motion
        self.vel += self.acc
        self.rot += self.vel + 0.5 * self.acc

        # Make sure that image is not out of bounds
        if self.rot.x > 361:
            self.rot.x += -360
        if self.rot.x < 1:
            self.rot.x += 360


        self.rotation = int(self.rot.x)


        self.image = self.sprites[self.rotation]

class Music:
    def __init__(self):
        self.jump1 = pg.mixer.Sound("CTT/assets/jumppp12.ogg")
        self.jump2 = pg.mixer.Sound("CTT/assets/jumppp23.ogg")
        self.land1 = pg.mixer.Sound("CTT/assets/Land1.wav")
        self.land2 = pg.mixer.Sound("CTT/assets/Land1.wav")
        self.land3 = pg.mixer.Sound("CTT/assets/Land1.wav")
        self.land1.set_volume(0.2)

        self.bg = pg.mixer.Sound("CTT/assets/ErrorManagement.ogg")
        self.bg.set_volume(0.02)


