from setting import *
import setting as set

fontname = pygame.font.match_font('arial')
font1 = pygame.font.Font(fontname, 28)


class Text(pygame.sprite.Sprite):
    def __init__(self, text, font, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(text, True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, surf):
        a, b = pygame.mouse.get_pos()
        if self.rect.x <= a <= self.rect.right and self.rect.y <= b <= self.rect.bottom:
            pygame.draw.rect(surf, RED, (self.rect.x - 5, self.rect.y - 5, self.rect.width + 10, self.rect.height + 10), 2)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.image.set_colorkey(BLACK)
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
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_img):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(set.player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.radius = 21
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius, 2)
        self.rect.bottom = HEIGHT - 10
        self.speedx = 5
        self.shield = 100
        self.shoot_delay = 250
        self.last_shoot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius, 2)
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        if self.power >= 2 and pygame.time.get_ticks() - self.power_timer > POWERUP_TIME:
            self.power -= 1
            self.power_timer = pygame.time.get_ticks()
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if key[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key[pygame.K_SPACE]:
            self.shoot()
        if self.rect.right > WIDTH - 5:
            self.rect.right = WIDTH
        if self.rect.left < 5:
            self.rect.left = 5

    def shoot(self):
        now = pygame.time.get_ticks()
        if now-self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top, bullet_img1)
                all_sprite.add(bullet)
                bullets.add(bullet)
            elif self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery, bullet_img2)
                bullet2 = Bullet(self.rect.right, self.rect.centery, bullet_img2)
                all_sprite.add(bullet1)
                all_sprite.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
            if set.sound:
                set.shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT + 200)

    def powerup(self):
        self.power += 1
        self.power_timer = pygame.time.get_ticks()


class Mob(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = random.choice(meteror_images)
        #self.image_original=pygame.image.load(path.join(img_dir,"meteorBrown_med1.png"))
        self.image_original.set_colorkey(BLACK)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        #pygame.draw.circle(self.image_original,YELLOW, self.rect.center, self.radius, 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < - 25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            self.speedy = random.randrange(1, 8)

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_original, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect.center = old_center


class Image(pygame.sprite.Sprite):

    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def drawr(self, surf):
        pygame.draw.rect(surf, GREEN, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 4)

    def change(self, changeimg):
        self.image = changeimg


class Alien1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(path.join(img_dir, "ship (16).png")), (88, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.y = -100
        self.radius = 42
        self.velx = random.choice([-1, -2, -3, -4, 1, 2, 3, 4])
        self.vely = random.choice([-1, -2, -3, -4, 1, 2, 3, 4])
        self.last_shoot = pygame.time.get_ticks()
        self.health = 400

    def update(self):
        if self.rect.top < 30:
            self.rect.y += 1
        elif self.rect.top >= 30:
            now = pygame.time.get_ticks()
            if now - self.last_shoot > random.randrange(1000, 3000):
                bullet = AlienBullet1(self.rect.centerx, self.rect.bottom)
                bullet1 = AlienBullet1(self.rect.left, self.rect.centery + self.rect.width)
                bullet2 = AlienBullet1(self.rect.right, self.rect.centery + self.rect.width)
                all_sprite.add(bullet)
                all_sprite.add(bullet1)
                all_sprite.add(bullet2)
                alien_bullet_sprite.add(bullet)
                alien_bullet_sprite.add(bullet1)
                alien_bullet_sprite.add(bullet2)
                self.last_shoot = now
            self.rect.x += self.velx
            self.rect.y += self.vely
            if self.velx < 0 and self.rect.x + self.velx < 10:
                self.rect.x = 10
                self.velx = random.choice([1, 2, 3, 4])
                self.vely = random.choice([-1, -2, -3, -4, 1, 2, 3, 4])
            elif self.velx > 0 and self.rect.right + self.velx > WIDTH - 10:
                self.rect.right = WIDTH - 10
                self.velx = random.choice([-1, -2, -3, -4])
                self.vely = random.choice([-1, -2, -3, -4, 1, 2, 3, 4])
            if self.vely < 0 and self.rect.top + self.vely < 30:
                self.rect.top = 30
                self.vely = random.choice([1, 2, 3, 4])
                self.velx = random.choice([-1, -2, -3, -4, 1, 2, 3, 4])
            elif self.vely > 0 and self.rect.bottom + self.vely > 300:
                self.rect.bottom = 300
                self.vely = random.choice([-1, -2, -3, -4])
                self.velx = random.choice([-1, -2, -3, -4, 1, 2, 3, 4])
        #pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        pygame.draw.rect(screen, WHITE, (self.rect.x - 2, self.rect.y - 10 - 2, self.rect.width + 4, 9), 2)
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, self.rect.width * self.health / 400, 5))


class AlienBullet1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = alien_bomb
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self):
        self.rect.y += 10
        if self.rect.top > HEIGHT:
            self.kill()
