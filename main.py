import random #

#import sys
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont("Verdana", 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Your Game")
bg = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

player_size = (20, 20)
#player = pygame.image.load("player.png").convert_alpha() 
player_frames = [
    pygame.image.load("1-1.png").convert_alpha(),
    pygame.image.load("1-2.png").convert_alpha(),
    pygame.image.load("1-3.png").convert_alpha(),
    pygame.image.load("1-4.png").convert_alpha(),
    pygame.image.load("1-5.png").convert_alpha(),
    pygame.image.load("player.png").convert_alpha(),
]
player_frames_number = 0
#player_rect = player.get_rect()
#player_rect = pygame.Rect(100, HEIGHT / 2 - player.get_height() / 2, *player.get_size())
player_index = 0  # Index to keep track of the current player frame
player_rect = pygame.Rect(100, HEIGHT / 2 - player_frames[0].get_height() / 2, 20, 20)

player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_right = [4, 0]
player_move_left = [-4, 0]

# Load multiple frames for the player


def crate_enemy():
    enemy_size = (10, 10)
    enemy_original = pygame.image.load("enemy.png").convert_alpha()
    enemy = pygame.transform.scale(
        enemy_original,
        (enemy_original.get_width() / 2, enemy_original.get_height() / 2),
    )
    enemy_rect = pygame.Rect(
        WIDTH + 200, random.randint(200, HEIGHT - 200), *enemy_size
    )
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus_size = (10, 10)
    bonus = pygame.image.load("bonus.png").convert_alpha()
    bonus_rect = pygame.Rect(random.randint(10, WIDTH - bonus_size[0]), 0, *bonus_size)
    bonus_speed = [4, 8]
    return [bonus, bonus_rect, bonus_speed]


CREATE_ENEMY = pygame.USEREVENT + 1
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_ENEMY, 1500)
pygame.time.set_timer(CREATE_BONUS, 3000)

enemies = []
bonuses = []

score = 0

playing = True

while playing:
    FPS.tick(210)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(crate_enemy())
        if event.type == CREATE_BONUS:
            bonus_info = create_bonus()
            bonuses.append(bonus_info)

        if player_frames_number == 29:
            player_frames_number = 0

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus_info in bonuses:
        bonus_info[1].move_ip(bonus_info[2])
        main_display.blit(bonus_info[0], bonus_info[1].topleft)
        if player_rect.colliderect(bonus_info[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus_info))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))
    main_display.blit(player_frames[player_index], player_rect)
    #main_display.blit(player_frames[player_frames], player_rect)
    #main_display.blit(player, player_rect)

    pygame.display.flip()

    print(len(enemies))
    print(len(bonuses))
    

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    player_index = (player_index + 1) % len(player_frames)

pygame.quit()