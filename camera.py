import pygame

class Camera:
    def __init__(self,width,height,screen_width,screen_height):
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = pygame.Vector2()
    def draw(self,window,all_sprites):
        for sprite in all_sprites:
            window.blit(sprite.image,sprite.rect.topleft - self.offset)
    def update(self,target,window,all_sprites):
        self.draw(window,all_sprites)
        self.offset.x = target.rect.centerx - self.screen_width // 2
        self.offset.y = target.rect.centery - self.screen_height // 2
        self.offset.x = max(0,min(self.offset.x,
                                  self.width - self.screen_width))
        self.offset.y = max(0,min(self.offset.y,
                                 self.height - self.screen_height))