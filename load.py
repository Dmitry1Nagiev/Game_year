import pygame

from script import load_image

player_images = {'right': load_image('assets/images/Frisk_animation/Right'),
                 'left': load_image('assets/images/Frisk_animation/Left'),
                 'up': load_image('assets/images/Frisk_animation/Up'),
                 'down': load_image('assets/images/Frisk_animation/Down')}
zombi_image_walk = {'walk':load_image('assets/images/Zomb_anim/Walk')}
zombi_image_idle = load_image('assets/images/Zomb_anim/Idle')
zombi_image_Hurt = load_image('assets/images/Zomb_anim/Hurt')
zombi_image_Dead = load_image('assets/images/Zomb_anim/Dead')
zombi_image_attack = load_image('assets/images/Zomb_anim/attack')
water_image = pygame.image.load('assets/images/water.png')
Grav_image = pygame.image.load('assets/images/blocks/Grav.png')