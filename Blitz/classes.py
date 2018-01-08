import pygame, os
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # sprite inladen
        self.image = spaceship_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 250
        self.rect.y = 600
        self.health = 5
        self.god = 0
        self.speed = 4
        self.speed_reverse = 6
        self.shoot_delay = 400
        self.last_update = pygame.time.get_ticks()
        self.last_update1 = pygame.time.get_ticks()
        self.shield = 300
        self.shield_st = True
        self.shield_st1 = True
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()


    def update(self):
        #powerup timer
        if self.power > 1 and pygame.time.get_ticks() - self.power_time > poweruptime:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        #unhide if hidden
        if self.hidden == True and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.x = 250
            self.rect.y = 600
        # movement keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            if self.rect.bottom >= H:
                self.rect.y += 0
                background.y -= 2
            else:
                self.rect.y += self.speed_reverse
                # self.image = self.image_straight

        if keys[pygame.K_w]:
            if self.rect.top <= 0:
                self.rect.y += 0
            else:
                self.rect.y -= self.speed
                # self.image = self.image_straight
            #background.y += 4

        if keys[pygame.K_d]:
            if self.rect.right >= W:
                self.rect.x += 0
                # self.image = self.image_right
            else:
                self.rect.x += self.speed
                # self.image = self.image_right

        if keys[pygame.K_a]:
            if self.rect.left <= 0:
                self.rect.x -= 0
                # self.image = self.image_left
            else:
                self.rect.x -= self.speed
                # self.image = self.image_left

        # function keys
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_SPACE]: #or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # amount of bullets on screen
            self.shoot()

    def powerup(self):
        self.power += 1
        if self.power >= 3:
            self.power = 3
        self.power_time = pygame.time.get_ticks()


    def shoot(self):
        # delay for shooting
        now = pygame.time.get_ticks()
        now1 = pygame.time.get_ticks()
        if now - self.last_update > self.shoot_delay:
            self.last_update = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1, bullet2)
                bullets.add(bullet1, bullet2)
            if self.power == 3:
                bullet1 = Bullet(self.rect.centerx, self.rect.top)
                bullet2 = Bullet(self.rect.left, self.rect.centery)
                bullet3 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1, bullet2, bullet3)
                bullets.add(bullet1, bullet2, bullet3)
        # delay for the shooting sound
        if now1 - self.last_update1 > 500:
            self.last_update1 = now1
            shoot_sound.play()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (W + 200, H + 200)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(W - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 15)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

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
        self.rect.y += self.speedy #+ background.speed
        self.rect.x -= self.speedx
        if self.rect.top > H + 150 or self.rect.right < 0 or self.rect.left > W:
            self.rect.x = random.randrange(W - self.rect.width)
            self.rect.y = random.randrange(-100, -80)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)

        if player.rect.bottom > H and pygame.key.get_pressed()[pygame.K_s]:
            self.rect.y -= 4


class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["shield", "shoot"])
        self.image = powerup_img[self.type]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # kill it if it moves off the screen
        if self.rect.top > H:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill it if it moves off the screen
        if self.rect.bottom < 0:
            self.kill()


class Background(object):
    def __init__(self):
        self.image = pygame.image.load(os.path.join(img_folder, "starrybackground.jpg")).convert()
        self.image.get_rect()
        self.y = 720
        self.rel_y = 0
        self.rect = self.image.get_rect()
        self.speed = 0
        self.speed_regulator = True

    def draw(self, surface):
        # self speed regulator
        if self.speed <= 60 and self.speed_regulator == True:
            self.speed += 0.01
            if self.speed >= 60:
                self.speed_regulator = False
        if self.speed_regulator == False:
            self.speed -= 0.01
            if self.speed <= 1:
                self.speed_regulator = True

        # background movement
        self.rel_y = self.y % self.image.get_rect().height
        surface.blit(self.image, [0, self.rel_y - self.image.get_rect().height])
        if self.rel_y < 1080:
            surface.blit(self.image, (0, self.rel_y))
        self.y += 1 + self.speed


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_images[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_images[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_images[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center