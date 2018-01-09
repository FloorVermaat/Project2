import pygame as pg
import pygame as pygame
from settings import *
from Sprites import *
import sys
import importlib


#CTT Import


#Import CTT Minigame



class Main:
    def __init__(self):
        # initialize game window, etc

        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

    # drawing text on screen
    def draw_text(self, surf, text, size, x, y):
        font_name = pygame.font.Font("Blitz/8.TTF", size)
        text_surface = font_name.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)


    def name_input_screen(self):
        font = pygame.font.Font("Blitz/8.TTF", 16)
        input_box = pygame.Rect(W / 2 - 100, H / 2 - 50, 140, 32)
        input_boxbackground = input_box
        color_inactive = pygame.Color('lightskyblue3')
        color_active = GREEN
        color = color_inactive
        active = False
        text = ''
        level_nameInput = False

        while not level_nameInput:
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
            pygame.draw.rect(self.screen, WHITE, input_boxbackground)
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            self.draw_text(self.screen, "The Number One", 64, W / 2, 50)
            self.draw_text(self.screen, "Insert Name", 30, W / 2, 200)
            self.draw_text(self.screen, "Name has to be atleast 3 characters long", 15, W / 2, H / 2 + 50)
            # Blit the input_box rect.
            pygame.draw.rect(self.screen, color, input_box, 5)
            pygame.display.flip()
            self.clock.tick(FPS)

    def load_CTT(self):
        import CTT.main as CTT
        #CTT.init(self.screen)
        CTT.CTT(self.screen)

    def load_Blitz(self):
            import Blitz.main as Blitz
            Blitz.Start(self.screen, Name)

    def load_SR(self):
        import SR.main as SR
        SR.SR(self.screen)

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
        self.ExitPlanet = ExitPlanet()
        self.MainGame_sprites.add(self.ExitPlanet)

    def select_Minigame(self):
        self.load_Planets()
        done = False
        while not done:
            self.clock.tick(FPS)
            self.screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                # Mouse over actions
                if self.BlitzPlanet.rect.collidepoint(pygame.mouse.get_pos()):
                    self.BlitzPlanet.active = True
                else:
                    self.BlitzPlanet.active = False

                if self.ClimbPlanet.rect.collidepoint(pygame.mouse.get_pos()):
                    self.ClimbPlanet.active = True
                else:
                    self.ClimbPlanet.active = False

                if self.RacePlanet.rect.collidepoint(pygame.mouse.get_pos()):
                    self.RacePlanet.active = True
                else:
                    self.RacePlanet.active = False

                if self.ShootPlanet.rect.collidepoint(pygame.mouse.get_pos()):
                    self.ShootPlanet.active = True
                else:
                    self.ShootPlanet.active = False

                if self.EvadePlanet.rect.collidepoint(pygame.mouse.get_pos()):
                    self.EvadePlanet.active = True
                else:
                    self.EvadePlanet.active = False

                if self.ExitPlanet.rect.collidepoint(pygame.mouse.get_pos()):
                    self.ExitPlanet.active = True
                else:
                    self.ExitPlanet.active = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If user clicks the Blitz button:
                    if self.BlitzPlanet.rect.collidepoint(event.pos):
                        M.load_Blitz()

                    if self.ClimbPlanet.rect.collidepoint(event.pos):
                        M.load_CTT()

                    if self.RacePlanet.rect.collidepoint(event.pos):
                        M.load_SR()

                    if self.ShootPlanet.rect.collidepoint(event.pos):
                        pass

                    if self.EvadePlanet.rect.collidepoint(event.pos):
                        pass

                    if self.ExitPlanet.rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()


            # Draw text on the boxes
            self.draw_text(self.screen, "Blitz", 14, self.BlitzPlanet.rect.x + self.BlitzPlanet.rect.w / 2,
                           self.BlitzPlanet.rect.y - 40)
            self.draw_text(self.screen, "Climb The Tower", 14, self.ClimbPlanet.rect.x + self.ClimbPlanet.rect.w / 2,
                           self.ClimbPlanet.rect.y - 40)
            self.draw_text(self.screen, "Space Race", 14, self.RacePlanet.rect.x + self.RacePlanet.rect.w / 2,
                           self.RacePlanet.rect.y - 40)
            self.draw_text(self.screen, "Space Escape", 14, self.EvadePlanet.rect.x + self.EvadePlanet.rect.w / 2,
                           self.EvadePlanet.rect.y - 40)
            self.draw_text(self.screen, "Space Shooter", 14, self.ShootPlanet.rect.x + self.ShootPlanet.rect.w / 2,
                           self.ShootPlanet.rect.y - 40)
            self.draw_text(self.screen, "Exit", 14, self.ExitPlanet.rect.x + self.ExitPlanet.rect.w / 2,
                           self.ExitPlanet.rect.y - 40)


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



M = Main()
Name = M.name_input_screen()
print(Name)
M.select_Minigame()