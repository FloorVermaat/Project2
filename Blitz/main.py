import pygame, sys, os, random, time
vec = pygame.math.Vector2
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

size = (W, H) = 1280, 720
FPS = 60
poweruptime = 30000
HS_File = "highscore.txt"
# asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
img_folder2 = os.path.join(img_folder, )
snd_folder = os.path.join(game_folder, 'sounds')

# Initialize pygame and create window
#pygame.init()
#pygame.mixer.init()

#screen = pygame.display.set_mode(size)

pygame.display.set_caption("The bestest of games")
clock = pygame.time.Clock()
keys = pygame.key.get_pressed()
Name = ""


# drawing text on screen
def draw_text(surf, text, size, x, y):
    font_name = pygame.font.Font("Blitz/8.TTF", size)
    text_surface = font_name.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# adding mob to mob groups and spawning them
def newmob():
    m = Mob()
    Blitz_sprites.add(m)
    mobs.add(m)


# adding enemyships to enemyship group and spawning them
def enemymob():
    e = EnemyShip()
    Blitz_sprites.add(e)
    enemyship.add(e)


# adding boss mob to the all sprites group
#def bossmob():
#    b = BossShip()
#    all_sprites.add(b)
#    Endboss.add(b)


# drawing the shield bar on the screen
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    bar_length = 70
    bar_height = 20
    fill = (pct / 150) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_bosshield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    bar_length = W / 2 - 70
    bar_height = 30
    fill = (pct / 5000) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

# drawing the powerup bar on the screen
def draw_powerup_bar(surf, x, y, time):
    if time < 0:
        time = 0
    bar_length = 100
    bar_height = 20
    fill = (time / poweruptime) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x + 1, y, fill, bar_height)
    pygame.draw.rect(surf, YELLOW, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


# drawing lives on the screen
def draw_lives(surf, x, y, lives, img):
    for life in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * life
        img_rect.y = y
        surf.blit(img, img_rect)


def name_input_screen():
    global nameinputscreen, intro_screen, text
    font = pygame.font.Font("8-BIT WONDER.ttf", 16)
    input_box = pygame.Rect(W / 2 - 100, H / 2 - 50, 140, 32)
    input_boxbackground = input_box
    color_inactive = pygame.Color('lightskyblue3')
    color_active = GREEN
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        background.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN and len(text) >= 3:
                        intro_screen = True
                        nameinputscreen = False
                        done = True
                        return text

                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Render the current text.
        txt_surface = font.render(text, True, BLACK)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        input_boxbackground.w = width
        # Blit the text.
        pygame.draw.rect(screen, WHITE, input_boxbackground)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        draw_text(screen, "The Number One", 64, W / 2, 50)
        draw_text(screen, "Insert Name", 30, W / 2, 200)
        draw_text(screen, "Name has to be atleast 3 characters long", 15, W / 2, H / 2 + 50)
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 5)
        pygame.display.flip()
        clock.tick(FPS)


def show_gameover_screen():
    global highscore, intro_screen, game_over
    waiting = True
    newhighscore = False
    pygame.mixer.music.fadeout(1000)
    while waiting:
        clock.tick(FPS)
        background.draw(screen)
        draw_text(screen, "Space Pirate " + text, 12, 120, 10)
        draw_text(screen, "You Died", 64, W / 2, H / 8)
        draw_text(screen, "your score was " + str(score), 15, W / 2, H / 3)
        draw_text(screen, "Press R key to return to homescreen", 15, W / 2, H / 2)
        if score > highscore:
            highscore = score
            newhighscore = True
            with open(os.path.join(game_folder, HS_File), 'r+') as f:
                f.write(str(highscore))
        if newhighscore:
            draw_text(screen, "YOU SET A NEW RECORD!", 15, W / 2, H / 1.5)
        pygame.display.flip()
        for test in pygame.event.get():
            if test.type == pygame.QUIT:
                pygame.quit()
            if pygame.key.get_pressed()[pygame.K_r]:
                intro_screen = True
                game_over = False
                waiting = False


def show_intro_screen():
    waiting = True
    while waiting:
        clock.tick(FPS)
        background.draw(screen)
        draw_text(screen, "Space Pirate " + Name, 12, 120, 10)
        draw_text(screen, "Blitz", 64, W / 2, H / 8)
        draw_text(screen, "use WASD to move around", 15, W / 2, H / 3)
        draw_text(screen, "Space to shoot", 15, W / 2, H / 2.5)
        draw_text(screen, "Press R key to begin", 15, W / 2, H / 1.3)
        draw_text(screen, "Highscore " + str(highscore), 15, W / 2, H / 1.1)
        pygame.display.flip()
        for test in pygame.event.get():
            if test.type == pygame.QUIT:
                pygame.quit()
            if pygame.key.get_pressed()[pygame.K_r]:
                waiting = False


def show_victory_screen():
    global highscore, intro_screen, victory
    waiting = True
    newhighscore = False
    pygame.mixer.music.fadeout(1000)
    while waiting:
        clock.tick(FPS)
        background.draw(screen)
        draw_text(screen, "Space Pirate " + text, 12, 120, 10)
        draw_text(screen, "VICTORY", 64, W / 2, H / 8)
        draw_text(screen, "your score was " + str(score), 15, W / 2, H / 3)
        draw_text(screen, "Press R key to return to homescreen", 15, W / 2, H / 2)
        if score > highscore:
            highscore = score
            newhighscore = True
            with open(os.path.join(game_folder, HS_File), 'r+') as f:
                f.write(str(highscore))
        if newhighscore:
            draw_text(screen, "YOU SET A NEW RECORD!", 15, W / 2, H / 1.5)
        pygame.display.flip()
        for test in pygame.event.get():
            if test.type == pygame.QUIT:
                pygame.quit()
            if pygame.key.get_pressed()[pygame.K_r]:
                intro_screen = True
                victory = False
                waiting = False

def shield_status():
    if not player.shield_st:
        death_expl = Explosion(player.rect.center, "player")
        Blitz_sprites.add(death_expl)
        player.hide()
        player.lives -= 1
        player.shield = 150
        player.shield_st1 = True
        player.shield_st = True
        player.powerbar = 0
        player.power = 1
    # if shield is at half, this happens
    if player.shield <= 75 and player.shield >= 1 and player.shield_st1:
        player.shield = 75
        shields_50.play()
        player.shield_st1 = False
    # if shield is down, this happens
    if player.shield <= 0: #and player.shield_st:
        player.shield_st = False
        shields_50.stop()
        shields.play()


def collision_checks():
    # player vs powerup collision check
    global score, game_over, bossbattle, victory
    power = pygame.sprite.spritecollide(player, powerups, True, pygame.sprite.collide_mask)
    for hits in power:
        if hits.type == "shield":
            player.shield += 50
            if player.shield >= 150:
                player.shield = 150
            if player.shield > 75:
                player.shield_st1 = True
            if player.shield in range(1, 75):
                player.shield_st = True
        if hits.type == "shoot":
            player.powerbar = poweruptime
            player.powerup()

    # enemybullet vs player collision check
    bulletvsplayer = pygame.sprite.spritecollide(player, enemybullets, True, pygame.sprite.collide_mask)
    for i in bulletvsplayer:
        expl = Explosion(i.rect.center, "small")
        Blitz_sprites.add(expl)
        player.shield -= 75
        # if you die this happens
        shield_status()

    # enemyship/mine vs player collision check
    shipvsplayer = pygame.sprite.spritecollide(player, enemyship, True, pygame.sprite.collide_mask)
    for i in shipvsplayer:
        expl = Explosion(i.rect.center, "player")
        Blitz_sprites.add(expl)
        player.shield -= player.shield
        # if you die this happens
        death_expl = Explosion(player.rect.center, "player")
        Blitz_sprites.add(death_expl)
        player.hide()
        player.lives -= 1
        player.shield = 300
        player.shield_st1 = True
        player.shield_st = True
        player.powerbar = 0
        player.power = 1

    # Player vs mob collision check
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_mask)
    for hit in hits:
        expl = Explosion(hit.rect.center, "small")
        Blitz_sprites.add(expl)
        newmob()
        player.shield -= hit.radius
        # if you die this happens
        shield_status()


    # enemyship vs mob collision check
    enemyvsmobhits = pygame.sprite.groupcollide(enemyship, mobs, False, True, pygame.sprite.collide_mask)
    for hit in enemyvsmobhits:
        expl = Explosion(hit.rect.center, "small")
        Blitz_sprites.add(expl)
        newmob()
        hit.shield -= 25

    # mob vs enemybullet collision check
    zap = pygame.sprite.groupcollide(mobs, enemybullets, True, True, pygame.sprite.collide_mask)
    for z in zap:
        expl = Explosion(z.rect.center, "large")
        Blitz_sprites.add(expl)
        newmob()
        # manage volume for the explosion sounds
        expl_sound = random.choice(explosion_sound)
        expl_sound.set_volume(0.1)
        expl_sound.play()

    # mobs vs Bullet collision check
    destroy = pygame.sprite.groupcollide(mobs, bullets, True, True, pygame.sprite.collide_mask)
    for boom in destroy:
        score += 130 - boom.radius
        expl = Explosion(boom.rect.center, "large")
        Blitz_sprites.add(expl)
        # spawn powerups
        if random.randrange(0, 10) == 4:
            pow = Powerup(boom.rect.center)
            Blitz_sprites.add(pow)
            powerups.add(pow)
        newmob()
        # manage volume of the explosion sounds
        expl_sound = random.choice(explosion_sound)
        expl_sound.set_volume(0.1)
        expl_sound.play()

    # bullet vs enemyship collision check
    enemyboom = pygame.sprite.groupcollide(enemyship, bullets, False, True, pygame.sprite.collide_mask)
    for i in enemyboom:
        i.shield -= 75
        if i.shield <= 0:
            score += 400
            expl = Explosion(i.rect.center, "player")
            Blitz_sprites.add(expl)
            Blitz_sprites.remove(i)
            enemyship.remove(i)
            if random.randrange(0, 5) == 4:
                pow = Powerup(i.rect.center)
                Blitz_sprites.add(pow)
                powerups.add(pow)

    # bullet vs bullet collision check
    bulletwipe = pygame.sprite.groupcollide(bullets, enemybullets, True, True, pygame.sprite.collide_mask)
    for i in bulletwipe:
        expl = Explosion(i.rect.center, 'small')
        Blitz_sprites.add(expl)

    # bullet vs Bosship collision check
    bulletvsboss = pygame.sprite.spritecollide(BosShip, bullets, True, pygame.sprite.collide_mask)
    for i in bulletvsboss:
        expl = Explosion(i.rect.center, "small")
        Blitz_sprites.add(expl)
        BosShip.shield -= 75
        if BosShip.shield <= 0:
            expl = Explosion(i.rect.center, "player")
            Blitz_sprites.add(expl)
            Blitz_sprites.remove(BosShip)
            score += 5000
            bossbattle = False
            victory = True
        if random.randrange(0, 10) == 4:
            pow = Powerup(i.rect.center)
            Blitz_sprites.add(pow)
            powerups.add(pow)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # sprite inladen
        self.image = spaceship_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = W / 2
        self.rect.y = 600
        self.health = 5
        self.god = 0
        self.speed = 6
        self.speed_reverse = 6
        self.shoot_delay = 400
        self.last_update = pygame.time.get_ticks()
        self.last_update1 = pygame.time.get_ticks()
        self.shield = 150
        self.shield_st = True
        self.shield_st1 = True
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.powerbar = 0
        self.powerbar_time = pygame.time.get_ticks()

    def update(self):
        # power up bar timer
        if self.powerbar > 0 and pygame.time.get_ticks() - self.powerbar_time > 100:
            self.powerbar -= 100
            self.powerbar_time += 100

        # power up timer
        if self.power > 1 and pygame.time.get_ticks() - self.power_time > poweruptime:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
            if self.powerbar == 0 and self.power > 1:
                self.powerbar = poweruptime

        # unhide if hidden
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
        if keys[pygame.K_SPACE]: # or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # amount of bullets on screen
            self.shoot()

    def powerup(self):
        self.power += 1
        if self.power >= 3:
            self.power = 3
        self.power_time = pygame.time.get_ticks()
        self.powerbar_time = pygame.time.get_ticks()

    def shoot(self):
        # delay for shooting
        now = pygame.time.get_ticks()
        now1 = pygame.time.get_ticks()
        if now - self.last_update > self.shoot_delay:
            self.last_update = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top, -10)
                Blitz_sprites.add(bullet)
                bullets.add(bullet)
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery, -10)
                bullet2 = Bullet(self.rect.right, self.rect.centery, -10)
                Blitz_sprites.add(bullet1, bullet2)
                bullets.add(bullet1, bullet2)
            if self.power == 3:
                bullet1 = Bullet(self.rect.centerx, self.rect.top, -10)
                bullet2 = Bullet(self.rect.left, self.rect.centery, -10)
                bullet3 = Bullet(self.rect.right, self.rect.centery, -10)
                Blitz_sprites.add(bullet1, bullet2, bullet3)
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


class EnemyShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["suicide", "normal", "laserbeam", "normal"])
        self.image_orig = enemyimages[self.type]
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.spawnlocation = [-30, W + 50]
        self.spawnlocation2 = random.choice(self.spawnlocation)
        self.distance = 0
        if self.spawnlocation2 == -30:
            self.distance *= -1
        self.rect.x = self.spawnlocation2 + self.distance
        self.rect.y = random.randrange(50, 200)
        # regulates speed
        self.speedy = 0
        self.speedx = 2
        if self.rect.x > W:
            self.speedx *= -1
        self.onscreen = False
        self.shoot_delay = 750
        self.last_update = pygame.time.get_ticks()
        # different shield values for the different enemyships
        self.shield = 300
        if self.type == "suicide":
            self.shield = 225
        self.enemyspawn = 0
        self.rot = 0
        self.rot_speed = 8
        self.vx, self.vy = 0, 0

    def update(self):
        # determines movement of the different spawns
        if self.type == "normal":
            self.shoot(Enemybullet_image, self.rect.centerx, self.rect.bottom, +10, 0)
            self.rect.x += self.speedx
            if self.spawnlocation2 == -30:
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                if self.rect.left > 0:
                    self.onscreen = True
            if self.rect.right > W and self.onscreen:
                self.speedx *= -1

            if self.spawnlocation2 == W + 50:
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                if self.rect.right < W:
                    self.onscreen = True
            if self.rect.left < 0 and self.onscreen:
                self.speedx *= -1

        if self.type == "suicide":
            self.rotate()
            self.speedx = random.randrange(1, 4)
            self.speedy = random.randrange(1, 4)
            self.follow()

        if self.type == "laserbeam":
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            self.shoot_delay = 25
            if self.spawnlocation2 == -30 and self.rect.right > W / 2:
                self.shoot(Enemybullet_image_horiz, self.rect.centerx, self.rect.bottom, 0, +10)
                self.speedx -= self.speedx
                self.speedy += 0.04
            if self.spawnlocation2 == W + 50 and self.rect.left < W / 2:
                self.shoot(Enemybullet_image_horiz, self.rect.centerx, self.rect.bottom, 0, +10)
                self.speedx -= self.speedx
                self.speedy += 0.04
            if self.rect.top > H:
                self.kill()

    def follow(self): # chase movement
            # Movement along x direction
        if self.rect.x > player.rect.x:
            self.rect.x -= self.speedx
        elif self.rect.x < player.rect.x:
            self.rect.x += self.speedx
        # Movement along y direction
        if self.rect.y < player.rect.y:
            self.rect.y += self.speedy
        elif self.rect.y > player.rect.y:
            self.rect.y -= self.speedy

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

    def shoot(self, img, x, y, movy, movx):
        # delay for shooting
        now = pygame.time.get_ticks()
        if now - self.last_update > self.shoot_delay:
            self.last_update = now
            if self.type == "normal":
                self.shoot_delay -= 15
                if self.shoot_delay <= 180:
                    self.shoot_delay = 180
                bullet = EnemyBullet(img, x, y, movy, movx)
                Blitz_sprites.add(bullet)
                enemybullets.add(bullet)
            if self.type == "laserbeam":
                bullet = EnemyBullet(img, x + 25, y - 25, movy, movx)
                Blitz_sprites.add(bullet)
                enemybullets.add(bullet)
                bullet2 = EnemyBullet(img, x - 25, y - 25, movy, -movx)
                Blitz_sprites.add(bullet2)
                enemybullets.add(bullet2)


class BossShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = spaceship_boss
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = -250
        self.rect.y = 200
        self.speedy = 0
        self.speedx = 4
        self.shoot_delay = 250
        self.last_update = pygame.time.get_ticks()
        self.shield = 5000
        self.onscreen = False

    def update(self):
        if bossbattle:
            self.shoot()
            if self.rect.left > 0:
                self.onscreen = True
            # determines movement of the Boss
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.right >= W:
                self.speedx = -4
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                if self.shield <= 2500:
                    self.speedx = -25
                    self.shoot_delay = 125
            elif self.rect.left <= 0 and self.onscreen:
                self.speedx = 4
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                if self.shield <= 2500:
                    self.speedx = 25
                    self.shoot_delay = 125
    def shoot(self):
        # delay for shooting
        now = pygame.time.get_ticks()
        if now - self.last_update > self.shoot_delay:
            self.last_update = now
            bullet = EnemyBullet(Enemybullet_boss, self.rect.centerx, self.rect.bottom, +10, 0)
            Blitz_sprites.add(bullet)
            enemybullets.add(bullet)


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
        self.speedy = random.randrange(5, 17)
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
    def __init__(self, x, y, mov):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = mov

    def update(self):
        self.rect.y += self.speedy
        # kill it if it moves off the screen
        if self.rect.bottom < 0:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, img, x, y, movy, movx):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = movy
        self.speedx = movx

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # kill it if it moves off the screen
        if self.rect.top > H or self.rect.left > W or self.rect.right < 0:
            self.kill()


class Background(object):
    def __init__(self):
        self.image = pygame.image.load(os.path.join(img_folder, "spacebackground.jpg")).convert()
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
        if not self.speed_regulator:
            self.speed -= 0.01
            if self.speed <= 1:
                self.speed_regulator = True

        # background movement
        self.rel_y = self.y % self.image.get_rect().height
        surface.blit(self.image, [0, self.rel_y - self.image.get_rect().height])
        if self.rel_y < 1080:
            surface.blit(self.image, (0, self.rel_y))
        self.y += 1 # + self.speed


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


# game graphics
spaceship_image = pygame.image.load(os.path.join(img_folder, "64_spaceship.png")).convert_alpha()
player_lives = pygame.image.load(os.path.join(img_folder, "lives.png")).convert_alpha()
player_minilives = pygame.transform.scale(player_lives, (25, 19))
bullet_image = pygame.image.load(os.path.join(img_folder, "laserGreen.png")).convert_alpha()
Enemybullet_image = pygame.image.load(os.path.join(img_folder, "laserRed.png")).convert_alpha()
Enemybullet_boss = pygame.transform.scale(Enemybullet_image, (10, 80))
Enemybullet_image_horiz = pygame.transform.rotate(Enemybullet_image, 90)
meteor_images = []
meteor_list = ['small1.png', 'small2.png', 'small3.png', 'small4.png', 'small5.png', 'small6.png',
               'medium1.png', 'medium2.png', 'medium3.png', 'medium4.png', 'medium5.png',
               'medium6.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(os.path.join(img_folder, img)).convert_alpha())

explosion_images = {}
explosion_images['large'] = []
explosion_images['small'] = []
explosion_images['player'] = []
explosion_dict = ['regularExplosion00.png', 'regularExplosion01.png', 'regularExplosion02.png', 'regularExplosion03.png', 'regularExplosion04.png',
                  'regularExplosion05.png', 'regularExplosion06.png', 'regularExplosion07.png', 'regularExplosion08.png',]
explosion_playerdict = ['sonicExplosion00.png', 'sonicExplosion01.png', 'sonicExplosion02.png', 'sonicExplosion03.png',
                        'sonicExplosion04.png', 'sonicExplosion05.png', 'sonicExplosion06.png', 'sonicExplosion07.png', 'sonicExplosion08.png']
for image in explosion_dict:
    img = pygame.image.load(os.path.join(img_folder, image)).convert_alpha()
    img_large = pygame.transform.scale(img, (75, 75))
    img_small = pygame.transform.scale(img, (30, 30))
    explosion_images['large'].append(img_large)
    explosion_images['small'].append(img_small)
for image in explosion_playerdict:
    img = pygame.image.load(os.path.join(img_folder, image)).convert_alpha()
    explosion_images['player'].append(img)

# power up images
shoot_img_orig = pygame.image.load(os.path.join(img_folder, "shoot_powerup.png")).convert_alpha()
shield_img_orig = pygame.image.load(os.path.join(img_folder, "shield_powerup.png")).convert_alpha()
shield_img = pygame.transform.scale(shield_img_orig, (35, 35))
shoot_img = pygame.transform.scale(shoot_img_orig, (35, 35))
powerup_img = {}
powerup_img["shoot"] = shoot_img
powerup_img["shield"] = shield_img

# enemy ship images
spaceship_boss_orig = pygame.image.load(os.path.join(img_folder, "64_enemyship.png")).convert_alpha()
spaceship_boss = pygame.transform.scale(spaceship_boss_orig, (120, 120))
spaceship_enemy = pygame.transform.rotate(spaceship_image, 180)
spacemine_image_orig = pygame.image.load(os.path.join(img_folder, "spacemine.png")).convert_alpha()
spacemine_image = pygame.transform.scale(spacemine_image_orig, (60, 60))
spacelaserbeam_image_orig = pygame.image.load(os.path.join(img_folder, "spacelaserbeam.png")).convert_alpha()
spacelaserbeam_image = pygame.transform.scale(spacelaserbeam_image_orig, (60, 60))
enemyimages = {}
enemyimages["suicide"] = spacemine_image
enemyimages["normal"] = spaceship_enemy
enemyimages["laserbeam"] = spacelaserbeam_image

# Sounds
# shooting sounds
shoot_sound = pygame.mixer.Sound(os.path.join(snd_folder, "Laser_Shoot11.wav"))
shoot_soundVolume = shoot_sound.set_volume(0.1)
# explosion sounds
explosion_sound = []
explosion_soundList = ['Explosion4.wav', 'Explosion17.wav']
for explosion in explosion_soundList:
    explosion_sound.append(pygame.mixer.Sound(os.path.join(snd_folder, explosion)))
# background music
pygame.mixer.music.load(os.path.join(snd_folder, "starwars.mp3"))
pygame.mixer.music.set_volume(0.2)
# shield sounds
shields = pygame.mixer.Sound(os.path.join(snd_folder, "shield depleted.wav"))
shields_50 = pygame.mixer.Sound(os.path.join(snd_folder, "shield_at_50.wav"))


#Look up the highscore
with open(os.path.join(game_folder, HS_File), 'r+') as f:
    try:
        highscore = int(f.read())
    except:
        highscore = 0
    f.close()

# different scenes of the game
intro_screen = True
game_over = False
bossbattle = False
victory = False
BlitzGameRun = False

background = Background()
score = 0

class Blitz:
    def __init__(self, screen):
        self.screen = screen

    def blitz_Game(self):
        global nameinputscreen, intro_screen, bossbattle, victory, Blitz_sprites, mobs, enemyship, bullets, enemybullets, powerups, BosShip, enemyfleet, player, score, game_over, Name
        done = False
        # -------- Main Program Loop -----------
        while not done:

            if intro_screen:
                bossbattle = False
                game_over = False
                victory = False
                show_intro_screen()
                intro_screen = False
                # Groups
                Blitz_sprites = pygame.sprite.Group()
                mobs = pygame.sprite.Group()
                enemyship = pygame.sprite.Group()
                bullets = pygame.sprite.Group()
                enemybullets = pygame.sprite.Group()
                powerups = pygame.sprite.Group()
                BosShip = BossShip()
                enemyfleet = EnemyShip()
                player = Player()
                Blitz_sprites.add(player)
                # number of enemies
                for i in range(10):
                    newmob()
                # scoreboard
                score = 0
                # start DA MUSIC!
                pygame.mixer.music.play(loops=-1)
                pygame.display.flip()

            if game_over:
                show_gameover_screen()
                # pygame.display.flip()
            if victory:
                show_victory_screen()

            # loop at right fps
            clock.tick(FPS)
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            # Update
            Blitz_sprites.update()

            # collisionchecks
            collision_checks()
            death_expl = Explosion(player.rect.center, "player")
            # if the player died and exposion finished playing
            if player.lives == 0 and not death_expl.alive():
                game_over = True


            # enemyspawner that takes points in consideration
            if score >= enemyfleet.enemyspawn + 500 and not bossbattle:
                for i in range(1):
                    enemyfleet.distance += 100
                    enemymob()
                    enemyfleet.enemyspawn = score

            # BOSS BATTLE!
            if score >= 1000 and not bossbattle:
                Blitz_sprites.remove(enemyship)
                Blitz_sprites.remove(mobs)
                mobs.empty()
                enemyship.empty()
                Blitz_sprites.add(BosShip)
                bossbattle = True
            if bossbattle:
                Blitz_sprites.remove(enemyship)
                Blitz_sprites.remove(mobs)
                mobs.remove()
                enemyship.remove()

            # Draw / Render
            self.screen.fill(BLACK)
            background.draw(self.screen)
            Blitz_sprites.draw(self.screen)
            draw_text(self.screen, str(score), 18, W / 2, 10)
            draw_text(self.screen, "Space Pirate " + Name, 12, 120, 10)
            # draw shield, only if you have shield
            if player.shield > 0:
                draw_shield_bar(self.screen, W - 80, H - 70, player.shield)
            # draw power up, only if you have an active powerup
            if player.powerbar > 0:
                draw_powerup_bar(self.screen, W - W + 10, H - 70, player.powerbar)
            # draw bossbar, only when bossbattle
            if bossbattle:
                draw_bosshield_bar(self.screen, W / 2 + 40, 10, BosShip.shield)
            draw_lives(self.screen, W - (W - 100), H - H + 70, player.lives, player_minilives)
            # --- Hiding the mouse
            pygame.mouse.set_visible(False)
            # --- updating screen
            pygame.display.flip()

        # Close the window and quit.
        done = True





def Start(ext_screen, ext_name):
    global screen, Name
    BLITZ = Blitz(ext_screen)
    screen = ext_screen
    Name = ext_name
    BLITZ.blitz_Game()
