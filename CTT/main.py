import pygame as pg
import random
from CTT.settings import *
from CTT.sprites import *
from pygame import *

class Climb_The_Tower_Game:
    def __init__(self, screen, ship, story):
        #Get Screen from Integration
        self.screen = screen
        self.ship = ship

        self.ship = pg.transform.rotate(self.ship, 90)
        self.ship = pg.transform.scale2x(self.ship)
        self.ship = pg.transform.scale2x(self.ship)


        self.story = story

        # initialize game window, etc

        #pg.mixer.pre_init(44100, -16, 2, 2048)
        #pg.mixer.init()
        #pg.init()

        #self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        #pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)




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
        self.tower.d = 0


        self.all_sprites.add(Background(self.spriteArrayBackground))

        while self.tower.i < 500:
            t = Tower(self.spriteArrayTower, 10, self.tower.i)

            if self.tower.i >25 and self.story:
                t = Tower(self.spriteArrayTower, 10, self.tower.i, self.ship)
                self.tower.i = 500

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
            #print("FPS: " + str(self.clock.get_fps()))

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
                    self.tower.d += 1
                    tower.kill()
                    print(self.tower.d)


        # Die!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False
            self.M.bg.stop()
            self.M.bg.stop()


        # spawn new platforms to keep same average number
        while len(self.platforms) < PLATFORMS:
            # Remove the last Platform from the Platform.last group
            self.platforms_last.empty()

            # Rotation Index 100 is about the middle,
            rotation = random.randrange(40, 160)
            while (rotation - self.platforms_last.rotation) in range(-30, 30):
                print("Rotation to close " + str(int(rotation - self.platforms_last.rotation)))
                rotation = random.randrange(40, 160)


            height = random.randrange(-280, -55)
            while (height - self.platforms_last.height) in range(-50,50):
                print("Height to close" + str(int(height - self.platforms_last.height)))
                height = random.randrange(-280, -55)




            p = Platform(rotation, height, GREEN)
            self.platforms.add(p)
            self.all_sprites.add(p)
            self.platforms_last.add(p)

            #Save old rotation
            self.platforms_last.rotation = rotation
            self.platforms_last.height = height


        if self.score >= 1000:
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
                if event.key == pg.K_SPACE:
                    self.player.jump()
                    self.M.jump1.play()
                    self.player.land = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    self.M.bg.stop()
                    self.running = False
                    self.playing = False

    def draw(self):
        # Climb_The_Tower_Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)

        if not self.player.djump:
            self.player.draw_cooldown(self.screen, 25, HEIGHT - 50)

        # *after* drawing everything, flip the display
        pg.display.flip()
    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Use AD or the Arrow Keys to move left or right!"
                       "Space is used to jump!", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press the c key to start", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)

        #import imageio
        #imageio.plugins.ffmpeg.download()
        #from moviepy.editor import VideoFileClip
        #clip = VideoFileClip('CTT/assets/retrowave.mp4')
        #clip.preview()




        pg.display.flip()
        self.wait_for_key()

    def show_load_screen(self):
        # game splash/start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("The Game Is Loading Right now!"
                       "", 22, WHITE, WIDTH / 2, HEIGHT / 2)

        self.draw_text("Please wait while this is being completed", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()

        ##Loading
        self.spriteArrayTower = []

        ProgressBar = 0



        self.spriteArrayBackground = []

        bgi = 50
        while bgi <= 99:
            self.path = "CTT/sprites/city_ash/image-0" + str(bgi) + ".png"
            #print(i)
            self.spriteArrayBackground.append(pg.image.load(self.path).convert_alpha())
            bgi += 1
            print("City Background Frame #" + str(len(self.spriteArrayBackground)))

            ProgressBar += 1
            self.draw_loadProgress(self.screen, ProgressBar, WIDTH / 2 - 250, HEIGHT * 3 / 4 + 50 )
            pg.display.flip()



        while bgi <= 365:
            self.path = "CTT/sprites/city_ash/image-" + str(bgi) + ".png"
            #print(i)
            self.spriteArrayBackground.append(pg.image.load(self.path).convert_alpha())
            bgi += 1
            print("City Background Frame #" + str(len(self.spriteArrayBackground)))

            ProgressBar += 1
            self.draw_loadProgress(self.screen, ProgressBar, WIDTH / 2 - 250, HEIGHT * 3 / 4 + 50 )
            pg.display.flip()


        ti = 1
        while ti <= 361:
            self.path = "CTT/tower/" + str(ti) + ".png"
            #print(i)
            self.spriteArrayTower.append(pg.image.load(self.path).convert_alpha())
            ti += 1
            print("Tower Frame #" + str(len(self.spriteArrayTower)))
            ProgressBar += 1
            self.draw_loadProgress(self.screen, ProgressBar, WIDTH / 2 - 250, HEIGHT * 3 / 4 + 50)
            pg.display.flip()


    def draw_loadProgress(self, surf, pb, x, y):
        bar_length = 500
        bar_height = 20
        fill = (pb / 676) * bar_length
        outline_rect = pg.Rect(x, y, bar_length, bar_height)
        fill_rect = pg.Rect(x, y, fill, bar_height)
        pg.draw.rect(surf, GREEN, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)


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

                if pressed[pg.K_q]:
                    waiting = False
                    self.running = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

def CTT(screen, ship, story=True):
    CTT = Climb_The_Tower_Game(screen, ship, story)
    CTT.show_load_screen()
    CTT.show_start_screen()
    while CTT.running:
        CTT.new()
        if CTT.win:
            CTT.show_win_screen()
        else:
            CTT.show_go_screen()
    CTT.spriteArrayTower = []
    CTT.spriteArrayBackground = []



