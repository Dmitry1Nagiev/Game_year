import pygame

import pygame

class Camera:
    def __init__(self, world_width, world_height, screen_width, screen_height):
        self.width = world_width          # размер мира по X (например, 8000)
        self.height = world_height        # размер мира по Y (например, 8000)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = pygame.Vector2()

    def update(self, target):
        """Обновляет смещение камеры, следуя за целью (обычно за игроком)"""
        self.offset.x = target.rect.centerx - self.screen_width // 2
        self.offset.y = target.rect.centery - self.screen_height // 2
        # Ограничиваем, чтобы камера не выходила за границы мира
        self.offset.x = max(0, min(self.offset.x, self.width - self.screen_width))
        self.offset.y = max(0, min(self.offset.y, self.height - self.screen_height))

    def draw(self, window, bg_sprites, fg_sprites):
        """Отрисовка: сначала фон bg_sprites, затем передний план fg_sprites"""
        for sprite in bg_sprites:
            window.blit(sprite.image, sprite.rect.topleft - self.offset)
        for sprite in fg_sprites:
            window.blit(sprite.image, sprite.rect.topleft - self.offset)

    def screen_to_world(self, screen_pos):
        """Преобразует экранные координаты (пиксели окна) в мировые координаты"""
        x, y = screen_pos
        world_x = x + self.offset.x
        world_y = y + self.offset.y
        # Ограничиваем границами мира
        world_x = max(0, min(world_x, self.width))
        world_y = max(0, min(world_y, self.height))
        return (world_x, world_y)