# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 7
# Video link: https://youtu.be/rLrMPg-GCqo
# Splash & End Screens

import pygame as pg
import random
from settings import *
from sprites import *
from pygame import *

class Climb_The_Tower_Game:
    def __init__(self):
        # initialize game window, etc

        #pg.mixer.pre_init(44100, -16, 2, 2048)
        #pg.mixer.init()
        #pg.init()

        #self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        #pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)


        self.spriteArrayTower = []
        i = 1
        while i <= 361:
            self.path = "tower/" + str(i) + ".png"
            #print(i)
            self.spriteArrayTower.append(pg.image.load(self.path).convert_alpha())
            i += 1
            print("Tower Frame #" + str(len(self.spriteArrayTower)))

        #Load Sound Effects
        self.M = Music()

    def new(self):

        self.M.bg.play(loops=-1)

        # start a new game
        self.score = 0
        self.win = False
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.tower = pg.sprite.Group()
        self.platforms_last = pg.sprite.Group()

        self.platforms.spawntimer = 200
        self.platforms_last.rotation = 0
        self.platforms_last.height = 0

        self.tower.i = 0
        while self.tower.i < 500:
            t = Tower(self.spriteArrayTower, 10, self.tower.i)
            self.all_sprites.add(t)
            self.tower.add(t)
            self.tower.i += 1

        self.player = Player(self)
        self.all_sprites.add(self.player)

        for plat in PLATFORM_LIST:
            p = Platform(*plat, RED)
            self.all_sprites.add(p)
            self.platforms.add(p)

        self.run()

    def run(self):
        # Climb_The_Tower_Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Climb_The_Tower_Game Loop - Update
        self.all_sprites.update()

        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                if self.player.land == False:
                    self.M.land1.play()
                    self.player.land = True

        # if player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

            for tower in self.tower:
                tower.rect.y += abs(self.player.vel.y)
                if tower.rect.top >= HEIGHT + 1000:
                    tower.kill()
                    self.tower.i += -1

        # Die!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False


        # spawn new platforms to keep same average number
        while len(self.platforms) < PLATFORMS:
            # Remove the last Platform from the Platform.last group
            self.platforms_last.empty()

            # Rotation Index 100 is about the middle,
            rotation = random.randrange(30, 170)
            while (rotation - self.platforms_last.rotation) in range(-30, 30):
                print("Rotation to close " + str(int(rotation - self.platforms_last.rotation)))
                rotation = random.randrange(0, 200)


            height = random.randrange(-300, -55)
            while (height - self.platforms_last.height) in range(-50,50):
                print("Height to close" + str(int(height - self.platforms_last.height)))
                height = random.randrange(-300, -55)




            p = Platform(rotation, height, GREEN)
            self.platforms.add(p)
            self.all_sprites.add(p)
            self.platforms_last.add(p)

            #Save old rotation
            self.platforms_last.rotation = rotation
            self.platforms_last.height = height


        if self.score >= 250:
            self.win = True
            self.playing = False


    def events(self):
        # Climb_The_Tower_Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_w:
                    self.player.jump()
                    self.M.jump1.play()
                    self.player.land = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.quit()
                    quit()

    def draw(self):
        # Climb_The_Tower_Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Use AD or the Arrow Keys to move left or right!"
                       "Space is used to jump!", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press the c key to start", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("U DED", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press the c key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def show_win_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("U Win", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press the c key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                pressed = pg.key.get_pressed()
                if pressed[pg.K_c]:
                    self.M.bg.stop()
                    print("c is pressed")
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

def CTT():
    CTT = Climb_The_Tower_Game()
    CTT.show_start_screen()
    while CTT.running:
        CTT.new()
        if CTT.win:
            CTT.show_win_screen()
        else:
            CTT.show_go_screen()
    pg.quit()

CTT()