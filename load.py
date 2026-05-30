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
grav_image = pygame.image.load('assets/images/blocks/Grav.png')
kysty_image = pygame.image.load('assets/images/blocks/kysty.jpg')
trava_image = pygame.image.load('assets/images/blocks/trava.jpg')


solid_image_walk_down = {'walk_vertical':load_image('assets/images/Solider_animation/Walk_Down')}
solid_image_walk_right = {'walk_horisont':load_image('assets/images/Solider_animation/Walk_right')}
solid_image_attack_down = {'attack':load_image('assets/images/Solider_animation/Attack_Down')}



Bull_image = pygame.image.load('assets/images/niga_bulet.png')

kamn_image = pygame.image.load('assets/images/Objects/raveh-removebg-preview.png')
kusty_image = pygame.image.load('assets/images/Objects/kust-removebg-preview.png')
bochka_image = pygame.image.load('assets/images/Objects/bochka-removebg-preview.png')
aptechka_image_1 = pygame.image.load('assets/images/Objects/aptechko.png')
aptechka_image = pygame.transform.scale(aptechka_image_1,(70,70))



gun_sound  = pygame.mixer.Sound('assets/images/Sounds/awp_02.wav')
heal_sound = pygame.mixer.Sound('assets/images/Sounds/undertale-save.wav')
wave_sound = pygame.mixer.Sound('assets/images/Sounds/zombies.wav')
loos_hp_sound = pygame.mixer.Sound('assets/images/Sounds/undertale-sound-effect-attack-hit.wav')
loosing_life_sound = pygame.mixer.Sound('assets/images/Sounds/gta-v-death-sound-effect-102.wav')

win_music = pygame.mixer.Sound('assets/images/Sounds/undertale_096. Last Goodbye (online-audio-converter.com) (1).ogg')


fon_music = pygame.mixer_music.load('assets/images/Sounds/doom_eternal_22. The Only Thing They Fear Is You.wav')
buttons_images = load_image('assets/images/buttons_animation')

button_up_img = buttons_images[0]

button_down_img = buttons_images[2]
button_down_img.set_colorkey((255,255,255))



gun_sound.set_volume(0.3)
wave_sound.set_volume(1)