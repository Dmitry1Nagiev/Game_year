import pygame
import math
from camera import *


WHITE = 255, 255, 255
import random

class Bochka(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.im_dir = 'Up'
class Aptechka(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
class Gravey(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
class Kamn(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
class Trava(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
class Kysty(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)


class Water(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)


import pygame

class Player(pygame.sprite.Sprite):
    global all_sprites
    def __init__(self, image, pos, collision_sprites, bull_group, camera,all_sprites,gun_sound):
        super().__init__()
        self.size = (70, 70)
        self.image = pygame.transform.scale(image, self.size)
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.Vector2(self.rect.center)
        self.direction = pygame.Vector2()
        self.speed = 250
        self.im_dir = 'down'
        self.frame = 0
        self.timer_anime = 0
        self.anime = {'wlk': False, 'attck': False}
        self.collision_sprites = collision_sprites
        self.bull_group = bull_group
        self.camera = camera

        # Таймер для атаки
        self.attack_timer = 0
        self.attack_duration = 0.3
        self.shoot_cooldown = 0
        self.shoot_cooldown_max = 1   # секунд между выстрелами

        self.down_frames_scaled = None
        self.right_frames_scaled = None
        self.attack_frames_scaled = None

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                    self.pos.x = self.rect.centerx
                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                    self.pos.y = self.rect.centery

    def move(self, dt):
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        self.collision('horizontal')

        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y
        self.collision('vertical')

    def shoot(self, target_pos, Bull_image, all_sprites,gun_sound):
        """Создаёт пулю, летящую в точку target_pos (мировые координаты)"""
        direction = (target_pos[0] - self.rect.centerx, target_pos[1] - self.rect.centery)
        if direction[0] == 0 and direction[1] == 0:
            return

        # Определяем направление выстрела для анимации
        dx, dy = direction
        if abs(dx) > abs(dy):
            self.im_dir = 'right' if dx > 0 else 'left'
        else:
            self.im_dir = 'down' if dy > 0 else 'up'

        gun_sound.play()
        bullet = Bull(Bull_image, self.rect.center, direction)
        self.bull_group.add(bullet)
        all_sprites.add(bullet)

        # Запускаем анимацию атаки
        self.anime['attck'] = True
        self.attack_timer = 0
        self.frame = 0

    def input(self,Bull_image,all_sprites,gun_sound):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0

        if self.anime['attck']:
            return

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.im_dir = 'right'
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.im_dir = 'left'
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.im_dir = 'up'
        if keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.im_dir = 'down'

        if self.direction.length() != 0:
            self.direction = self.direction.normalize()
            self.anime['wlk'] = True
        else:
            self.anime['wlk'] = False

        # Выстрел
        if pygame.mouse.get_pressed()[0] and self.shoot_cooldown <= 0:
            click_pos = pygame.mouse.get_pos()
            world_click = self.camera.screen_to_world(click_pos)
            distance = ((world_click[0] - self.rect.centerx) ** 2 +
                        (world_click[1] - self.rect.centery) ** 2) ** 0.5
            if distance <= 1000:
                self.shoot(world_click,Bull_image,all_sprites,gun_sound)
                self.shoot_cooldown = self.shoot_cooldown_max

    def animation(self, FPS, down_frames, right_frames, attack_frames):
        if self.down_frames_scaled is None:
            self.down_frames_scaled = [pygame.transform.scale(img, self.size) for img in down_frames]
            self.right_frames_scaled = [pygame.transform.scale(img, self.size) for img in right_frames]
            self.attack_frames_scaled = [pygame.transform.scale(img, self.size) for img in attack_frames]

        # Анимация атаки
        if self.anime['attck']:
            self.attack_timer += 1 / FPS
            if self.frame < len(self.attack_frames_scaled):
                frame_img = self.attack_frames_scaled[self.frame]

                # Отражаем кадр в зависимости от направления
                if self.im_dir == 'left':
                    frame_img = pygame.transform.flip(frame_img, True, False)
                elif self.im_dir == 'up':
                    frame_img = pygame.transform.flip(frame_img, False, True)

                self.image = frame_img

                if self.attack_timer > 0.12:  # смена кадра
                    self.frame += 1
                    self.attack_timer = 0
            else:
                self.anime['attck'] = False
                self.frame = 0
                # Возвращаемся к спрайту стояния с учётом последнего направления
                if self.im_dir == 'down':
                    self.image = self.down_frames_scaled[0]
                elif self.im_dir == 'up':
                    self.image = pygame.transform.flip(self.down_frames_scaled[0], False, True)
                elif self.im_dir == 'left':
                    self.image = pygame.transform.flip(self.right_frames_scaled[0], True, False)
                else:  # 'right'
                    self.image = self.right_frames_scaled[0]
            return

        # ... остальная часть метода (ходьба, стойка) без изменений

        # Анимация ходьбы
        elif self.anime['wlk']:
            self.timer_anime += 1
            if self.im_dir in ('down', 'up'):
                frames = self.down_frames_scaled
                flip_x = False
                flip_y = (self.im_dir == 'up')
            else:
                frames = self.right_frames_scaled
                flip_x = (self.im_dir == 'left')
                flip_y = False

            if self.frame >= len(frames):
                self.frame = 0
            frame_img = frames[self.frame]
            if flip_x or flip_y:
                frame_img = pygame.transform.flip(frame_img, flip_x, flip_y)
            self.image = frame_img

            if self.timer_anime / FPS > 0.08:
                self.frame = (self.frame + 1) % len(frames)
                self.timer_anime = 0
        else:
            # Стоим
            if self.im_dir == 'down':
                self.image = self.down_frames_scaled[0]
            elif self.im_dir == 'up':
                self.image = pygame.transform.flip(self.down_frames_scaled[0], False, True)
            elif self.im_dir == 'left':
                self.image = pygame.transform.flip(self.right_frames_scaled[0], True, False)
            else:
                self.image = self.right_frames_scaled[0]

    def update(self, dt, FPS, down_frames, right_frames, attack_frames,Bull_image,all_sprites,gun_sound):
        self.input(Bull_image,all_sprites,gun_sound)
        self.move(dt)
        self.animation(FPS, down_frames, right_frames, attack_frames)
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
        self.all_sprites = all_sprites




class Bull(pygame.sprite.Sprite):
    def __init__(self, image, pos, direction):
        super().__init__()
        self.original_image = image
        self.size = (20, 30)
        self.image = pygame.transform.scale(image, self.size)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.direction = pygame.Vector2(direction).normalize()
        self.speed = 1000   # пикселей в секунду
        self.rotate_image()

    def rotate_image(self):
        """Поворачивает изображение снаряда в соответствии с направлением движения"""
        angle_rad = math.atan2(self.direction.y, self.direction.x)
        angle_deg = math.degrees(angle_rad)
        scaled_img = pygame.transform.scale(self.original_image, self.size)
        self.image = pygame.transform.rotate(scaled_img, -angle_deg)
        # Сохраняем центр спрайта, чтобы не сместился при повороте
        center = self.rect.center
        self.rect = self.image.get_rect(center=center)

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos
        # Удаляем пулю, если она вышла за пределы мира (8000x8000)
        if (self.rect.right < 0 or self.rect.left > 8000 or
            self.rect.bottom < 0 or self.rect.top > 8000):
            self.kill()






