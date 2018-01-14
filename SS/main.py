import pygame as pg
import sys
from random import *
from os import path
from SS.settings import *
vec = pg.math.Vector2

# tijdelijk
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


# sprites
def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                Bullet(self.game, pos, dir)
                choice(self.game.shoot_sounds['gun']).play()



    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT
        self.rect.center = self.hit_rect.center


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        # self.vel = vec(0, 0)
        # self.acc = vec(0, 0)
        self.speedy = random.randrange(-5, 5)
        self.speedx = random.randrange(-5, 5)
        self.rect.center = self.pos
        self.rot = 0
        self.rot_speed = random.randrange(-6, 6)
        self.health = MOB_HEALTH


    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = self.rot + self.rot_speed
            if self.rot >= 360:
                self.rot = 1
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        # self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.rot = self.rot + self.rot_speed
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        # self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
        # self.acc += self.vel * -1
        # self.vel += self.acc * self.game.dt
        # self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.pos.x += self.speedx
        self.pos.y += self.speedy
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()
            choice(self.game.mob_hit_sounds['explosion']).play()
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE



# main

#hud functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.running = True

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = 'SS/'
        img_folder = path.join(game_folder, 'img')
        sound_folder = path.join(game_folder, 'sound')
        music_folder = path.join(game_folder, 'music')
        self.title_font = path.join(img_folder, 'ALBA.TTF')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img= pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        # sound loading
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.shoot_sounds = {}
        self.shoot_sounds['gun'] = []
        for sound in SHOOT_SOUND:
            self.shoot_sounds['gun'].append(pg.mixer.Sound(path.join(sound_folder, sound)))
        self.mob_hit_sounds = {}
        self.mob_hit_sounds['explosion'] = []
        for sound in MOB_HIT_SOUND:
            self.mob_hit_sounds['explosion'].append(pg.mixer.Sound(path.join(sound_folder, sound)))
        for sound in self.shoot_sounds['gun']:
            sound.set_volume(0.1)


    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.score = 0
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
        self.paused = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            # if mode = 'story':
                #if self.score > 2500:
                    #you win
            # if mode = 'survival':
            if self.score >= 0:
                while len(self.mobs) < 6:
                    Mob(self, random.randrange(0, WIDTH), random.randrange(0, HEIGHT))
                    self.score += MOB_SCORE
            if self.score > 1000:
                while len(self.mobs) < 12:
                    Mob(self, random.randrange(0, WIDTH), random.randrange(0, HEIGHT))
                    self.score += MOB_SCORE
            if self.score > 2500:
                while len(self.mobs) < 18:
                    Mob(self, random.randrange(0, WIDTH), random.randrange(0, HEIGHT))
                    self.score += MOB_SCORE
            if self.score > 4000:
                while len(self.mobs) < 26:
                    Mob(self, random.randrange(0, WIDTH), random.randrange(0, HEIGHT))
                    self.score += MOB_SCORE
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        hits = pg.sprite.spritecollide(self.player, self.mobs, True, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        # if hits:
            # self.player.pos += vec(MOB_KNOCKBACK, 0).rotate (-hits[0].rot)
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)

        hits = pg.sprite.spritecollide(self.player, self.bullets, True, collide_hit_rect)
        for hit in hits:
            self.player.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False


    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(BACKGROUNDIMAGE, (0, 0))
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.all_sprites.draw(self.screen)
            if isinstance(sprite, Mob):
                sprite.draw_health()


        #pg.draw.rect(self.screen, WHITE, self.player.hit_rect , 2)
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_text(str(self.score), self.title_font, 40, RED, 1175, 15)
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, 200, align="center")
            self.draw_text("Press P to continue", self.title_font, 75, WHITE,
                           WIDTH / 2, 350, align="center")

        pg.display.flip()

    def events(self):
        global DONE
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_ESCAPE:
                    self.running = False


    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text("SPACE SHOOTER", self.title_font, 150, RED,
                       WIDTH / 2, 150, align="center")
        self.draw_text("Use WASD or ARROW keys to move", self.title_font, 50, WHITE
                       , WIDTH / 2, 300, align="center")
        self.draw_text("Press SPACEBAR to shoot", self.title_font, 50, WHITE,
                       WIDTH / 2, 375, align="center")
        self.draw_text("Press P to pause", self.title_font, 50, WHITE,
                       WIDTH / 2, 450, align="center")
        self.draw_text("Press ESCAPE or Q to quit", self.title_font, 50, WHITE,
                       WIDTH / 2, 525, align="center")
        self.draw_text("Press R to start", self.title_font, 50, WHITE,
                       WIDTH / 2, 600, align="center")
        pg.display.flip()
        self.wait_for_key()
        # pass

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 200, RED,
                       WIDTH / 2, 300, align="center")
        self.draw_text("Press R KEY to try again", self.title_font, 75, WHITE,
                       WIDTH / 2, 450, align="center")
        self.draw_text("score = " + str(self.score), self.title_font, 75, WHITE,
                       WIDTH / 2, 550, align="center")
        self.draw_text("Press ESC or R to quit", self.title_font, 75, WHITE,
                      WIDTH / 2, 650, align="center")
        pg.display.flip()
        self.wait_for_key()
        #pass

    def show_win_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("You WIN!!!", self.title_font, 200, RED,
                       WIDTH / 2, 300, align="center")
        self.draw_text("Press R KEY to try again", self.title_font, 75, WHITE,
                       WIDTH / 2, 450, align="center")
        self.draw_text("score = " + str(self.score), self.title_font, 75, WHITE,
                       WIDTH / 2, 550, align="center")
        self.draw_text("Press ESC or R to quit", self.title_font, 75, WHITE,
                       WIDTH / 2, 650, align="center")
        pg.display.flip()
        self.wait_for_key()
        # pass

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        waiting = False
                    if event.key == pg.K_q or event.key == pg.K_ESCAPE:
                        pg.mixer.music.fadeout(1000)
                        self.running = False
                        waiting = False

def SS(screen, story):
    print(story)
    # create the game object
    g = Game(screen)
    g.show_start_screen()
    # pg.mixer.music.load(path.join(sound_folder, 'music.mp3'))
    # pg.mixer.music.play(-1)
    while g.running:
        g.new()
        g.run()
        g.show_go_screen()

