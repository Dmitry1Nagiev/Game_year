import pygame

from script import load_image

player_images_1 = {'right': load_image('assets/images/Frisk_animation/Right'),
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


solid_image_walk_down = {'walk_vertical':load_image('assets/images/Solider_animation/Walk_Down')}
solid_image_walk_right = {'walk_horisont':load_image('assets/images/Solider_animation/Walk_right')}
solid_image_attack_down = {'attack':load_image('assets/images/Solider_animation/Attack_Down')}