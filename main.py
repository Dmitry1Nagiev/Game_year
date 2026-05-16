

import pygame
import sys
import random
import pygwidgets

from sprites.sprite_classes import *
from camera import Camera
from collections import deque
BLACK = (0,0,0)
WIDTH = 1500
HEIGHT = 1000


mapFile = ('game_locations/test_player1.txt')
FPS = 60

open_size = 20

window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('underverse')
clock = pygame.time.Clock()
from load import *
pygame.init()


def restart():
    global camera, all_sprites, water_group, collision_sprites, player_group, player, zombi, zombi_group

    water_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    zombi_group = pygame.sprite.Group()
    collision_sprites = pygame.sprite.Group()

    # Создаем ОДНОГО игрока
    player = Player(player_images['right'][0], (1000, 1000), collision_sprites)

    # Создаем ОДНОГО зомби
    zombi = Zombi(zombi_image_idle[0], (800, 50))

    # Добавляем в группы
    player_group.add(player)
    zombi_group.add(zombi)  # Добавляем зомби в группу

    camera = Camera(8000, 8000, WIDTH, HEIGHT)
    all_sprites = pygame.sprite.Group()


def lvlGame():
    global camera, collision_sprites, water_group, mapFile, player, zombi

    # Обновляем ОДНОГО игрока
    player.update(dt, FPS, player_images)

    # Обновляем ОДНОГО зомби (передаем одного игрока, а не список)
    zombi.update(FPS, zombi_image_walk,zombi_image_attack, player)  # player, не players

    # Обновляем группу зомби (если используете)
    zombi_group.update(FPS, zombi_image_walk,zombi_image_attack, player)

    # Обновляем камеру
    camera.update(player, window, all_sprites)

    # Рисуем все спрайты

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
        for i in range(20):
            game_map.append(file.readline().replace('\n', '').split(','))

    pos = [0, 0]
    for i in range(20):
        pos[1] = i * 80
        for j in range(30):
            pos[0] = j * 80

            if game_map[i][j] == '1':
                water = Water(water_image,pos)
                water_group.add(water)
                #collision_sprites.add(water)
                all_sprites.add(water)


def get_grid():
    # Создаем сетку на основе размера карты, а не экрана
    grid_width = 8000 // 40  # 8000 - размер вашей карты
    grid_height = 8000 // 40
    grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

    for water in water_group:
        x = water.rect.x // 40
        y = water.rect.y // 40
        if 0 <= x < grid_width and 0 <= y < grid_height:
            grid[y][x] = 1

    return grid


def bfs(start, goal, grid):
    if start == goal:
        return [start]

    queue = deque()
    queue.append((start, [start]))
    visited = set()
    visited.add(start)

    while queue:
        (current, path) = queue.popleft()

        # Проверяем соседей (вверх, вниз, влево, вправо)
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            next_pos = (current[0] + dx, current[1] + dy)

            # Проверяем границы и препятствия
            if (0 <= next_pos[0] < len(grid[0]) and
                    0 <= next_pos[1] < len(grid) and
                    next_pos not in visited):

                # Проверяем, не является ли клетка препятствием (водой)
                if grid[next_pos[1]][next_pos[0]] == 0:  # 0 - проходимая клетка
                    if next_pos == goal:
                        return path + [next_pos]

                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))

    return None  # Путь не найден



class Zombi(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = 3
        self.dir = "top"
        self.timer_move = 0
        self.trigger = False
        self.timer_anime = 0
        self.frame = 0
        self.path = None
        # Состояния: 'walk' или 'attack'
        self.state = 'walk'
        self.attack_timer = 0
        self.attack_duration = 30   # кадров анимации атаки (0.5 сек при 60 FPS)

    def try_move(self, dx, dy):
        """Проверяет, можно ли сделать шаг (стены, вода, игрок)"""
        next_rect = self.rect.copy()
        next_rect.x += dx
        next_rect.y += dy

        # Границы карты (8000x8000)
        if next_rect.x < 0 or next_rect.x > 8000 or next_rect.y < 0 or next_rect.y > 8000:
            return False

        # Проверка воды
        temp_self = pygame.sprite.Sprite()
        temp_self.rect = next_rect
        if pygame.sprite.spritecollide(temp_self, water_group, False):
            return False

        # Проверка столкновения с игроком (не проходить сквозь)
        if pygame.sprite.collide_rect(temp_self, player):
            return False

        return True

    def update(self, FPS, zombi_image_walk, zombi_image_attack, player):
        self.timer_move += 1

        if player is None:
            return

        distance_to_player = ((self.rect.centerx - player.rect.centerx) ** 2 +
                              (self.rect.centery - player.rect.centery) ** 2) ** 0.5

        # Если очень близко – атакуем
        if distance_to_player < 80:
            if self.state != 'attack':
                self.state = 'attack'
                self.attack_timer = self.attack_duration
                self.frame = 0
            self.anime = True
            # Уменьшаем таймер атаки
            if self.attack_timer > 0:
                self.attack_timer -= 1
            else:
                self.state = 'walk'
        else:
            # Игрок далеко – возвращаемся к ходьбе
            if self.state == 'attack':
                self.state = 'walk'
                self.frame = 0

            # Логика движения (только в режиме ходьбы)
            self.trigger = distance_to_player < 500
            if self.trigger:
                if self.timer_move % 60 == 0:
                    grid = get_grid()
                    start = (self.rect.x // 40, self.rect.y // 40)
                    goal = (player.rect.x // 40, player.rect.y // 40)
                    self.path = bfs(start, goal, grid)
                if hasattr(self, 'path') and self.path and len(self.path) > 1:
                    self.move_along_path()
                else:
                    self.random_movement()
            else:
                self.random_movement()

        # Анимация
        self.animation(FPS, zombi_image_walk, zombi_image_attack)

    def move_along_path(self):
        """Движение по найденному пути BFS"""
        if not self.path or len(self.path) <= 1:
            return

        next_cell = self.path[1]
        target_x = next_cell[0] * 40 + 20
        target_y = next_cell[1] * 40 + 20

        # Движение по X
        dx = 0
        if abs(self.rect.centerx - target_x) > self.speed:
            if self.rect.centerx < target_x:
                dx = self.speed
                self.dir = 'right'
            else:
                dx = -self.speed
                self.dir = 'left'
            if self.try_move(dx, 0):
                self.rect.x += dx
        elif len(self.path) > 1:
            self.path.pop(0)

        # Движение по Y
        dy = 0
        if abs(self.rect.centery - target_y) > self.speed:
            if self.rect.centery < target_y:
                dy = self.speed
                self.dir = 'bottom'
            else:
                dy = -self.speed
                self.dir = 'top'
            if self.try_move(0, dy):
                self.rect.y += dy
        elif len(self.path) > 1:
            self.path.pop(0)

        self.anime = True

    def random_movement(self):
        """Случайное движение, когда зомби не видит игрока или нет пути"""
        if self.timer_move % 60 == 0:
            self.dir = random.choice(['top', 'bottom', 'left', 'right'])

        dx, dy = 0, 0
        if self.dir == 'top':
            dy = -self.speed
        elif self.dir == 'bottom':
            dy = self.speed
        elif self.dir == 'left':
            dx = -self.speed
        elif self.dir == 'right':
            dx = self.speed

        if self.try_move(dx, dy):
            self.rect.x += dx
            self.rect.y += dy
            self.anime = True
        else:
            self.dir = random.choice(['top', 'bottom', 'left', 'right'])
            self.anime = False

    def animation(self, FPS, zombi_image_walk, zombi_image_attack):
        if self.anime:
            self.timer_anime += 1
            # Выбираем кадры в зависимости от состояния
            if self.state == 'walk':
                frames = zombi_image_walk['walk']   # предполагаем ключ 'walk'
            else:
                frames = zombi_image_attack          # список кадров атаки

            if self.frame >= len(frames):
                self.frame = 0

            frame_img = frames[self.frame]

            # Отражение при движении вправо (только для ходьбы, но можно и для атаки)
            if self.dir == 'left':
                frame_img = pygame.transform.flip(frame_img, True, False)

            self.image = frame_img

            if self.timer_anime / FPS > 0.1:
                self.frame = (self.frame + 1) % len(frames)
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