

import pygame
import sys

import pygwidgets

from sprites.sprite_classes import *
from camera import Camera
from collections import deque
BLACK = (0,0,0)
WIDTH = 1500
HEIGHT = 1000


mapFile = ('game_locations/test_player1.txt')
FPS = 60

open_size = 10

window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('underverse')
clock = pygame.time.Clock()
from load import *
pygame.init()


def restart():
    global camera,all_sprites,water_group,collision_sprites,player_group,player,zombi,zombi_group
    water_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    zombi_group = pygame.sprite.Group()
    collision_sprites = pygame.sprite.Group()
    player = Player(player_images['right'][0], (10, 10), collision_sprites)
    zombi = Zombi(zombi_image_idle[0],  (800,50))

    player_group.add(player)
    camera = Camera(8000, 8000, WIDTH, HEIGHT)
    all_sprites = pygame.sprite.Group()

def lvlGame():
    global camera,collision_sprites,water_group,mapFile
    player_group.update(dt, FPS, player_images)
    zombi_group.update(FPS,zombi_image_walk)
    camera.update(player, window, all_sprites)
    pygame.display.update()

game_map = []
def loadMap(mapFile):
    global game_map
    with open(mapFile,'r') as file:
        for line in file:
            game_map.append(line.replace('/n', '').split(','))
def drawMap():
    global player_group, player, water_group,collision_sprites,game_map

    water_group.empty()
    collision_sprites.empty()


    with open(mapFile, 'r') as file:
        for i in range(10):
            game_map.append(file.readline().replace('\n', '').split(','))

    pos = [0, 0]
    for i in range(open_size):
        pos[1] = i * 80
        for j in range(open_size):
            pos[0] = j * 80
            if game_map[i][j] == '1':
                water = Water(water_image,pos)
                water_group.add(water)
                #collision_sprites.add(water)
                all_sprites.add(water)


def get_grid():
    grid = [[0 for _ in range(WIDTH // 40)] for _ in range(HEIGHT // 40)]
    for brick in water_group:
        x = brick.rect.x // 40
        y = brick.rect.y // 40
        grid[y][x] = 1

    return grid
def bfs(start, goal, grid):
    queue = deque()
    queue.append((start, [start]))
    visited = set()
    visited.add(start)


class Zombi(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.direction = pygame.Vector2()
        self.speed = 1
        self.im_dir = 'walk'
        self.dir = "top"
        self.timer_move = 0
        self.timer_shot = 0
        self.trigger = False
        self.atack_dir = None
        self.timer_anime = 0
        self.anime = False
        self.frame = 0

    def try_move(self, dx, dy):
        """Проверяем, можно ли сделать шаг"""
        next_rect = self.rect.copy()
        next_rect.x += dx
        next_rect.y += dy

        # если столкновение с препятствием — шаг отменяется
        if (pygame.sprite.spritecollideany(self, water_group)):
            return False
        return True

    def update(self):

        self.timer_move += 1
        self.timer_shot += 1

        dx, dy = 0, 0
        if self.dir == 'top':

            dy = -self.speed
        elif self.dir == 'bottom':

            dy = self.speed
        elif self.dir == 'left':
            zombi_image_walk1 = pygame.transform.rotate(zombi_image_walk,0,180)
            dx = -self.speed
        elif self.dir == 'right':

            dx = self.speed

        temp_sprite = pygame.sprite.Sprite()
        temp_sprite.rect = self.rect.copy()
        temp_sprite.rect.x += dx
        temp_sprite.rect.y += dy

        if not (pygame.sprite.spritecollideany(temp_sprite, water_group)):
            self.rect = temp_sprite.rect
        else:
            self.dir = random.choice(['top', 'bottom', 'left', 'right'])

        if self.timer_shot / FPS > 1:
            self.timer_shot = 0

        d = ((self.rect.center[0] - player.rect.center[0]) ** 2
             + (self.rect.center[1] - player.rect.center[1]) ** 2) ** (1 / 2)

        if d < 300:
            self.trigger = True
        else:
            self.trigger = False
            self.path = None  # сбрасываем путь, чтобы не зависал

        if self.trigger:
            pos_player = player.rect.center
            pos = self.rect.center
            if pos[0] - pos_player[0] > 0:
                self.atack_dir = ('left', 'top') if (pos[1] - pos_player[1] > 0) else ('left', 'bottom')
            else:
                self.atack_dir = ('right', 'top') if (pos[1] - pos_player[1] > 0) else ('right', 'bottom')

            if self.atack_dir == ('left', 'top'):
                self.dir = 'left'
                if abs(pos[0] - pos_player[0]) < 20:
                    self.dir = 'top'
            elif self.atack_dir == ('left', 'bottom'):
                self.dir = 'left'
                if abs(pos[0] - pos_player[0]) < 20:
                    self.dir = 'bottom'
            elif self.atack_dir == ('right', 'top'):
                self.dir = 'right'
                if abs(pos[0] - pos_player[0]) < 20:
                    self.dir = 'top'
            elif self.atack_dir == ('right', 'bottom'):
                self.dir = 'right'
                if abs(pos[0] - pos_player[0]) < 20:
                    self.dir = 'bottom'

            # если уткнулись в препятствие — рикошет направления
            if (pygame.sprite.spritecollide(self, water_group, False)):
                self.timer_move = 0
                if self.dir == 'top':
                    self.dir = 'bottom'
                elif self.dir == 'bottom':
                    self.dir = 'top'
                elif self.dir == 'left':
                    self.dir = 'right'
                elif self.dir == 'right':
                    self.dir = 'left'

            # ВСЕГДА формируем grid перед BFS
            grid = get_grid()
            start = (self.rect.x // 40, self.rect.y // 40)
            goal = (player.rect.x // 40, player.rect.y // 40)
            path = bfs(start, goal, grid)
            if self.timer_move % FPS == 0:  # раз в секунду
                grid = get_grid()
                start = (self.rect.x // 40, self.rect.y // 40)
                goal = (player.rect.x // 40, player.rect.y // 40)

                if hasattr(self, "path") and self.path and len(self.path) > 1:
                    next_cell = self.path[1]
                    target_x = next_cell[0] * 40
                    target_y = next_cell[1] * 40

                    if self.rect.x < target_x:
                        if self.try_move(self.speed, 0):
                            self.rect.x += self.speed
                            self.dir = 'right'
                    elif self.rect.x > target_x:
                        if self.try_move(-self.speed, 0):
                            self.rect.x -= self.speed
                            self.dir = 'left'
                    elif self.rect.y < target_y:
                        if self.try_move(0, self.speed):
                            self.rect.y += self.speed
                            self.dir = 'bottom'
                    elif self.rect.y > target_y:
                        if self.try_move(0, -self.speed):
                            self.rect.y -= self.speed
                            self.dir = 'top'
                    if self.direction.length() != 0:
                        self.direction = self.direction.normalize()
                        self.anime = True
                    else:
                        self.anime = False
                    self.animation(FPS, zombi_image_walk)

    def animation(self, FPS, zombi_image_walk):
        if self.anime:
            self.timer_anime += 1
            self.image = zombi_image_walk[self.im_dir][self.frame]
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(zombi_image_walk[self.im_dir]) - 1:
                    self.frame = 0
                else:
                    self.frame += 1
                self.timer_anime = 0


dt = clock.tick(FPS) / 1000


restart()
loadMap(mapFile)
drawMap()

all_sprites.add(player)
all_sprites.add(zombi)



while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    window.fill(BLACK)
    lvlGame()