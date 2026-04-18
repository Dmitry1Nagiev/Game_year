import pygame

from script import load_image

player_images = {'right': load_image('assets/images/Frisk_animation/Right'),
                 'left': load_image('assets/images/Frisk_animation/Left'),
                 'up': load_image('assets/images/Frisk_animation/Up'),
                 'down': load_image('assets/images/Frisk_animation/Down')}
water_image = pygame.image.load('assets/images/water.png')
Grav_image = pygame.image.load('assets/images/blocks/Grav.png')