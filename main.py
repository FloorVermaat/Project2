import pygame as pg
import pygame as pygame
from settings import *


#CTT Import


#Import CTT Minigame



class Main:
    def __init__(self):
        # initialize game window, etc

        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
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


        #BLITZ = Blitz(screen)
        #BLITZ.blitz_Game()

    def select_Minigame(self):
        global intro_screen, Worldselect
        self.BlitzButton = pygame.Rect(W / 2 - 70, H / 2 - 300, 140, 32)
        self.ClimbButton = pygame.Rect(W / 2 - 250, H / 2 - 200, 500, 32)
        self.RaceButton = pygame.Rect(W / 2 - 70, H / 2 - 100, 140, 32)
        self.ShootButton = pygame.Rect(W / 2 - 70, H / 2 + 150 - 50, 140, 32)
        self.EvadeButton = pygame.Rect(W / 2 - 70, H / 2 + 200 - 50, 140, 32)
        done = False
        while not done:
            self.clock.tick(FPS)
            self.screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if self.BlitzButton.collidepoint(pygame.mouse.get_pos()):
                    #

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If user clicks the Blitz button:
                    if self.BlitzButton.collidepoint(event.pos):
                        M.load_Blitz()
                        done = True
                    if self.ClimbButton.collidepoint(event.pos):
                        M.load_CTT()
                        done = True
                    if self.RaceButton.collidepoint(event.pos):
                        pass
                    if self.ShootButton.collidepoint(event.pos):
                        pass
                    if self.EvadeButton.collidepoint(event.pos):
                        pass

            # Blit the boxes
            pygame.draw.rect(self.screen, BLACK, self.BlitzButton)
            pygame.draw.rect(self.screen, BLACK, self.ClimbButton)
            pygame.draw.rect(self.screen, BLACK, self.RaceButton)
            pygame.draw.rect(self.screen, BLACK, self.ShootButton)
            pygame.draw.rect(self.screen, BLACK, self.EvadeButton)
            # Background of the boxes
            pygame.draw.rect(self.screen, WHITE, self.BlitzButton, 5)
            pygame.draw.rect(self.screen, WHITE, self.ClimbButton, 5)
            pygame.draw.rect(self.screen, WHITE, self.RaceButton, 5)
            pygame.draw.rect(self.screen, WHITE, self.ShootButton, 5)
            pygame.draw.rect(self.screen, WHITE, self.EvadeButton, 5)

            # Draw text on the boxes
            self.draw_text(self.screen, "Blitz", 25, self.BlitzButton.x + 70, self.BlitzButton.y + 0)
            self.draw_text(self.screen, "Climb The Tower", 25, self.ClimbButton.x + 250, self.ClimbButton.y + 0)

            # Flip the screen
            pygame.display.flip()








      waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                pressed = pg.key.get_pressed()
                if pressed[pg.K_b]:
                    print("b is pressed")
                    waiting = False
                    M.load_Blitz()

                elif pressed[pg.K_c]:
                    print("c is pressed")
                    waiting = False
                    M.load_CTT()



M = Main()
Name = M.name_input_screen()
print(Name)
M.select_Minigame()