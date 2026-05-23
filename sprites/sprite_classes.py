import pygame
WHITE = 255,255,255
import random




class Diamond(pygame.sprite.Sprite):
    def __init__(self,image,pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)

class Water(pygame.sprite.Sprite):
    def __init__(self,image,pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)

class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos, collision_sprites):
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
        self.anime = {'wlk': False,
                      'attck': False}
        self.collision_sprites = collision_sprites


        self.down_frames_scaled = None
        self.right_frames_scaled = None

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




    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0
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
        if pygame.mouse.get_pressed()[0]:
            click_pos = pygame.mouse.get_pos()
            if ((click_pos[0] - self.rect.center[0]) ** 2 + (
                click_pos[1] - self.rect.center[1]) ** 2) ** 0.5 <= 1000:
                self.im_dir = 'attack'
                self.anime['attck'] = True


    def animation(self, FPS, down_frames, right_frames):
        if self.down_frames_scaled is None:
            self.down_frames_scaled = [pygame.transform.scale(img, self.size) for img in down_frames]
            self.right_frames_scaled = [pygame.transform.scale(img, self.size) for img in right_frames]

        if self.anime['wlk']:
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

            if self.timer_anime / FPS > 0.03:
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
            else:  # right
                self.image = self.right_frames_scaled[0]
        if self.anime['attck']:
            self.timer_anime += 1




    def update(self, dt, FPS, down_frames, right_frames):
        self.input()
        self.move(dt)
        self.animation(FPS, down_frames, right_frames)

    def update(self, dt, FPS, down_frames, right_frames,solid_image_attack_down):
        self.input()
        self.move(dt)
        self.animation(FPS, down_frames, right_frames,solid_image_attack_down)

