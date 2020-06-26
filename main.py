import pygame
from screens import *
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
while set.running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            set.running = False
    if set.main_menu:
        menu_screen(screen)
    if set.start_game:
        start_screen(screen)
    if set.option_start:
        option_screen(screen)
    if set.ship_option:
        ship_option_screen(screen)
    if set.sm:
        soundandmusic(screen)
    pygame.display.flip()
pygame.quit()
