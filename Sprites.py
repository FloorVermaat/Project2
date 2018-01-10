from settings import *
import pygame as pg
import pygame as pygame
vec = pygame.math.Vector2

class BlitzPlanet(pg.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pg.image.load(os.path.join(img_folder, "blitz planet.png")).convert_alpha()
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = W - 300
        self.rect.y = H - 250
        self.rot = 0
        self.rot_speed = 5
        self.last_update = pygame.time.get_ticks()
        self.active = False
        self.sizex = 120
        self.sizey = 120

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = self.rot + self.rot_speed
            if self.rot >= 360:
                self.rot = 1
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        if self.active:
            if self.sizex < 180:
                self.sizex += 5
            if self.sizey < 180:
                self.sizey += 5
            self.image = pygame.transform.scale(self.image, (self.sizex, self.sizey))


class ClimbPlanet(pg.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, "Climb planet2.png")).convert_alpha()
        self.image_orig = self.image.copy()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 100
        self.rect.y = 100
        self.rot = 0
        self.rot_speed = 5
        self.last_update = pygame.time.get_ticks()
        self.active = False
        self.sizex = 120
        self.sizey = 120

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = self.rot + self.rot_speed
            if self.rot >= 360:
                self.rot = 1
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        if self.active:
            if self.sizex < 180:
                self.sizex += 5
            if self.sizey < 180:
                self.sizey += 5
            self.image = pygame.transform.scale(self.image, (self.sizex, self.sizey))


class RacePlanet(pg.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, "Race planet.png")).convert_alpha()
        self.image_orig = self.image.copy()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = W - 200
        self.rect.y = 100
        self.rot = 0
        self.rot_speed = 5
        self.last_update = pygame.time.get_ticks()
        self.active = False
        self.sizex = 120
        self.sizey = 120

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = self.rot + self.rot_speed
            if self.rot >= 360:
                self.rot = 1
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        if self.active:
            if self.sizex < 180:
                self.sizex += 5
            if self.sizey < 180:
                self.sizey += 5
            self.image = pygame.transform.scale(self.image, (self.sizex, self.sizey))


class ShootPlanet(pg.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, "Shoot planet.png")).convert_alpha()
        self.image_orig = self.image.copy()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 300
        self.rect.y = H / 2 - 30
        self.rot = 0
        self.rot_speed = 5
        self.last_update = pygame.time.get_ticks()
        self.active = False
        self.sizex = 120
        self.sizey = 120

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = self.rot + self.rot_speed
            if self.rot >= 360:
                self.rot = 1
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        if self.active:
            if self.sizex < 180:
                self.sizex += 5
            if self.sizey < 180:
                self.sizey += 5
            self.image = pygame.transform.scale(self.image, (self.sizex, self.sizey))


class EvadePlanet(pg.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, "Evade planet.png")).convert_alpha()
        self.image_orig = self.image.copy()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = W / 2
        self.rect.y = 150
        self.rot = 0
        self.rot_speed = 5
        self.last_update = pygame.time.get_ticks()
        self.active = False
        self.sizex = 120
        self.sizey = 120

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = self.rot + self.rot_speed
            if self.rot >= 360:
                self.rot = 1
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        if self.active:
            if self.sizex < 180:
                self.sizex += 5
            if self.sizey < 180:
                self.sizey += 5
            self.image = pygame.transform.scale(self.image, (self.sizex, self.sizey))


class ExitPlanet(pg.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(img_folder, "Exit planet.png")).convert_alpha()
        self.image_orig = self.image.copy()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 50
        self.rect.y = H - 200
        self.rot = 0
        self.rot_speed = 5
        self.last_update = pygame.time.get_ticks()
        self.active = False
        self.sizex = 120
        self.sizey = 120

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = self.rot + self.rot_speed
            if self.rot >= 360:
                self.rot = 1
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        if self.active:
            if self.sizex < 180:
                self.sizex += 5
            if self.sizey < 180:
                self.sizey += 5
            self.image = pygame.transform.scale(self.image, (self.sizex, self.sizey))


class Background(object):
    def __init__(self):
        self.image_orig = pygame.image.load(os.path.join(img_folder, "spacebackground.png")).convert()
        self.image = self.image_orig.copy()
        self.image.get_rect()
        self.y = 720
        self.rel_y = 0
        self.rect = self.image.get_rect()
        self.speed = 0
        self.speed_regulator = True
        self.rot = 0
        self.rot_speed = 0.5
        self.last_update = pygame.time.get_ticks()
        self.rect.center = [640, 360]

    def draw(self, surface, speed):
        # background movement
        self.rel_y = self.y % self.image.get_rect().height
        surface.blit(self.image, [0, self.rel_y - self.image.get_rect().height])
        if self.rel_y < 1080:
            surface.blit(self.image, (0, self.rel_y))
        self.y += 0.8 + speed

    def draw2(self, surface):
        surface.blit(self.image, [-1920, -1080])
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = self.rot + self.rot_speed
            if self.rot >= 360:
                self.rot = 1
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


class MainPlayer(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image_orig = pg.image.load(os.path.join(img_folder, "spaceship.png")).convert_alpha()
        self.image2 = pg.image.load(os.path.join(img_folder, "64_enemyship.png")).convert_alpha()
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 90
        self.clock = pg.time.Clock()
        self.dt = self.clock.tick(FPS) / 1000.0

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = 200
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -200
        if keys[pg.K_UP] or keys[pg.K_w]:
                self.vel = vec(300, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-300 / 2, 0).rotate(-self.rot)
        if keys[pg.K_o]:
            self.image_orig = self.image2

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.dt) % 360
        self.image = pg.transform.rotate(self.image_orig, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.dt
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT


