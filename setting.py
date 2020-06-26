# http://millionthvector.blogspot.de.
# Art from kenny.nl
# http://creativecommons.org/licenses/by-sa/3.0/
import pygame
import sys
from os import path
import random
WIDTH = 480
HEIGHT = 600
PAUSEW = 300
PAUSEH = 300
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (135, 211, 248)
# original cyan(0,255,255)
main_menu = True
menu_init = False
start_game = False
game_init = False
option_init = False
option_start = False
ship_option_init = False
ship_option = False
sm_init = False
sm = False
game_over = False

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "sound")

pygame.init()
pygame.mixer.init()
pygame.display.set_icon(pygame.transform.rotate(pygame.image.load(path.join(img_dir, "playerShip1_blue.png")), 315))
screen = pygame.display.set_mode((WIDTH, HEIGHT))

text_sprites = pygame.sprite.Group()
all_sprite = pygame.sprite.Group()
powerupGroups = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
image_sprite = pygame.sprite.Group()
aliens_sprite = pygame.sprite.Group()
alien_bullet_sprite = pygame.sprite.Group()
bullets_img = ["aliendropping0001.png"]
alien_bomb = pygame.transform.scale(pygame.image.load(path.join(img_dir, random.choice(bullets_img))), (22, 37))

bg = pygame.transform.scale(pygame.image.load(path.join(img_dir, "bg3.png")).convert(), (600, 600))
f = open("player.txt", "r+")
try:
    player_img = pygame.image.load(path.join(img_dir, f.read()))
except:
    player_img = pygame.image.load(path.join(img_dir, "playerShip1_red.png"))
    f.seek(0)
    f.truncate(0)
    f.write("playerShip1_red.png")
f.close()
player_rotated_img = pygame.transform.rotate(pygame.transform.scale(player_img, (45, 38)), 315)
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

bullet_img1 = pygame.image.load(path.join(img_dir, "laserGreen12.png")).convert()
bullet_img2 = pygame.image.load(path.join(img_dir, "laserBlue06.png")).convert()

meteror_images = []
meteror_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png', 'meteorBrown_big4.png',
                'meteorBrown_med1.png', 'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
                'meteorBrown_tiny1.png', 'meteorBrown_tiny2.png',
                'meteorGrey_big1.png', 'meteorGrey_big2.png', 'meteorGrey_big3.png', 'meteorGrey_big4.png',
                'meteorGrey_med1.png', 'meteorGrey_med2.png', 'meteorGrey_small1.png', 'meteorGrey_small2.png',
                'meteorGrey_tiny1.png', 'meteorGrey_tiny2.png']
for img in meteror_list:
    meteror_images.append(pygame.image.load(path.join(img_dir, img)).convert())

powerup_images={}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, "shield_gold.png"))
powerup_images['gun'] = pygame.image.load(path.join(img_dir, "bolt_gold.png"))

explosion_anim={}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (72, 72))
    explosion_anim['lg'].append(img_lg)
    img_sm=pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    im = pygame.image.load(path.join(img_dir, filename)).convert()
    im.set_colorkey(BLACK)
    explosion_anim['player'].append(im)

score = 0
POWERUP_TIME = 5000


running = True

music = pygame.mixer.music.load(path.join(snd_dir, 'AloneAgainst Enemy.ogg'))
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "laser5.ogg"))
click_sound = pygame.mixer.Sound(path.join(snd_dir, "MenuSelection.ogg"))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.7)
off = pygame.transform.scale(pygame.image.load(path.join(img_dir, "mute.png")), (64, 64)).convert()
off.set_colorkey(BLACK)
onn = pygame.transform.scale(pygame.image.load(path.join(img_dir, "sound.png")), (64, 64)).convert()
onn.set_colorkey(BLACK)
f2 = open("music.txt", "r+")
if f2.read() == "0":
    pygame.mixer.music.pause()
elif f2.read() == "1":
    pass
else:
    f2.seek(0)
    f2.truncate(0)
    f2.write("0")
    pygame.mixer.music.pause()
f2.close()
sound = True
f2 = open("sound.txt", "r+")
if f2.read() == "0":
    sound = False
elif f2.read() == "1":
    sound = True
else:
    f2.seek(0)
    f2.truncate(0)
    f2.write("0")
    sound = False
f2.close()
pause = False
pause_button_img = pygame.transform.scale(pygame.image.load(path.join(img_dir, "pause.png")), (50, 50)).convert()
pause_button_img.set_colorkey(BLACK)
play_button_img = pygame.transform.scale(pygame.image.load(path.join(img_dir, "play.png")), (50, 50))
play_button_img.set_colorkey(BLACK)

alien_start = False
alien_start_time = random.randrange(5000, 50000)

