import os





# game graphics
spaceship_image = pygame.image.load(os.path.join(img_folder, "64_spaceship.png")).convert_alpha()
player_lives = pygame.image.load(os.path.join(img_folder, "lives.png")).convert_alpha()
player_minilives = pygame.transform.scale(player_lives, (25, 19))
bullet_image = pygame.image.load(os.path.join(img_folder, "laserRed.png")).convert_alpha()
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

shoot_img_orig = pygame.image.load(os.path.join(img_folder, "shoot_powerup.png")).convert_alpha()
shield_img_orig = pygame.image.load(os.path.join(img_folder, "shield_powerup.png")).convert_alpha()
shield_img = pygame.transform.scale(shield_img_orig, (35, 35))
shoot_img = pygame.transform.scale(shoot_img_orig, (35, 35))
powerup_img = {}
powerup_img["shoot"] = shoot_img
powerup_img["shield"] = shield_img
