import random

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
player = pygame.Surface(player_size)
player.fill(COLOR_WHITE)
player_rect = player.get_rect()
player_move_down = [0, 1]
player_move_up = [0, -1]
player_move_right = [1, 0]
player_move_left = [-1, 0]


def crate_enemy():
    enemy_size = (30, 30)
    enemy = pygame.Surface(enemy_size)
    enemy.fill(COLOR_BLUE)
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *enemy_size)
    enemy_move = [random.randint(-6, -1), 0]
    return [enemy, enemy_rect, enemy_move]


def create_bonus():
    bonus_size = (20, 20)
    bonus = pygame.Surface(bonus_size)
    bonus.fill(COLOR_YELLOW)
    bonus_rect = pygame.Rect(random.randint(10, WIDTH - bonus_size[0]), 0, *bonus_size)
    bonus_speed = [0, 3]
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

    bg_X1 -= bg_move
    main_display.blit(bg, (0, 0))

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
    main_display.blit(player, player_rect)

    pygame.display.flip()

    print(len(enemies))
    print(len(bonuses))

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))


pygame.quit()
