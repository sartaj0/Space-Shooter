from sprites import *


def newmob():
    m = Mob()
    mobs.add(m)
    all_sprite.add(m)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 10
    fill = (pct / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for z in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * z
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(fontname, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_logo(surf, a, b, img):
    img_rect = img.get_rect()
    img_rect.x = a
    img_rect.y = b
    surf.blit(img, img_rect)


def menu_screen(surf):
    global text1, options, exit_game, player_rotated_img, score
    screen_fill()
    if not set.menu_init:
        text1 = Text("Start a Game", font1, WIDTH/2, 200)
        options = Text("Options", font1, WIDTH/2, 250)
        exit_game = Text("Exit", font1, WIDTH/2, 300)
        f = open("highestscore.txt", "r")
        score = f.read()
        text_sprites.add(text1)
        text_sprites.add(options)
        text_sprites.add(exit_game)
        text_sprites.draw(surf)
        draw_text(screen, "Space Shooter", 40, WIDTH / 2, HEIGHT - 525)
        draw_text(screen, "All Time Highest Score :"+str(score), 30, WIDTH / 2, HEIGHT - 170)
        draw_logo(screen, 360, HEIGHT - 530, player_rotated_img)
        f.close()
        set.menu_init = True
    else:
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONUP:
            mx, my = pygame.mouse.get_pos()
            if text1.rect.collidepoint(mx, my):
                text_sprites.empty()
                set.main_menu = False
                set.start_game = True
                set.menu_init = False
                if set.sound:
                    click_sound.play()
            elif options.rect.collidepoint(mx, my):
                text_sprites.empty()
                set.main_menu = False
                set.option_start = True
                set.menu_init = False
                if set.sound:
                    click_sound.play()
            elif exit_game.rect.collidepoint(mx, my):
                set.running = False
        elif event.type == pygame.QUIT:
            set.running = False
        text_sprites.update(surf)
        text_sprites.draw(surf)
        draw_text(screen, "Space Shooter", 40, WIDTH / 2, HEIGHT - 525)
        draw_logo(screen, 360, HEIGHT - 530, player_rotated_img)
        draw_text(screen, "All Time Highest Score :" + str(score), 30, WIDTH / 2, HEIGHT - 170)


def start_screen(surf):
    global score, player, death_explosion, pause_button, pause_surface, back_option, music_img, on, f1, sound_img, f2, ons
    global alien_timer, alien1, retry_option, exit_option
    screen_fill()
    if not set.game_init:
        player = Player()
        all_sprite.add(player)
        all_sprite.draw(surf)
        score = 0
        set.game_init = True
        for i in range(8):
            newmob()
        pause_button = Image(pause_button_img, 35, 50)
        image_sprite.add(pause_button)
        image_sprite.draw(surf)
        pause_surface = pygame.Surface((PAUSEW, PAUSEH))
        pause_surface.set_alpha(128)
        pause_surface.fill(CYAN)
        back_option = Text("Go Back To Menu", font1, WIDTH/2, 200)
        retry_option = Text("Try Again", font1, WIDTH / 2, 300)
        exit_option = Text("Exit from Game", font1, WIDTH / 2, 400)
        f1 = open("music.txt", "r+")
        on = f1.read()
        text_sprites.add(back_option)
        f2 = open("sound.txt", "r+")
        ons = f2.read()
        if on == "1":
            music_img = Image(onn, WIDTH / 2 - PAUSEW / 2 + 200, HEIGHT / 2 - PAUSEH / 2 + 110)
        elif on == "0":
            music_img = Image(off, WIDTH / 2 - PAUSEW / 2 + 200, HEIGHT / 2 - PAUSEH / 2 + 110)
        if set.sound:
            sound_img = Image(onn, WIDTH / 2 - PAUSEW / 2 + 200, HEIGHT / 2 - PAUSEH / 2 + 180)
        elif not set.sound:
            sound_img = Image(off, WIDTH / 2 - PAUSEW / 2 + 200, HEIGHT / 2 - PAUSEH / 2 + 180)
        alien_timer = pygame.time.get_ticks()
    elif set.game_init and not set.game_over:
        if not set.alien_start:
            now = pygame.time.get_ticks()
            if now - alien_timer > set.alien_start_time:
                set.alien_start = True
                alien1 = Alien1()
                all_sprite.add(alien1)
        image_sprite.draw(surf)
        all_sprite.draw(surf)
        image_sprite.draw(surf)
        draw_text(screen, str(score), 18, WIDTH / 2, 10)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_lives(screen, WIDTH - 100, 5, player.lives, set.player_mini_img)
        if not set.pause and not set.game_over:
            all_sprite.update()
            hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
            for hit in hits:
                score += 50 - hit.radius
                expl = Explosion(hit.rect.center, 'lg')
                all_sprite.add(expl)
                if random.random() > 0.95:
                    pows = Pow(hit.rect.center)
                    all_sprite.add(pows)
                    powerupGroups.add(pows)
                if not set.alien_start:
                    newmob()
            hits = pygame.sprite.spritecollide(player, alien_bullet_sprite, True)
            for hit in hits:
                player.shield -= 10
                expl = Explosion(hit.rect.center, 'sm')
                all_sprite.add(expl)
                if player.shield <= 0:
                    death_explosion = Explosion(player.rect.center, 'player')
                    all_sprite.add(death_explosion)
                    player.hide()
                    player.lives -= 1
                    player.shield = 100
            if set.alien_start:
                hits = pygame.sprite.spritecollide(alien1, bullets, True, pygame.sprite.collide_circle)
                for hit in hits:
                    alien1.health -= 10
                    score += 50
                    expl = Explosion(hit.rect.center, 'sm')
                    all_sprite.add(expl)
                    if alien1.health <= 0:
                        death_explosion = Explosion(alien1.rect.center, 'player')
                        all_sprite.add(death_explosion)
                        alien1.kill()
                        set.alien_start = False
                        set.alien_start_time = random.randrange(5000, 50000)
                        alien_timer = pygame.time.get_ticks()
                        score += 1000
                        for i in range(8):
                            newmob()
            hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle) # false is used if mob hit player it will disappear or not
            for hit in hits:
                player.shield -= hit.radius * 2
                expl = Explosion(hit.rect.center, 'sm')
                all_sprite.add(expl)
                newmob()
                if player.shield <= 0:
                    death_explosion = Explosion(player.rect.center, 'player')
                    all_sprite.add(death_explosion)
                    player.hide()
                    player.lives -= 1
                    player.shield = 100
            if player.lives == 0 and not death_explosion.alive():
                all_sprite.empty()
                image_sprite.empty()
                powerupGroups.empty()
                bullets.empty()
                mobs.empty()
                pause_button.kill()
                set.game_over = True
                player.kill()
                f1 = open("highestscore.txt", "r+")
                value = int(f1.read())
                if value < int(score):
                    f1.seek(0)
                    f1.truncate(0)
                    f1.write(str(score))
                f1.close()
                f2.close()
                text_sprites.add(back_option)
                text_sprites.add(retry_option)
                text_sprites.add(exit_option)

            hits = pygame.sprite.spritecollide(player, powerupGroups, True)
            for hit in hits:
                if hit.type == 'shield':
                    player.shield += random.randrange(10, 30)
                    if player.shield >= 100:
                        player.shield = 100
                if hit.type == 'gun':
                    player.powerup()

        elif set.pause:
            surf.blit(pause_surface, (WIDTH / 2 - PAUSEW / 2, HEIGHT / 2 - PAUSEH / 2))
            text_sprites.draw(surf)
            draw_text(surf, "Music", 30, WIDTH / 2 - PAUSEW / 2 + 90, HEIGHT / 2 - PAUSEH / 2 + 90)
            draw_text(surf, "Sound", 30, WIDTH / 2 - PAUSEW / 2 + 90, HEIGHT / 2 - PAUSEH / 2 + 160)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and pause_button.alive():
                x, y = event.pos
                if pause_button.rect.collidepoint(x, y) and not set.pause:
                    pause_button.change(play_button_img)
                    set.pause = True
                    text_sprites.add(back_option)
                    image_sprite.add(music_img)
                    image_sprite.add(sound_img)
                elif back_option.rect.collidepoint(x, y):
                    all_sprite.empty()
                    text_sprites.empty()
                    mobs.empty()
                    powerupGroups.empty()
                    player.kill()
                    set.main_menu = True
                    set.start_game = False
                    set.game_init = False
                    set.pause = False
                    set.game_over = False
                    pause_button.kill()
                    music_img.kill()
                    sound_img.kill()
                    pause_button.kill()
                    f1.close()
                    f2.close()
                    set.alien_start = False
                elif pause_button.rect.collidepoint(x, y) and set.pause:
                    set.pause = False
                    pause_button.change(pause_button_img)
                    back_option.kill()
                    music_img.kill()
                    sound_img.kill()
                elif music_img.rect.collidepoint(x, y):
                    if on == "1":
                        f1.seek(0)
                        f1.truncate(0)
                        f1.write("0")
                        music_img.change(off)
                        on = "0"
                        pygame.mixer.music.pause()
                    elif on == "0":
                        f1.seek(0)
                        f1.truncate(0)
                        f1.write("1")
                        on = "1"
                        music_img.change(onn)
                        pygame.mixer.music.unpause()
                elif sound_img.rect.collidepoint(x, y):
                    if ons == "1":
                        f2.seek(0)
                        f2.truncate(0)
                        sound_img.change(off)
                        f2.write("0")
                        ons = "0"
                        set.sound = False
                    elif ons == "0":
                        f2.seek(0)
                        f2.truncate(0)
                        sound_img.change(onn)
                        f2.write("1")
                        ons = "1"
                        set.sound = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p and pause_button.alive():
                if not set.pause:
                    pause_button.change(play_button_img)
                    set.pause = True
                    text_sprites.add(back_option)
                    image_sprite.add(music_img)
                    image_sprite.add(sound_img)
                elif set.pause:
                    set.pause = False
                    pause_button.change(pause_button_img)
                    back_option.kill()
                    music_img.kill()
                    sound_img.kill()
    elif set.game_over:
        surf.blit(pause_surface, (WIDTH / 2 - PAUSEW / 2, HEIGHT / 2 - PAUSEH / 2))
        draw_text(screen, "Your Score " + str(score), 40, WIDTH / 2, HEIGHT / 10)
        draw_text(screen, "!! Game Over !!", 40, WIDTH / 2, 10)
        text_sprites.draw(surf)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if back_option.rect.collidepoint(x, y):
                    text_sprites.empty()
                    set.alien_start = False
                    set.main_menu = True
                    set.game_over = False
                    set.start_game = False
                    set.game_init = False
                    set.pause = False
                elif retry_option.rect.collidepoint(x, y):
                    all_sprite.empty()
                    alien1.kill()
                    set.alien_start = False
                    text_sprites.empty()
                    image_sprite.empty()
                    alien1.kill()
                    set.game_over = False
                    set.start_game = True
                    set.game_init = False
                elif exit_option.rect.collidepoint(x, y):
                    set.running = False


def option_screen(surf):
    global sound_options, player_option, back_option
    screen_fill()
    if not set.option_init:
        sound_options = Text("Sounds and  Music", font1, WIDTH/2, 200)
        player_option = Text("Select a Ship", font1, WIDTH / 2, 250)
        back_option = Text("Back", font1, 35, 25)
        text_sprites.add(back_option)
        text_sprites.add(sound_options)
        text_sprites.add(player_option)
        text_sprites.draw(surf)
        set.option_init = True
    elif set.option_init:
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONUP:
            mx, my = pygame.mouse.get_pos()
            if sound_options.rect.collidepoint(mx, my):
                if set.sound:
                    click_sound.play()
                set.sm = True
                set.option_start = False
                set.option_init = False
                text_sprites.empty()
            elif player_option.rect.collidepoint(mx, my):
                if set.sound:
                    click_sound.play()
                set.option_init = False
                set.option_start = False
                set.ship_option = True
                text_sprites.empty()
            elif back_option.rect.collidepoint(mx, my):
                if set.sound:
                    click_sound.play()
                text_sprites.empty()
                set.option_init = False
                set.option_start = False
                set.main_menu = True
        elif event.type == pygame.QUIT:
            set.running = False
        text_sprites.update(surf)
        text_sprites.draw(surf)


def ship_option_screen(surf):
    global back_option, red1, red2, red3, red4, orange1, orange2, orange3, orange4, f1, orange1, text
    global green1, green4, green3, green2, blue1, blue2, blue3, blue4
    screen_fill()
    if not set.ship_option_init:
        back_option = Text("Back", font1, 35, 25)
        text_sprites.add(back_option)
        text_sprites.draw(surf)
        red1 = Image(pygame.image.load(path.join(img_dir, "playerShip1_red.png")), WIDTH / 2 - 175, HEIGHT / 2 - 210)
        red2 = Image(pygame.image.load(path.join(img_dir, "playerShip2_red.png")), WIDTH / 2 - 60, HEIGHT / 2 - 210)
        red3 = Image(pygame.image.load(path.join(img_dir, "playerShip3_red.png")), WIDTH / 2 + 55, HEIGHT / 2 - 210)
        red4 = Image(pygame.image.load(path.join(img_dir, "ufoRed.png")), WIDTH / 2 + 170, HEIGHT / 2 - 210)
        blue1 = Image(pygame.image.load(path.join(img_dir, "playerShip1_blue.png")), WIDTH / 2 - 175, HEIGHT / 2 - 60)
        blue2 = Image(pygame.image.load(path.join(img_dir, "playerShip2_blue.png")), WIDTH / 2 - 60, HEIGHT / 2 - 60)
        blue3 = Image(pygame.image.load(path.join(img_dir, "playerShip3_blue.png")), WIDTH / 2 + 55, HEIGHT / 2 - 60)
        blue4 = Image(pygame.image.load(path.join(img_dir, "ufoBlue.png")), WIDTH / 2 + 170, HEIGHT / 2 - 60)
        orange1 = Image(pygame.image.load(path.join(img_dir, "playerShip1_orange.png")), WIDTH / 2 - 175, HEIGHT / 2 + 90)
        orange2 = Image(pygame.image.load(path.join(img_dir, "playerShip2_orange.png")), WIDTH / 2 - 60, HEIGHT / 2 + 90)
        orange3 = Image(pygame.image.load(path.join(img_dir, "playerShip3_orange.png")), WIDTH / 2 + 55, HEIGHT / 2 + 90)
        orange4 = Image(pygame.image.load(path.join(img_dir, "ufoYellow.png")), WIDTH / 2 + 170, HEIGHT / 2 + 90)
        green1 = Image(pygame.image.load(path.join(img_dir, "playerShip1_green.png")), WIDTH / 2 - 175, HEIGHT / 2 + 240)
        green2 = Image(pygame.image.load(path.join(img_dir, "playerShip2_green.png")), WIDTH / 2 - 60, HEIGHT / 2 + 240)
        green3 = Image(pygame.image.load(path.join(img_dir, "playerShip3_green.png")), WIDTH / 2 + 55, HEIGHT / 2 + 240)
        green4 = Image(pygame.image.load(path.join(img_dir, "ufoGreen.png")), WIDTH / 2 + 170, HEIGHT / 2 + 240)
        image_sprite.add(red1)
        image_sprite.add(red2)
        image_sprite.add(red3)
        image_sprite.add(red4)
        image_sprite.add(blue1)
        image_sprite.add(blue2)
        image_sprite.add(blue3)
        image_sprite.add(blue4)
        image_sprite.add(green1)
        image_sprite.add(green2)
        image_sprite.add(green3)
        image_sprite.add(green4)
        image_sprite.add(orange1)
        image_sprite.add(orange2)
        image_sprite.add(orange3)
        image_sprite.add(orange4)
        text_sprites.update(surf)
        text_sprites.draw(surf)
        image_sprite.draw(surf)
        f1 = open("player.txt", "r+")
        text = f1.read()
        set.ship_option_init = True
    elif set.ship_option_init:
        if text == "playerShip1_red.png":
            red1.drawr(screen)
        elif text == "playerShip2_red.png":
            red2.drawr(screen)
        elif text == "playerShip3_red.png":
            red3.drawr(screen)
        elif text == "ufoRed.png":
            red4.drawr(screen)
        elif text == "playerShip1_orange.png":
            orange1.drawr(screen)
        elif text == "playerShip2_orange.png":
            orange2.drawr(screen)
        elif text == "playerShip3_orange.png":
            orange3.drawr(screen)
        elif text == "ufoYellow.png":
            orange4.drawr(screen)
        elif text == "playerShip1_blue.png":
            blue1.drawr(screen)
        elif text == "playerShip2_blue.png":
            blue2.drawr(screen)
        elif text == "playerShip3_blue.png":
            blue3.drawr(screen)
        elif text == "ufoBlue.png":
            blue4.drawr(screen)
        elif text == "playerShip1_green.png":
            green1.drawr(screen)
        elif text == "playerShip2_green.png":
            green2.drawr(screen)
        elif text == "playerShip3_green.png":
            green3.drawr(screen)
        elif text == "ufoGreen.png":
            green4.drawr(screen)
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONUP:
            mx, my = pygame.mouse.get_pos()
            if back_option.rect.collidepoint(mx, my):
                if set.sound:
                    click_sound.play()
                text_sprites.empty()
                image_sprite.empty()
                set.ship_option_init = False
                set.ship_option = False
                set.option_start = True
                f1.close()
                image_sprite.empty()
            if red1.rect.collidepoint(mx, my):
                playerupdate("playerShip1_red.png")
            elif red2.rect.collidepoint(mx, my):
                playerupdate("playerShip2_red.png")
            elif red3.rect.collidepoint(mx, my):
                playerupdate("playerShip3_red.png")
            elif red4.rect.collidepoint(mx, my):
                playerupdate("ufoRed.png")
            elif orange1.rect.collidepoint(mx, my):
                playerupdate("playerShip1_orange.png")
            elif orange2.rect.collidepoint(mx, my):
                playerupdate("playerShip2_orange.png")
            elif orange3.rect.collidepoint(mx, my):
                playerupdate("playerShip3_orange.png")
            elif orange4.rect.collidepoint(mx, my):
                playerupdate("ufoYellow.png")
            elif green1.rect.collidepoint(mx, my):
                playerupdate("playerShip1_green.png")
            elif green2.rect.collidepoint(mx, my):
                playerupdate("playerShip2_green.png")
            elif green3.rect.collidepoint(mx, my):
                playerupdate("playerShip3_green.png")
            elif green4.rect.collidepoint(mx, my):
                playerupdate("ufoGreen.png")
            elif blue1.rect.collidepoint(mx, my):
                playerupdate("playerShip1_blue.png")
            elif blue2.rect.collidepoint(mx, my):
                playerupdate("playerShip2_blue.png")
            elif blue3.rect.collidepoint(mx, my):
                playerupdate("playerShip3_blue.png")
            elif blue4.rect.collidepoint(mx, my):
                playerupdate("ufoBlue.png")
        elif event.type == pygame.QUIT:
            set.running = False
        text_sprites.update(surf)
        text_sprites.draw(surf)
        image_sprite.draw(surf)


def soundandmusic(surf):
    screen_fill()
    global back_option, music_img, on, f1, sound_img, ons, f2
    if not set.sm_init:
        back_option = Text("Back", font1, 35, 25)
        f1 = open("music.txt", "r+")
        on = f1.read()
        f2 = open("sound.txt", "r+")
        ons = f2.read()
        text_sprites.add(back_option)
        if on == "1":
            music_img = Image(onn, WIDTH / 2 - 100, HEIGHT / 2 - 80)
        elif on == "0":
            music_img = Image(off, WIDTH / 2 - 100, HEIGHT / 2 - 80)
        if set.sound:
            sound_img = Image(onn, WIDTH / 2 + 100 , HEIGHT / 2 - 80)
        elif not set.sound:
            sound_img = Image(off, WIDTH / 2 + 100 , HEIGHT / 2 - 80)
        image_sprite.add(music_img)
        image_sprite.add(sound_img)
        image_sprite.draw(surf)
        text_sprites.draw(surf)
        draw_text(surf, "Music", 34, WIDTH / 2 - 100, HEIGHT / 2 - 150)
        draw_text(surf, "Sound", 34, WIDTH / 2 + 100, HEIGHT / 2 - 150)
        set.sm_init = True
    elif set.sm_init:
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONUP:
            mx, my = pygame.mouse.get_pos()
            if back_option.rect.collidepoint(mx, my):
                if set.sound:
                    click_sound.play()
                set.option_start = True
                set.sm = False
                set.sm_init = False
                text_sprites.empty()
                image_sprite.empty()
                f1.close()
                f2.close()
            elif music_img.rect.collidepoint(mx, my):
                if on == "1":
                    f1.seek(0)
                    f1.truncate(0)
                    f1.write("0")
                    music_img.change(off)
                    on = "0"
                    pygame.mixer.music.pause()
                elif on == "0":
                    f1.seek(0)
                    f1.truncate(0)
                    f1.write("1")
                    on = "1"
                    music_img.change(onn)
                    pygame.mixer.music.unpause()
            elif sound_img.rect.collidepoint(mx, my):
                if ons == "1":
                    f2.seek(0)
                    f2.truncate(0)
                    sound_img.change(off)
                    f2.write("0")
                    ons = "0"
                    set.sound = False
                elif ons == "0":
                    f2.seek(0)
                    f2.truncate(0)
                    sound_img.change(onn)
                    f2.write("1")
                    ons = "1"
                    set.sound = True
        elif event.type == pygame.QUIT:
            set.running = False
        text_sprites.update(surf)
        text_sprites.draw(surf)
        image_sprite.draw(surf)
        draw_text(surf, "Music", 34, WIDTH / 2 - 100, HEIGHT / 2 - 150)
        draw_text(surf, "Sound", 34, WIDTH / 2 + 100, HEIGHT / 2 - 150)


def screen_fill():
    screen.fill(BLACK)
    screen.blit(bg, (0, 0))


def playerupdate(img_name):
    global player_rotated_img, f1, text
    f1.seek(0)#we use seek bcx truncate method leaves white spaces
    f1.truncate(0)#to remove content from file and 0 is the cursor it means from start of the file
    f1.write(img_name)
    text = img_name
    set.player_img = pygame.image.load(path.join(img_dir, img_name))
    player_rotated_img = pygame.transform.rotate(pygame.transform.scale(set.player_img, (45, 38)), 315)
    set.player_mini_img = pygame.transform.scale(set.player_img, (25, 19))
    set.player_mini_img.set_colorkey(BLACK)
