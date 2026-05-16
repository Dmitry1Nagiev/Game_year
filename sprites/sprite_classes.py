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
    def __init__(self,image,pos,collision_sprites):
        super().__init__()
        self.image = image

        self.pl_img = pygame.transform.scale(self.image, (65, 75))
        self.image = self.pl_img

        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.Vector2(self.rect.center)
        self.direction = pygame.Vector2()
        self.speed = 10
        self.im_dir = 'right'
        self.frame = 0
        self.timer_anime = 0
        self.anime = False
        self.collision_spite = collision_sprites
    def collision(self,direction):
        for sprite in self.collision_spite:
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
    def move(self,dt):
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
            self.anime =True
        else:
            self.anime = False

    def animation(self,FPS,player_images):
        if self.anime:
            self.timer_anime += 1
            self.image = player_images[self.im_dir][self.frame]
            if self.timer_anime / FPS > 0.1:
                if self.frame==len(player_images[self.im_dir]) - 1:
                    self.frame = 0
                else:
                    self.frame += 1
                self.timer_anime = 0
    def update(self,dt,FPS,player_images):
        self.input()
        self.move(dt)
        self.animation(FPS,player_images)
        self.pl_img = pygame.transform.scale(self.image, (65, 75))
        self.image = self.pl_img

