import sys

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
bg_move = 2

class Player(pygame.sprite.Sprite):
    def __init__(self, images, x, y, speed):
        super().__init__()
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.index = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keys[K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        # Зміна картинки гравця для анімації руху
        self.index = (self.index + 1) % len(self.images)
        self.image = self.images[self.index]

def crate_enemy():
    enemy_size = (20, 20)
    enemy_original = pygame.image.load("enemy.png").convert_alpha()
    enemy = pygame.transform.scale(
        enemy_original,
        (enemy_original.get_width() // 2, enemy_original.get_height() // 2),
    )
    enemy_rect = pygame.Rect(
        WIDTH + 200, random.randint(200, HEIGHT - 200), *enemy_size
    )
    enemy_move = [random.randint(-1, -1), 0]
    enemies.add([enemy, enemy_rect, enemy_move]) 
    enemy_move = [-ENEMY_SPEED, 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus_size = (20, 20)
    bonus = pygame.image.load("bonus.png").convert_alpha()
    bonus_rect = pygame.Rect(random.randint(10, WIDTH - bonus_size[0]), 0, *bonus_size)
    bonus_speed = [4, 8]
    return [bonus, bonus_rect, bonus_speed]

player_images = [
    pygame.image.load("1-1.png").convert_alpha(),
    pygame.image.load("1-2.png").convert_alpha(),
    pygame.image.load("1-3.png").convert_alpha(),
    pygame.image.load("1-4.png").convert_alpha(),
    pygame.image.load("1-5.png").convert_alpha(),
]
player = Player(player_images, 100, HEIGHT / 2 - player_images[0].get_height() / 2, 4)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


ENEMY_SPEED = 1
#ENEMY_FREQUENCY = 3000 

CHANGE_PLAYER_IMAGE = pygame.USEREVENT + 1
CREATE_ENEMY = pygame.USEREVENT + 1
CREATE_BONUS = pygame.USEREVENT + 2

pygame.time.set_timer(CREATE_ENEMY, 1500)
pygame.time.set_timer(CREATE_BONUS, 3000)
pygame.time.set_timer(CHANGE_PLAYER_IMAGE, 1500)


enemies = pygame.sprite.Group()
bonuses = pygame.sprite.Group()

score = 0

playing = True

while playing:
    FPS.tick(110)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.add(crate_enemy())
        if event.type == CREATE_BONUS:
            bonuses.add(create_bonus())

        if event.type == CHANGE_PLAYER_IMAGE:
            player.update()

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()
    if keys[K_DOWN] and player.rect.bottom < HEIGHT:
        player.rect.y += player.speed
    if keys[K_UP] and player.rect.top > 0:
        player.rect.y -= player.speed
    if keys[K_RIGHT] and player.rect.right < WIDTH:
        player.rect.x += player.speed
    if keys[K_LEFT] and player.rect.left > 0:
        player.rect.x -= player.speed

    for enemy in enemies.sprites():
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
        if player.rect.colliderect(enemy[1]):
            playing = False

    for bonus_info in bonuses:
        bonus_info[1].move_ip(bonus_info[2])
        main_display.blit(bonus_info[0], bonus_info[1].topleft)
        if player.rect.colliderect(bonus_info[1]):
            score += 1
            bonuses.remove(bonus_info)

    print(len(enemies))
    print(len(bonuses))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))
    all_sprites.update()
    all_sprites.draw(main_display)

    

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.remove(enemy)

pygame.quit()
sys.exit()