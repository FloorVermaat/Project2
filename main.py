import pygame as pg
import pygame as pygame
from settings import *
from Sprites import *
import sys
import importlib


class Main:
    def __init__(self, autoload = 0):
        # initialize game window, etc

        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()
        self.running = True
        self.background = Background()
        self.font_name = pygame.font.match_font(FONT_NAME)

        if autoload == 1: #Load Climb The Tower
            self.load_CTT()
        elif autoload == 2: #Load Blitz
            self.load_Blitz()
        elif autoload == 3: #Load SR
            self.load_SR()
        elif autoload == 4: #Load SE
            self.load_SE()
        elif autoload == 5: #Load SS
            self.load_SS()

    # drawing text on screen
    def draw_text(self, surf, text, size, x, y, color):
        font_name = pygame.font.Font("Blitz/8.TTF", size)
        text_surface = font_name.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def Credits_screen(self):
        done = False
        movement = 0
        while not done:
            # moving background
            self.background.draw(self.screen, 0)
            movement_down = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if movement_down:
                movement -= 5
                #if movement > 1000:

            self.draw_text(self.screen, "The Number One", 64, W / 2, 50 + movement, WHITE)
            self.draw_text(self.screen, "Insert Name", 30, W / 2, 200 + movement, WHITE)
            self.draw_text(self.screen, "Name has to be atleast 3 characters long", 15, W / 2, H / 2 + 50 + movement, WHITE)

            pygame.display.flip()
            self.clock.tick(FPS)


    def name_input_screen(self):
        # start da music
        pygame.mixer.music.load(os.path.join(snd_folder, "One_impact.wav"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=1)

        font = pygame.font.Font("Blitz/8.TTF", 16)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = GREEN
        color = color_inactive
        active = False
        text = ''
        level_nameInput = False
        movement_down = False
        Number_mov = True
        movement = 0
        background_mov = 0
        number_mov_speed = 0
        Title_mov = True
        Title_mov_speed = 0
        last_tick = pygame.time.get_ticks()

        while not level_nameInput:
            input_box = pygame.Rect(W / 2 - 100, H / 2 - 50 + movement, 140, 32)
            input_boxbackground = input_box
            # moving background
            self.background.draw(self.screen, background_mov)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(text) >= 3 or event.key == pygame.K_KP_ENTER and len(text) >= 3:
                        pygame.mixer.music.load(os.path.join(snd_folder, "Takeoff.wav"))
                        movement_down = True
                        pygame.mixer.music.play(loops=1)
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

            if movement_down and not Number_mov:
                background_mov += 1
                movement += 5
                if movement > 1000:
                    return text
            if Number_mov:
                number_mov_speed += 16
                if number_mov_speed >= 2100:
                    number_mov_speed = 2100
                    if pygame.time.get_ticks() - last_tick > 4000:
                        Number_mov = False

            if not Number_mov:
                Title_mov_speed -= 2
                if Title_mov_speed <= -220:
                    Title_mov_speed = -220

            # Render the current text.
            txt_surface = font.render(text, True, BLACK)
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            input_boxbackground.w = width

            self.draw_text(self.screen, "The Number", 64, W / 2 - 100, 300 + movement + Title_mov_speed, WHITE)
            self.draw_text(self.screen, "One", 64, W / 2 + 336, -1800 + movement + number_mov_speed + Title_mov_speed, RED)
            # draw input box if not pressed enter
            if not movement_down:
                if pygame.time.get_ticks() - last_tick > 6000:
                    pygame.draw.rect(self.screen, WHITE, input_boxbackground)
                    pygame.draw.rect(self.screen, color, input_box, 5)
                    self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5 + movement))
                    self.draw_text(self.screen, "Insert Name And Press Enter", 30, W / 2, 200 + movement, WHITE)
                    self.draw_text(self.screen, "Name has to be atleast 3 characters long", 15, W / 2, H / 2 + 50 + movement, WHITE)
            else:
                self.draw_text(self.screen, "Insert Name And Press Enter", 30, W / 2, 200 + movement, WHITE)
                self.draw_text(self.screen, "Name has to be atleast 3 characters long", 15, W / 2,
                               H / 2 + 50 + movement, WHITE)

            pygame.display.flip()
            self.clock.tick(FPS)

    def load_CTT(self):
        import CTT.main as CTT
        #CTT.init(self.screen)
        CTT.CTT(self.screen)

    def load_Blitz(self):
            import Blitz.main as Blitz
            Blitz.Start(self.screen, Name, self.MainSpaceship.image_orig)

    def load_SR(self):
        import SR.main as SR
        SR.SR(self.screen)

    def load_SS(self):
        import SS.main as SS
        SS.SS(self.screen)

    def load_SE(self):
        import SE.main as SE
        SE.Escape_Game(self.screen)

    # loading the planets to the spritegroup
    def load_Planets(self):
        self.MainGame_sprites = pg.sprite.Group()
        self.BlitzPlanet = BlitzPlanet()
        self.MainGame_sprites.add(self.BlitzPlanet)
        self.ClimbPlanet = ClimbPlanet()
        self.MainGame_sprites.add(self.ClimbPlanet)
        self.RacePlanet = RacePlanet()
        self.MainGame_sprites.add(self.RacePlanet)
        self.ShootPlanet = ShootPlanet()
        self.MainGame_sprites.add(self.ShootPlanet)
        self.EvadePlanet = EvadePlanet()
        self.MainGame_sprites.add(self.EvadePlanet)
        self.CreditsPlanet = CreditsPlanet()
        self.MainGame_sprites.add(self.CreditsPlanet)
        self.BlackHolePlanet = BlackHolePlanet()
        self.MainGame_sprites.add(self.BlackHolePlanet)
        self.MainSpaceship = MainPlayer(W / 2, H - 200)
        self.MainGame_sprites.add(self.MainSpaceship)


    def MouseOver_Actions(self):
        if self.BlitzPlanet.rect.colliderect(self.MainSpaceship.rect) or \
                self.BlitzPlanet.rect.collidepoint(pygame.mouse.get_pos()):
            self.BlitzPlanet.active = True
        else:
            self.BlitzPlanet.active = False

        if self.ClimbPlanet.rect.colliderect(self.MainSpaceship.rect) or \
                self.ClimbPlanet.rect.collidepoint(pygame.mouse.get_pos()):
            self.ClimbPlanet.active = True
        else:
            self.ClimbPlanet.active = False

        if self.RacePlanet.rect.colliderect(self.MainSpaceship.rect) or \
                self.RacePlanet.rect.collidepoint(pygame.mouse.get_pos()):
            self.RacePlanet.active = True
        else:
            self.RacePlanet.active = False

        if self.ShootPlanet.rect.colliderect(self.MainSpaceship.rect) or \
                self.ShootPlanet.rect.collidepoint(pygame.mouse.get_pos()):
            self.ShootPlanet.active = True
        else:
            self.ShootPlanet.active = False

        if self.EvadePlanet.rect.colliderect(self.MainSpaceship.rect) or \
                self.EvadePlanet.rect.collidepoint(pygame.mouse.get_pos()):
            self.EvadePlanet.active = True
        else:
            self.EvadePlanet.active = False

        if self.CreditsPlanet.rect.colliderect(self.MainSpaceship.rect) or \
                self.CreditsPlanet.rect.collidepoint(pygame.mouse.get_pos()):
            self.CreditsPlanet.active = True
        else:
            self.CreditsPlanet.active = False

        if self.BlackHolePlanet.rect.colliderect(self.MainSpaceship.rect) or \
                self.BlackHolePlanet.rect.collidepoint(pygame.mouse.get_pos()):
            self.BlackHolePlanet.active = True
        else:
            self.BlackHolePlanet.active = False

    def select_Minigame(self):
        self.load_Planets()
        done = False
        while not done:
            self.screen.fill(BLACK)
            self.background.draw(self.screen, 0)
            self.clock.tick(FPS)
            self.MouseOver_Actions()
            # Loading game actions
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                # If the user clicks on the planets they load with this
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.BlitzPlanet.rect.collidepoint(event.pos):
                        M.load_Blitz()

                    if self.ClimbPlanet.rect.collidepoint(event.pos):
                        M.load_CTT()

                    if self.RacePlanet.rect.collidepoint(event.pos):
                        M.load_SR()

                    if self.ShootPlanet.rect.collidepoint(event.pos):
                        M.load_SS()

                    if self.EvadePlanet.rect.collidepoint(event.pos):
                        M.load_SE()

                    if self.CreditsPlanet.rect.collidepoint(event.pos):
                        self.Credits_screen()

                    if self.BlackHolePlanet.rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

                # If the user presses enter while ship is on the planet they load with this
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if self.BlitzPlanet.rect.colliderect(self.MainSpaceship.rect):
                            M.load_Blitz()
                        if self.ClimbPlanet.rect.colliderect(self.MainSpaceship.rect):
                            M.load_CTT()
                        if self.RacePlanet.rect.colliderect(self.MainSpaceship.rect):
                            M.load_SR()
                        if self.ShootPlanet.rect.colliderect(self.MainSpaceship.rect):
                            M.load_SS()
                        if self.EvadePlanet.rect.colliderect(self.MainSpaceship.rect):
                            M.load_SE()
                        if self.CreditsPlanet.rect.colliderect(self.MainSpaceship.rect):
                            self.Credits_screen()
                        if self.BlackHolePlanet.rect.colliderect(self.MainSpaceship.rect):
                            pygame.quit()
                            sys.exit()



            # Draw text
            self.draw_text(self.screen, "Blitz", 14, self.BlitzPlanet.rect.x + self.BlitzPlanet.rect.w / 2,
                           self.BlitzPlanet.rect.y - 40, WHITE)
            self.draw_text(self.screen, "Climb The Tower", 14, self.ClimbPlanet.rect.x + self.ClimbPlanet.rect.w / 2,
                           self.ClimbPlanet.rect.y - 40, WHITE)
            self.draw_text(self.screen, "Space Race", 14, self.RacePlanet.rect.x + self.RacePlanet.rect.w / 2,
                           self.RacePlanet.rect.y - 40, WHITE)
            self.draw_text(self.screen, "Space Escape", 14, self.EvadePlanet.rect.x + self.EvadePlanet.rect.w / 2,
                           self.EvadePlanet.rect.y - 40, WHITE)
            self.draw_text(self.screen, "Space Shooter", 14, self.ShootPlanet.rect.x + self.ShootPlanet.rect.w / 2,
                           self.ShootPlanet.rect.y - 40, WHITE)
            self.draw_text(self.screen, "Exit", 14, self.BlackHolePlanet.rect.x + self.BlackHolePlanet.rect.w / 2 - 50,
                           self.BlackHolePlanet.rect.y - 25, WHITE)
            self.draw_text(self.screen, "Credits", 14, self.CreditsPlanet.rect.x + self.CreditsPlanet.rect.w / 2,
                           self.CreditsPlanet.rect.y - 40, WHITE)
            self.draw_text(self.screen, "space pirate " + Name + ":", 14, W / 2,
                           H - 140, WHITE)
            self.draw_text(self.screen, "To Play...Fly To A Planet And Press Enter", 14, W / 2,
                           H - 100, WHITE)


            # game loop update
            self.MainGame_sprites.update()

            # gameloop draw
            self.MainGame_sprites.draw(self.screen)

            # Flip the screen
            pygame.display.flip()








#      waiting = True
#        while waiting:
#            self.clock.tick(FPS)
#            for event in pg.event.get():
#                if event.type == pg.QUIT:
#                    waiting = False
#                    self.running = False
#                pressed = pg.key.get_pressed()
#                if pressed[pg.K_b]:
##                    print("b is pressed")
#                    waiting = False
#                    M.load_Blitz()
#
#                elif pressed[pg.K_c]:
#                    print("c is pressed")
#                    waiting = False
#                    M.load_CTT()




M = Main(1)
#Autoload Can be disabled by removing x in Main(x) above
#1 For CTT
#2 For Blitz
#3 For SR
#4 For SE
#5 For SS

Name = M.name_input_screen()
print(Name)
M.select_Minigame()