import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 1280
HEIGHT = 720
FPS = 60

# Define terms
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (101, 67, 33)

pygame.init()
pygame.mixer.init()

font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
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
    global tunnels, all_sprites
    screen.blit(background, (0,0))
    draw_text(screen, "Space Escape", 128, WIDTH / 2, HEIGHT / 4)
    #draw_text(screen, "Score: " + str(score), 44, WIDTH / 2, HEIGHT / 3)
    draw_text(screen, "Arrow Keys to Move, Space to Fire!", 44, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin!", 32, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
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
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):

        self.rect.x += -1

class Player(pygame.sprite.Sprite):
    # Sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("SE/spaceship.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, 270)
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.radius = 26
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        # Unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            self.speedy += 10
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            self.speedy -= 10
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx += 10
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx -= 10
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if keystate[pygame.K_q]:
            pygame.quit()

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
            bullet = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

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
        self.radius = int(self.rect.width * 0.8 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = 1300
        self.rect.y = random.randrange(60, 640)
        self.speedx = random.randrange(1, 8)
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
            self.speedx = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = -10

    def update(self):
        self.rect.x -= self.speedx
        # Kill the bullet when off the screen
        if self.rect.bottom < 0:
            self.kill()

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
screen = pygame.display.set_mode((WIDTH, HEIGHT))
heart = pygame.image.load(path.join(img_dir, "heart_2.gif")).convert()
live = pygame.transform.scale(heart, (30, 30))
meteor_images = []
meteor_list = ['small1.png', 'small2.png', 'small3.png', 'small4.png', 'small5.png', 'small6.png',
               'medium1.png', 'medium2.png', 'medium3.png', 'medium4.png', 'medium5.png', 'medium5.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert_alpha())

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

# Load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'laser1.wav'))
expl_sound = pygame.mixer.Sound(path.join(snd_dir, 'explosion.wav'))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
pygame.mixer.music.load(path.join(snd_dir, 'space.ogg'))
pygame.mixer.music.set_volume(0.4)

pygame.display.set_caption("Space Escape")
clock = pygame.time.Clock()

background = pygame.image.load("SE/starfield.jpg").convert()

pygame.mixer.music.play(loops=-1)

tunnels = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


# Game loop

def Escape_Game(ext_screen):
    global all_sprites, mobs, bullets, tunnel_gat, screen

    screen = ext_screen

    running = True
    game_over = True
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
            game_over = False

            mobs = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)

            for i in range(10):
                newmob()
            score = 0

        # Keep loop running at the right speed
        clock.tick(FPS)
        # Process input (events)
        for event in pygame.event.get():
            # Check for closing window
            if event.type == pygame.QUIT:
                running = False
            if pygame.key.get_pressed()[pygame.K_ESCAPE] or pygame.key.get_pressed()[pygame.K_q]:
                running = False

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

            tunnel_hoogte += random.randrange(-5, 7)

            # Boven Helft Tunnel
            t = Tunnel(WIDTH + 10, 0, tunnel_hoogte)
            tunnels.add(t)
            # Onder Helft Tunnel
            t = Tunnel(WIDTH + 10, HEIGHT - tunnel_hoogte, tunnel_hoogte)
            tunnels.add(t)

        if score > 100 and not diff_1:
            print("Updated")
            tunnel_gat = 150
            tunnel_half = (HEIGHT / 2) - (tunnel_gat / 2)
            diff_1 = True

        if score > 200 and not diff_2:
            print("Updated")
            tunnel_gat = 100
            tunnel_half = (HEIGHT / 2) - (tunnel_gat / 2)
            diff_2 = True

        if score > 500 and not diff_3:
            print("Updated")
            tunnel_gat = 75
            tunnel_half = (HEIGHT / 2) - (tunnel_gat / 2)
            diff_3 = True

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
        hits = pygame.sprite.spritecollide(player, tunnels, False)
        for hit in hits:
            player.shield = 0
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

        # Check to see if a mob hit the player
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.shield -= hit.radius * 2
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
        if player.lives == 0 and not death_explosion.alive():
            game_over = True
            tunnels.empty()
            all_sprites.empty()
            diff_1 = False
            diff_2 = False
            diff_3 = False


        # Draw / Render
        rel_x = x % background.get_rect().width

        screen.blit(background, (rel_x - background.get_rect().width, 0))
        if rel_x < WIDTH:
            screen.blit(background, (rel_x, 0))
        x -= 2

        all_sprites.draw(screen)
        tunnels.draw(screen)

        draw_text(screen, str(score), 30, WIDTH / 2, 10)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_lives(screen, WIDTH - 100, 5, player.lives, live)
        # After drawing everything, flip the display
        pygame.display.flip()

    pygame.quit()

