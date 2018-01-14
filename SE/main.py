import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

POWERUP_TIME = 5000 # 5 seconden power up tijd

WIDTH = 1280        # breedte scherm
HEIGHT = 720        # hoogte scherm
FPS = 60            # frame per second = 60

# Kleuren gedefinieerd
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (101, 67, 33)
GREY = (20, 20, 20)

pygame.init()
pygame.mixer.init()     # Pygame code waardoor muziek werkt

def draw_text(surf, text, size, x, y):
    font_name = pygame.font.Font("Blitz/8.TTF", size)
    text_surface = font_name.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newpowerup():
    pow = Pow()
    all_sprites.add(pow)
    powerups.add(pow)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def show_go_screen():
    global tunnels, all_sprites, tunnel_hoogte, tunnel_gat, diff_1, diff_2, diff_3
    screen.blit(background, (0,0))
    draw_text(screen, "Space Escape", 70, WIDTH / 2, HEIGHT / 4)

    draw_text(screen, "PowerUps", 30, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Pill gives Shield Restore and Bullets", 20, WIDTH / 2, HEIGHT / 1.8)
    draw_text(screen, "Shield gives Shield Restore", 20, WIDTH / 2, HEIGHT / 1.7)
    draw_text(screen, "Bolt gives Bullets", 20, WIDTH / 2, HEIGHT / 1.6)

    draw_text(screen, "Keys", 30, WIDTH / 2, HEIGHT / 1.4)
    draw_text(screen, "Use the arrow keys to move around", 20, WIDTH / 2, HEIGHT / 1.3)
    draw_text(screen, "Use space to shoot", 20, WIDTH / 2, HEIGHT / 1.25)
    draw_text(screen, "Press R to begin", 20, WIDTH / 2, HEIGHT / 1.15)
    draw_text(screen, "Press esc or q key to Exit at any time", 20, WIDTH / 2, HEIGHT / 1.1)
    #draw_text(screen, "Highscore: " + str(highscore), 20, WIDTH / 2, HEIGHT / 3)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:           # Rood kruisje klikken sluit python
                pygame.quit()
        if pygame.key.get_pressed()[pygame.K_r]:    # R klikken start de game
            waiting = False

    tunnel_gat = 400
    tunnel_half = (HEIGHT / 2) - (tunnel_gat / 2)
    tunnel_i = 0
    tunnel_hoogte = 200

    diff_1 = False
    diff_2 = False
    diff_3 = False


    while len(tunnels) < 128 * 2 + 10:
        while tunnel_hoogte > tunnel_half:
            tunnel_hoogte += -5
        while tunnel_hoogte <= 0:
            tunnel_hoogte += 5

        tunnel_hoogte += random.randrange(-5, 6)

        # Boven Helft Tunnel
        t = Tunnel(tunnel_i, 0, tunnel_hoogte)
        tunnels.add(t)
        # Onder Helft Tunnel
        t = Tunnel(tunnel_i, HEIGHT - tunnel_hoogte, tunnel_hoogte)
        tunnels.add(t)
        tunnel_i += 10

class Tunnel(pygame.sprite.Sprite):
    def __init__(self, x, y, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,h))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):

        self.rect.x += -5

class Player(pygame.sprite.Sprite):
    # Sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("SE/spaceship.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, 270)
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.center = (WIDTH / 4, HEIGHT / 2)
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 0
        self.power_time = pygame.time.get_ticks()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # Time out for powerups
        if self.power >= 1 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        # Unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.center = (WIDTH / 4, HEIGHT / 2)
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            self.speedy += 5
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            self.speedy -= 5
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx += 5
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx -= 5
        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power >= 1:
                bullet = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
                keystate = pygame.key.get_pressed()
                if keystate[pygame.K_SPACE]:
                    self.shoot()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.45 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = 1300
        self.rect.y = random.randrange(60, 640)
        self.speedx = random.randrange(6, 10)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x -= self.speedx
        if self.rect.right < 0:
            self.rect.x = 1300
            self.rect.y = random.randrange(60, 640)
            self.speedx = random.randrange(6, 10)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = -4

    def update(self):
        self.rect.x -= self.speedx
        # Kill the bullet when off the screen
        if self.rect.centerx < -10:
            self.kill()
        #if self.rect.centerx > 500:
        #    self.kill()

class Pow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun', 'pill'])
        self.image = powerup_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1300, 1800)
        self.rect.y = HEIGHT / 2
        self.speedx = random.randrange(6, 10)

    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right < 0:
            self.rect.x = 1300
            self.rect.y = HEIGHT / 2
            self.speedx = random.randrange(6, 10)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Load all game graphics
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
heart = pygame.image.load(path.join(img_dir, "heart_2.gif")).convert()
live = pygame.transform.scale(heart, (30, 30))
meteor_images = []
meteor_list = ['small1.png', 'small2.png', 'small3.png', 'small4.png', 'small5.png', 'small6.png',
               'medium1.png', 'medium2.png', 'medium3.png', 'medium4.png', 'medium5.png', 'medium5.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert_alpha())

# Directory explosion images
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range (9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert_alpha()
    explosion_anim['player'].append(img)

# Directory power up images
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_silver.png')).convert_alpha()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bold_silver.png')).convert_alpha()
powerup_images['pill'] = pygame.image.load(path.join(img_dir, 'pill_yellow.png')).convert_alpha()

# Load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'laser1.wav'))
shoot_sound.set_volume(0.2)
expl_sound = pygame.mixer.Sound(path.join(snd_dir, 'explosion.wav'))
expl_sound.set_volume(0.2)
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
player_die_sound.set_volume(0.2)
pygame.mixer.music.load(path.join(snd_dir, 'space.ogg'))
pygame.mixer.music.set_volume(0.35)

pygame.display.set_caption("Space Escape")
clock = pygame.time.Clock()

background = pygame.image.load("SE/starfield.jpg").convert()

tunnels = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Game loop

def Escape_Game(ext_screen, story):
    print(story)
    global all_sprites, mobs, bullets, tunnel_gat, screen, powerups

    screen = ext_screen
    newscore = 0
    running = True
    game_over = True
    pygame.mixer.music.play(loops=-1)

    x = 0
    tunnel_gat = 400
    tunnel_half = (HEIGHT / 2) - (tunnel_gat / 2)
    tunnel_i = 0
    tunnel_hoogte = 200

    diff_1 = False
    diff_2 = False
    diff_3 = False

    while running:
        if game_over:
            show_go_screen()
            mobs = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            powerups = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            game_over = False

            score = 0
            for i in range(10):
                newmob()

        # Keep loop running at the right speed
        clock.tick(FPS)
        # Process input (events)
        for event in pygame.event.get():
            # Check for closing window
            if pygame.key.get_pressed()[pygame.K_ESCAPE] or pygame.key.get_pressed()[pygame.K_q]:
                all_sprites.empty()
                mobs.empty()
                bullets.empty()
                powerups.empty()
                running = False
            if running == False:
                pygame.mixer.music.fadeout(1000)

        # Keep Creating Tunnels
        for tunnel in tunnels:    # Tunnels weghalen als ze van scherm af gaan
            if tunnel.rect.x <= -10:
                tunnel.kill()

        while len(tunnels) < (128 * 2) + 25:
            print(tunnel_half)
            while tunnel_hoogte > tunnel_half:
                tunnel_hoogte += -10
                print('1')
            while tunnel_hoogte <= 0:
                tunnel_hoogte += 10
                print('2')

            tunnel_hoogte += random.randrange(-5, 8)

            # Boven Helft Tunnel
            t = Tunnel(WIDTH + 10, 0, tunnel_hoogte)
            tunnels.add(t)
            # Onder Helft Tunnel
            t = Tunnel(WIDTH + 10, HEIGHT - tunnel_hoogte, tunnel_hoogte)
            tunnels.add(t)

        if x < 100:
            score += 0.25

        if score > newscore + 400:
            newpowerup()
            newscore = score

        if score > 1000 and not diff_1:
            print("Updated")
            tunnel_gat = 300
            tunnel_half = (HEIGHT / 2) - (tunnel_gat / 2)
            diff_1 = True

        if score > 2000 and not diff_2:
            print("Updated")
            tunnel_gat = 200
            tunnel_half = (HEIGHT / 2) - (tunnel_gat / 2)
            diff_2 = True

        if score > 3000 and not diff_3:
            print("Updated")
            tunnel_gat = 150
            tunnel_half = (HEIGHT / 2) - (tunnel_gat / 2)
            diff_3 = True

        #if score > 4000 and not diff_2:
        #    print("Updated")
        #    tunnel_gat = 200
        #    tunnel_half = (HEIGHT / 2) - (tunnel_gat / 2)
        #    diff_2 = True

        # Update
        all_sprites.update()
        tunnels.update()

        # Check to see if a bullet hit mob
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 50 - hit.radius
            expl_sound.play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            newmob()

        # Check to see if the player hits the wall
        hits = pygame.sprite.spritecollide(player, tunnels, False, pygame.sprite.collide_circle)
        for hit in hits:
            player.shield -= 10
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            if player.shield <= 0:
                player_die_sound.play()
                death_explosion = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1
                player.shield = 100

        # Check to see if a mob hits the wall
        hits = pygame.sprite.groupcollide(mobs, tunnels, True, False)
        for hit in hits:
            newmob()

        # Check to see if a power up hits the wall
        hits = pygame.sprite.groupcollide(powerups, tunnels, True, False)
        for hit in hits:
            newpowerup()

        # Check to see if the player hit a powerup
        hits = pygame.sprite.spritecollide(player, powerups, True, pygame.sprite.collide_mask)
        for hit in hits:
            if hit.type == 'shield':
                player.shield += random.randrange(10, 50)
                if player.shield >= 100:
                        player.shield = 100
            if hit.type == 'gun':
                player.powerup()
            if hit.type == 'pill':
                player.shield += random.randrange(10, 50)
                if player.shield >= 100:
                    player.shield = 100
                player.powerup()

        # Check to see if a mob hit the player
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.shield -= hit.radius * 0.5
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            newmob()
            if player.shield <= 0:
                player_die_sound.play()
                death_explosion = Explosion(player.rect.center, 'player')
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1
                player.shield = 100

        # If the player died and the explosion has finished playing
        if player.lives <= 0 and not death_explosion.alive():
            game_over = True
            tunnels.empty()
            all_sprites.empty()
            diff_1 = False
            diff_2 = False
            diff_3 = False
            tunnel_gat = 400
            tunnel_half = (HEIGHT / 2) - (tunnel_gat / 2)

        # Draw / Render
        rel_x = x % background.get_rect().width

        screen.blit(background, (rel_x - background.get_rect().width, 0))
        if rel_x < WIDTH:
            screen.blit(background, (rel_x, 0))
        x -= 2

        all_sprites.draw(screen)
        tunnels.draw(screen)

        draw_text(screen, str(int(score)), 30, WIDTH / 2, 10)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_lives(screen, WIDTH - 100, 5, player.lives, live)
        # After drawing everything, flip the display
        pygame.display.flip()