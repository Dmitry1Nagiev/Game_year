

import pygame
import sys

import pygwidgets

from sprites.sprite_classes import *
from camera import Camera

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
    global camera,all_sprites,water_group,collision_sprites,player_group,player
    water_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    collision_sprites = pygame.sprite.Group()
    player = Player(player_images['right'][0], (10, 10), collision_sprites)

    player_group.add(player)
    camera = Camera(8000, 8000, WIDTH, HEIGHT)
    all_sprites = pygame.sprite.Group()

def lvlGame():
    global camera,collision_sprites,water_group,mapFile
    player_group.update(dt, FPS, player_images)
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


dt = clock.tick(FPS) / 1000


restart()
loadMap(mapFile)
drawMap()

all_sprites.add(player)



while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    window.fill(BLACK)
    lvlGame()