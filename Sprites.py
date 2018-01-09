from settings import *
import pygame as pg
import pygame as pygame


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
        self.image = pg.image.load(os.path.join(img_folder, "Climb planet.png")).convert_alpha()
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